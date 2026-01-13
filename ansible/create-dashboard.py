#!/usr/bin/env python3
"""
CERBERUS - Zabbix Dashboard Creator
Automatically creates a monitoring dashboard with CPU/RAM graphs
"""
import requests
import json
import sys

ZABBIX_URL = "http://localhost/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"

def zabbix_request(method, params, auth=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    if auth:
        payload["auth"] = auth
    try:
        response = requests.post(ZABBIX_URL, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return {}

def main():
    # Login
    print("[*] Connecting to Zabbix API...")
    result = zabbix_request("user.login", {"username": ZABBIX_USER, "password": ZABBIX_PASS})
    auth_token = result.get("result")
    if not auth_token:
        print("[!] Login failed!")
        sys.exit(1)
    print("[+] Logged in successfully")

    # Get host IDs for node01 and node02
    print("[*] Fetching hosts...")
    result = zabbix_request("host.get", {
        "output": ["hostid", "host"],
        "filter": {"host": ["node01", "node02"]}
    }, auth_token)
    hosts = result.get("result", [])
    
    if len(hosts) < 2:
        print("[!] Hosts node01/node02 not found in Zabbix!")
        print("[!] Make sure Zabbix agents are configured and hosts are added.")
        sys.exit(1)

    node01_id = None
    node02_id = None
    for h in hosts:
        if h["host"] == "node01":
            node01_id = h["hostid"]
        elif h["host"] == "node02":
            node02_id = h["hostid"]

    print(f"[+] node01 ID: {node01_id}")
    print(f"[+] node02 ID: {node02_id}")

    # Get CPU graphs
    print("[*] Fetching CPU graphs...")
    result = zabbix_request("graph.get", {
        "output": ["graphid", "name"],
        "hostids": [node01_id, node02_id],
        "search": {"name": "CPU utilization"}
    }, auth_token)
    cpu_graphs = result.get("result", [])

    cpu_node01 = None
    cpu_node02 = None
    for g in cpu_graphs:
        result2 = zabbix_request("graph.get", {
            "output": ["graphid"],
            "graphids": [g["graphid"]],
            "selectHosts": ["hostid"]
        }, auth_token)
        if result2.get("result"):
            graph_host = result2["result"][0].get("hosts", [{}])[0].get("hostid")
            if graph_host == node01_id:
                cpu_node01 = g["graphid"]
            elif graph_host == node02_id:
                cpu_node02 = g["graphid"]

    print(f"[+] CPU graph node01: {cpu_node01}")
    print(f"[+] CPU graph node02: {cpu_node02}")

    # Get Memory graphs
    print("[*] Fetching Memory graphs...")
    result = zabbix_request("graph.get", {
        "output": ["graphid", "name"],
        "hostids": [node01_id, node02_id],
        "search": {"name": "Memory utilization"}
    }, auth_token)
    mem_graphs = result.get("result", [])

    mem_node01 = None
    mem_node02 = None
    for g in mem_graphs:
        result2 = zabbix_request("graph.get", {
            "output": ["graphid"],
            "graphids": [g["graphid"]],
            "selectHosts": ["hostid"]
        }, auth_token)
        if result2.get("result"):
            graph_host = result2["result"][0].get("hosts", [{}])[0].get("hostid")
            if graph_host == node01_id:
                mem_node01 = g["graphid"]
            elif graph_host == node02_id:
                mem_node02 = g["graphid"]

    print(f"[+] Memory graph node01: {mem_node01}")
    print(f"[+] Memory graph node02: {mem_node02}")

    # Delete existing dashboard
    print("[*] Checking for existing dashboard...")
    result = zabbix_request("dashboard.get", {
        "output": ["dashboardid"],
        "filter": {"name": "CERBERUS - Cluster Monitoring"}
    }, auth_token)
    existing = result.get("result", [])
    if existing:
        zabbix_request("dashboard.delete", [existing[0]["dashboardid"]], auth_token)
        print("[+] Deleted existing dashboard")

    # Create widgets list
    widgets = [
        {
            "type": "hostavail",
            "name": "Nodes Availability",
            "x": 0, "y": 0, "width": 35, "height": 5,
            "fields": []
        },
        {
            "type": "problems",
            "name": "Cluster Alerts",
            "x": 35, "y": 0, "width": 37, "height": 5,
            "fields": []
        },
        {
            "type": "systeminfo",
            "name": "Zabbix Server Info",
            "x": 0, "y": 5, "width": 35, "height": 6,
            "fields": []
        },
        {
            "type": "problemhosts",
            "name": "Problem Hosts",
            "x": 35, "y": 5, "width": 37, "height": 6,
            "fields": []
        }
    ]

    # Add CPU/Memory graphs if found
    if cpu_node01:
        widgets.append({
            "type": "graph",
            "name": "CPU node01",
            "x": 0, "y": 11, "width": 36, "height": 5,
            "fields": [{"type": 6, "name": "graphid.0", "value": cpu_node01}]
        })
    if cpu_node02:
        widgets.append({
            "type": "graph",
            "name": "CPU node02",
            "x": 36, "y": 11, "width": 36, "height": 5,
            "fields": [{"type": 6, "name": "graphid.0", "value": cpu_node02}]
        })
    if mem_node01:
        widgets.append({
            "type": "graph",
            "name": "Memory node01",
            "x": 0, "y": 16, "width": 36, "height": 5,
            "fields": [{"type": 6, "name": "graphid.0", "value": mem_node01}]
        })
    if mem_node02:
        widgets.append({
            "type": "graph",
            "name": "Memory node02",
            "x": 36, "y": 16, "width": 36, "height": 5,
            "fields": [{"type": 6, "name": "graphid.0", "value": mem_node02}]
        })

    # Create dashboard
    print("[*] Creating dashboard...")
    result = zabbix_request("dashboard.create", {
        "name": "CERBERUS - Cluster Monitoring",
        "display_period": 60,
        "auto_start": 1,
        "pages": [{
            "name": "Cluster Overview",
            "widgets": widgets
        }]
    }, auth_token)

    if result.get("result"):
        print("[+] Dashboard 'CERBERUS - Cluster Monitoring' created successfully!")
        print(f"[+] Dashboard ID: {result['result']['dashboardids'][0]}")
    else:
        print(f"[!] Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
