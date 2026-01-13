# fix_ip.ps1
# Based on GOAD project - Modified for Vagrant Connection Stability
# https://github.com/hashicorp/vagrant/issues/5000#issuecomment-258209286

param ([String] $ip)

Write-Host "=== Fix IP Configuration ==="
Write-Host "Target IP: $ip"

$subnet = $ip -replace "\.\d+$", ""
Write-Host "Subnet: $subnet"

# Recherche de l'interface qui possède actuellement une IP dans le subnet (donnée par DHCP VMware)
$name = (Get-NetIPAddress -AddressFamily IPv4 `
    | Where-Object -FilterScript { ($_.IPAddress).StartsWith($subnet) } `
).InterfaceAlias

if (-not $name) {
    Write-Host "No IP match found. Trying fallback to 'Ethernet1' (standard Vagrant Host-Only adapter)..."
    if (Get-NetAdapter -Name "Ethernet1" -ErrorAction SilentlyContinue) {
        $name = "Ethernet1"
    }
}

if ($name) {
    Write-Host "Found interface: $name"
    
    # --- MODIFICATION START ---
    # Cela permet à ce script de se terminer et à Vagrant de recevoir le code "OK" avant que la connexion ne coupe.
    
    Write-Host "Scheduling IP change to $ip in 10 seconds to allow Vagrant to disconnect cleanly..."
    
    # Commande qui sera exécutée en arrière-plan : Attendre 10s -> Changer l'IP -> Log result
    $logFile = "C:\vagrant\ip_fix.log"
    $cmd = "Start-Sleep -Seconds 10; try { netsh.exe int ip set address `"$name`" static $ip 255.255.255.0; Add-Content $logFile 'IP Changed Successfully' } catch { Add-Content $logFile 'IP Change Failed: $_' }"
    
    # Lancement du processus détaché
    Start-Process powershell.exe -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", "& { $cmd }"
    
    Write-Host "IP change scheduled successfully. The connection will drop momentarily after this script exits."
    # --- MODIFICATION END ---

}
else {
    Write-Host "ERROR: No interface found with subnet $subnet"
    Write-Host "Available adapters:"
    Get-NetAdapter | Format-Table Name, Status, MacAddress
}
