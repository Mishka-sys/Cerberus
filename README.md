#  CERBERUS - Guardian of Infrastructure

<div align="center">

```
                                             %@@@@%*                                           %@@@%*                                                                                             
                                             @@##*#@@*              =  #%%#                 #@@@#+*@%                                             
                                            %%*####**.  #@%+      #@@++@# .#%+=          #@@-  :#%%%%@                                            
                                            @##%%%%%%***. .#@@#@@##:.%+  * ++:=##@@#**@@#.  +##%%%%#*@#                                           
                                           *@+%%%%%%%%%%%*=   :.-++-. -++:..-+++=: .*-  :**#%@%%%%%%##@#                                          
                        #%%@@%#*##@@%#%@@%%#@+%%%%%%%@@@@@#*+**++++++++++++++++++++++=-**#@@@%%%%%%%#+@#                                          
                     #@%+-::++:--:.  :::. :*@@%%%%%%%%@@@@#****@@#+++++++++++++++%#*+***%@@@@%%%%%%%#*@@      +###:                               
                      #@@@#++===+++++++++++*%@#%%%%%%@@@@*********+++++++++++++*****#*****@@@@%%%%%%#@@@@%##**+-:-=#%@%@@#+                       
                     @@.    .++++++=.=+++++**@@@%%%%@@@@**************++*+++++++******+++*+@@@%%%%%%@@*++++++++++ .-:.   -#@                      
                 =@@#. -- =++++++++++*%##%****%@@%%%@@@****@@@@@@******************@@@%*****@@@%%%@@@#*++++++++++++= .++@@@@#                     
                @@- ++++=+++++++++++++++*******@@%%@@@****@@@   @@***************%@  @@@%****@@@@%@%***+++**+=++++++++-     #@                    
              *@* +**++*%++++++++++++++++*@@@@##@@@@@****@@@@@@@@@**************#@@: @@@@#***@@@@@@#*****+*++++++++++++++-+++=#@@#                
             *@+.*%%++@#****++******+++*#@.  @@@***@@****%@@@@@@@@**=@@@@@@@%=**#@@@@@@@@#***#@%##*******++++++++++++++++++++++. #@*              
            *@*.*%@*********************@@@.*@@@@*#@@*****%@@@@@%*****@@@@@@#****%@@@@@@@*****@%***#@@@@@*++++++++++++***=.=+++**.:@#             
           @@.-##@@***+******************@@@@@@@@*#@@**#******++#*******@%*********%%@%#******@@**@@+  #@@#****+++++++****%%+++*@*=.@%            
         #@* *%#%@@**#@@*:@%******%*+%:+**@@@@@@#**@@***=======+*@%***%@##@#****@%++==++***#*#@#*#@@@@@@@@#****++++++*******@***@@*=.@%           
        -@:-%%%%@@@**@@@  *@@**#@@@@@@***++++***===*@#*=--=======*@@#########@@@+=========***@@***@@@@@@@@*****++++*************#@#*- @@          
       %@:#%%%%%@@@*#@@@@@@@@*=+@@@@@*****+%@:  =%--%@*+=-========#@*####*##*+@+==========++*@%****@@@@@%*++#@##+++*****%@@*****#@%##* #@         
      *@+%%%%%%%%@@**@@@@@@@@******##+****@@     :+-=*@@+-========*#=####****=@===========+%@@=====++++*****@@@@@@**+*@@  @@@+**#@@%%*#:.@%       
      @@%#######%@@****@@@@#*******@###%*.        @==*@@@@========+@**########%=========*#@@%+=======-*@+****@@@@@*+*@@@..@@@@**%@@##%#%#:@#      
      @@%########@@#****++*%%@%#%@%#-              %=@@##@@@+-=====+@#**#####@========+@@@%@%+=========@@@@%%@#**++++@@@@@@@@#**@@%##%%%%%#@      
      -@@########%@@**+-+@              :+#@@*    *@@@#####%@@@@*+=-=*@%##@@+---==#@@@@@####@@=========#*#####@%++++++@@@@@@@***@@%%%%%%%%#%@     
        @@@#%####%@@@#=-*+         :*@@@%#***%@@@@@@@@@@@@@@@##@@@@@@@@%%%@@@@@@@@@@@@#@@###@@@--=====@:***#####@@@@+++#%@#****%@@%%%%%%%%%%@@    
         @@@@@%##@@@@@*=-##      %%%#*                                                    @@#@@*-===+@*#*##***#@#======+****+*@@@#%#%###%%@@     
           #@@@@@@@@@@@@*=%-    -%*+                                                       @*##%@@%===@#****##+@===========***@@@@%#%%%##@@@      
               -@@@+   %@@@@-..-@*+                                                          *##%@@@=-*@##*#@%==========-=*+@@@@@###%#@@@-     


```

**High Availability Infrastructure Lab**

*Active Directory • Zabbix Monitoring • Pacemaker/Corosync Cluster*

[![Vagrant](https://img.shields.io/badge/Vagrant-2.2.9+-1868F2?style=for-the-badge&logo=vagrant)](https://www.vagrantup.com/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?style=for-the-badge&logo=ansible)](https://www.ansible.com/)
[![Windows Server](https://img.shields.io/badge/Windows_Server-2022-0078D6?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows-server)
[![Rocky Linux](https://img.shields.io/badge/Rocky_Linux-9-10B981?style=for-the-badge&logo=rockylinux)](https://rockylinux.org/)

</div>

---

##  About The Project

**Cerberus** is named after the legendary three-headed dog that guards the gates of the Underworld in Greek mythology. Just as Cerberus protected Hades' realm, this project guards your infrastructure through high availability, continuous monitoring, and centralized authentication.

This project was born from the need to have a complete, reproducible lab environment that demonstrates enterprise-grade infrastructure concepts. Whether you're a student learning about system administration, a professional preparing for certifications, or an engineer testing deployment strategies, Cerberus provides a realistic sandbox to experiment with.

###  What Does Cerberus Do?

Cerberus automatically deploys a complete infrastructure lab featuring:

- ** Active Directory Domain** - A Windows Server 2022 domain controller managing the `cerberus.local` domain with security hardening based on ANSSI recommendations
- ** Zabbix Monitoring** - Enterprise-grade monitoring solution watching over all your infrastructure components with real-time alerting capabilities
- ** High Availability Cluster** - A two-node Pacemaker/Corosync cluster demonstrating automatic failover for web services (Nginx) and file sharing (Samba)
- ** Virtual IP (VIP)** - A floating IP address that automatically moves between cluster nodes during failover events
- ** Security Hardening** - Both Linux and Windows systems are hardened following security best practices

###  Why Cerberus?

| Challenge | Cerberus Solution |
|-----------|-------------------|
| Setting up AD takes hours | One command, fully automated |
| HA clusters are complex to configure | Pre-configured Pacemaker/Corosync |
| Monitoring setup is tedious | Zabbix auto-deployed with agents |
| Labs are hard to reproduce | Vagrant ensures identical environments |



##  Virtual Machines

| Machine | OS | IP Address | RAM | vCPU | Role |
|---------|:--:|:----------:|:---:|:----:|------|
| **admin** | Ubuntu 22.04 | 192.168.56.10 | 2 GB | 2 | Zabbix Server, Ansible Controller |
| **node01** | Rocky Linux 9 | 192.168.56.21 | 1 GB | 1 | HA Cluster Node (Primary) |
| **node02** | Rocky Linux 9 | 192.168.56.22 | 1 GB | 1 | HA Cluster Node (Secondary) |
| **winsrv** | Windows Server 2022 | 192.168.56.30 | 2 GB | 2 | Active Directory Domain Controller |

**Total Resources:** ~6 GB RAM, ~50 GB Disk Space

---

##  Features

###  Active Directory
- Windows Server 2022 Domain Controller
- Domain: `cerberus.local`
- Security hardening (SMBv1 disabled, audit logging, password policies)
- DNS server with forwarders

###  Zabbix Monitoring
- Zabbix Server 7.0 LTS
- Auto-discovery and agent registration
- Pre-configured Linux monitoring templates
- Web interface with dashboards

###  High Availability Cluster
- Pacemaker + Corosync cluster stack
- Active/Passive configuration
- Automatic failover (< 30 seconds)
- Managed resources:
  - **Nginx** - Web server
  - **Samba** - File sharing
  - **Virtual IP** - Floating 192.168.56.100

###  Security Hardening
**Linux (Rocky Linux 9):**
- Firewalld configured
- SSH hardening (no root login, banner)
- Automatic security updates (dnf-automatic)
- Audit logging enabled

**Windows Server 2022:**
- SMBv1 disabled
- LLMNR/NetBIOS disabled
- Password policy enforced
- Audit logging enabled
- RDP with NLA

---

##  Quick Start

### Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads) 2.2.9+
- [VMware Workstation](https://www.vmware.com/products/workstation-pro.html) or [VirtualBox](https://www.virtualbox.org/)
- 8 GB RAM (minimum)
- 50 GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/Mishka-sys/Cerberus.git
cd Cerberus

# Launch the interactive menu
python deploy.py

# Or deploy directly
python deploy.py start
```

### First Launch

```
$ python deploy.py

 CERBERUS
Active Directory + Zabbix + HA Cluster
By Mishka-sys

[*] cerberus | vmware_desktop | not created

Cerberus/vmware_desktop > start
```

The deployment takes approximately **20-30 minutes** depending on your hardware and internet connection.

---

##  Commands

| Command | Description |
|---------|-------------|
| `start` | Deploy the complete lab |
| `start -v` | Deploy with verbose output |
| `stop` | Gracefully stop all VMs |
| `cleanup` | Destroy all VMs and free disk space |
| `status` | Show VM status |
| `check` | Verify prerequisites |
| `info` | Display access URLs and IPs |
| `passwd` | Show all credentials |
| `logs` | View deployment logs |
| `logs -n 100` | View last 100 log lines |
| `ssh <vm>` | SSH into a specific VM |
| `rdp` | Connect to Windows Server via RDP |
| `provider` | Switch between VMware/VirtualBox |
| `help` | Display all commands |

---

##  Credentials

### Linux Systems
| Service | Username | Password |
|---------|----------|----------|
| SSH | `vagrant` | `vagrant` |
| SSH | `ansible` | `ansible` |
| HA Cluster | `hacluster` | `hacluster` |

### Zabbix
| Service | Username | Password |
|---------|----------|----------|
| Web UI | `Admin` | `zabbix` |
| Database | `zabbix` | `zabbix_password` |

### Windows / Active Directory
| Service | Username | Password |
|---------|----------|----------|
| Administrator | `CERBERUS\Administrator` | `Vagrant123!` |
| DSRM | - | `P@ssw0rd2025!SafeMode` |

---

##  Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Zabbix** | http://192.168.56.10/ | Admin / zabbix |
| **Web (VIP)** | http://192.168.56.100/ | - |
| **Node01** | http://192.168.56.21/ | - |
| **Node02** | http://192.168.56.22/ | - |
| **RDP** | 192.168.56.30:3389 | CERBERUS\Administrator |

---

##  Testing the HA Cluster

### Verify Cluster Status
```bash
vagrant ssh admin -c "ssh ansible@192.168.56.21 'sudo pcs status'"
```

### Simulate Failover
```bash
# Stop the active node
vagrant ssh admin -c "ssh ansible@192.168.56.21 'sudo pcs node standby node01'"

# Watch the VIP move to node02
curl http://192.168.56.100/

# Restore node01
vagrant ssh admin -c "ssh ansible@192.168.56.21 'sudo pcs node unstandby node01'"
```

### Test Samba Share
```bash
# From Windows
\\192.168.56.100\shared

# From Linux
smbclient //192.168.56.100/shared -U guest -N
```

---

##  Project Structure

```
cerberus/
├── deploy.py                 # Main deployment script
├── Vagrantfile              # VM definitions
├── README.md
├── .gitignore
├── scripts/
│   ├── ConfigureRemotingForAnsible.ps1
│   └── fix_ip.ps1
├── logs/                    # Deployment logs
└── ansible/
    ├── ansible.cfg
    ├── site.yml             # Main playbook
    ├── create-dashboard.yml
    ├── create-dashboard.py
    ├── inventory/
    │   └── hosts
    ├── group_vars/
    │   ├── all.yml
    │   ├── ha_cluster.yml
    │   └── windows.yml
    └── roles/
        ├── zabbix-server/
        ├── zabbix-agent/
        ├── ha-cluster/
        ├── cluster-resources/
        ├── nginx/
        ├── samba/
        ├── hardening-linux/
        ├── windows-ad/
        └── windows-hardening/
```

---

##  Troubleshooting

### Common Issues

**VMs won't start**
```bash
# Check prerequisites
python deploy.py check

# Try switching provider
python deploy.py
> provider
```

**Ansible fails with connection errors**
```bash
# Check VM status
vagrant status

# Restart VMs
vagrant reload
```

**Windows provisioning fails**
```bash
# Windows needs more time - increase timeout
vagrant up winsrv --provider=vmware_desktop
```

**Cluster resources not starting**
```bash
# Check cluster status
vagrant ssh admin -c "ssh ansible@192.168.56.21 'sudo pcs status'"

# Clear resource failures
vagrant ssh admin -c "ssh ansible@192.168.56.21 'sudo pcs resource cleanup'"
```

### View Logs
```bash
python deploy.py logs -n 100
```

---

##  Contributing

Contributions are welcome! Feel free to:
-  Report bugs
-  Suggest new features
-  Submit pull requests

---

##  License

This project is open source and available under the [MIT License](LICENSE).

---

##  Author

**Mishka-sys**

- GitHub: [@Mishka-sys](https://github.com/Mishka-sys)

---

<div align="center">

** Star this repository if you find it useful! **

*Cerberus - Guarding your infrastructure from the depths of the Underworld* 🔥

</div>
