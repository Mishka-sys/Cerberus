#!/usr/bin/env python3
"""
Cerberus - High Availability Infrastructure Lab
By Mishka-sys
"""
import os, sys, subprocess, time, shutil, glob, re, argparse
from datetime import datetime

# Fix Windows encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

class Colors:
    FIRE = '\033[38;5;202m'
    EMBER = '\033[38;5;196m'
    PURPLE = '\033[38;5;129m'
    GOLD = '\033[38;5;220m'
    SMOKE = '\033[38;5;240m'
    ASH = '\033[38;5;245m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'

OK = f"{Colors.GREEN}[+]{Colors.ENDC}"
ERR = f"{Colors.EMBER}[x]{Colors.ENDC}"
INFO = f"{Colors.FIRE}[!]{Colors.ENDC}"

class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.start = time.time()
    def update(self, n, txt):
        pct = int(100*n/self.total)
        filled = int(40*n/self.total)
        bar = f"{Colors.FIRE}{'#'*filled}{Colors.SMOKE}{'-'*(40-filled)}{Colors.ENDC}"
        elapsed = time.time() - self.start
        sys.stdout.write(f"\r[{bar}] {Colors.GOLD}{pct:3d}%{Colors.ENDC} | {n}/{self.total} | {Colors.PURPLE}{txt[:25]:<25}{Colors.ENDC} | {int(elapsed//60):02d}:{int(elapsed%60):02d}")
        sys.stdout.flush()
    def done(self):
        self.update(self.total, "Complete")
        print()

class Lab:
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.dir)
        self.os = self._detect_os()
        self.vagrant = "vagrant.exe" if self.os == "wsl" and shutil.which("vagrant.exe") else "vagrant"
        self.provider = self._load_cfg()
        self.log = None
        self.verbose = False

    def _detect_os(self):
        if sys.platform == "win32": return "windows"
        try:
            with open("/proc/version") as f:
                if "microsoft" in f.read().lower(): return "wsl"
        except: pass
        return "linux"

    def _load_cfg(self):
        if os.path.exists(".cerberus_config"):
            with open(".cerberus_config") as f:
                for l in f:
                    if l.startswith("PROVIDER="): return l.strip().split("=")[1]
        return "vmware_desktop"

    def _save_cfg(self, p):
        with open(".cerberus_config", "w") as f: f.write(f"PROVIDER={p}\n")
        self.provider = p

    def _log(self, msg):
        if self.log:
            with open(self.log, "a", encoding='utf-8') as f: f.write(f"[{datetime.now():%H:%M:%S}] {msg}\n")

    def _run(self, cmd, name=None, check=True, silent=False):
        if name: self._log(f"START: {name}")
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                text=True, encoding='utf-8', errors='replace')
        out = ""
        for line in proc.stdout:
            out += line
            if self.verbose and not silent: 
                try:
                    sys.stdout.write(line)
                except:
                    pass
            if self.log:
                with open(self.log, "a", encoding='utf-8', errors='replace') as f: f.write(line)
        rc = proc.wait()
        if name: self._log(f"{'OK' if rc==0 else 'FAIL'}: {name}")
        if rc != 0 and check: raise Exception(f"{name or cmd} failed (exit {rc})")
        return rc, out

    def _wait_winrm(self, ip="192.168.56.30", retries=60):
        self._log("Waiting for WinRM...")
        chk = f"import socket; s=socket.socket(); s.settimeout(2); exit(0 if s.connect_ex(('{ip}',5985))==0 else 1)"
        for i in range(retries):
            if subprocess.run(f'{self.vagrant} ssh admin -c "python3 -c \\"{chk}\\""', shell=True, capture_output=True).returncode == 0:
                self._log(f"WinRM OK after {i+1} tries")
                return True
            time.sleep(10)
        return False

    def check(self):
        print(f"\n{INFO} Checking prerequisites...\n")
        ok = True
        if shutil.which(self.vagrant): print(f"{OK} Vagrant")
        else: print(f"{ERR} Vagrant not found"); ok = False
        if self.provider == "vmware_desktop":
            if any(shutil.which(x) for x in ["vmrun", "vmrun.exe"]): print(f"{OK} VMware")
            else: print(f"{ERR} VMware not found"); ok = False
        else:
            if any(shutil.which(x) for x in ["VBoxManage", "VBoxManage.exe"]): print(f"{OK} VirtualBox")
            else: print(f"{ERR} VirtualBox not found"); ok = False
        print(f"\n{OK if ok else ERR} {'All OK' if ok else 'Errors found'}\n")

    def start(self, verbose=False):
        self.verbose = verbose
        os.makedirs("logs", exist_ok=True)
        self.log = f"logs/install_{datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
        start = time.time()
        
        print(f"\n{'='*60}")
        print(f"            CERBERUS - Deployment")
        print(f"{'='*60}\n")
        print(f"{OK} Provider: {Colors.PURPLE}{self.provider}{Colors.ENDC}")
        print(f"{OK} Log: {Colors.ASH}{self.log}{Colors.ENDC}\n")
        
        if input(f"Start deployment? (y/N) ").lower() != 'y':
            return
        
        print()
        pb = ProgressBar(8)
        
        try:
            pb.update(1, "Linux VMs")
            self._run(f"{self.vagrant} up admin node01 node02 --provider={self.provider}", "Linux VMs", silent=not verbose)
            time.sleep(30)
            
            pb.update(2, "SSH Setup")
            self._run(f'{self.vagrant} ssh admin -c "sudo apt-get update && sudo apt-get install -y sshpass"', silent=True)
            self._run(f'{self.vagrant} ssh admin -c "sshpass -p ansible ssh-copy-id -o StrictHostKeyChecking=no ansible@192.168.56.21"', silent=True)
            self._run(f'{self.vagrant} ssh admin -c "sshpass -p ansible ssh-copy-id -o StrictHostKeyChecking=no ansible@192.168.56.22"', silent=True)
            
            pb.update(3, "Ansible Linux")
            self._run(f'{self.vagrant} ssh admin -c "cd /home/vagrant/ansible && ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts site.yml --limit admin,node01,node02"', "Ansible Linux", silent=not verbose)
            
            pb.update(4, "Windows VM")
            self._run(f"{self.vagrant} up winsrv --provider={self.provider}", "Windows VM", silent=not verbose)
            
            pb.update(5, "WinRM")
            if not self._wait_winrm(): raise Exception("WinRM timeout")
            time.sleep(10)
            
            pb.update(6, "Ansible Windows")
            self._run(f'{self.vagrant} ssh admin -c "cd /home/vagrant/ansible && ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory/hosts site.yml --limit winsrv"', "Ansible Windows", silent=not verbose)
            
            pb.update(7, "PHP Fix")
            self._run(f'{self.vagrant} ssh admin -c "sudo sed -i s/post_max_size=8M/post_max_size=16M/ /etc/php/8.1/fpm/php.ini; sudo systemctl restart php8.1-fpm"', silent=True, check=False)
            
            pb.update(8, "Dashboard")
            self._run(f'{self.vagrant} ssh admin -c "cd /home/vagrant/ansible && ansible-playbook create-dashboard.yml"', "Dashboard", silent=not verbose, check=False)
            
            pb.done()
            elapsed = time.time() - start
            print(f"\n{Colors.GREEN}Success!{Colors.ENDC} Duration: {Colors.GOLD}{int(elapsed//60):02d}m {int(elapsed%60):02d}s{Colors.ENDC}\n")
            self.info()
            
        except Exception as e:
            print(f"\n{ERR} Failed: {e}")
            print(f"{INFO} Check: logs\n")

    def stop(self):
        self._run(f"{self.vagrant} halt", check=False)
        print(f"{OK} Stopped\n")

    def cleanup(self):
        if input(f"Destroy all? (y/N) ").lower() != 'y': return
        self._run(f"{self.vagrant} destroy -f", check=False)
        print(f"{OK} Cleaned\n")

    def logs(self, n=50):
        files = sorted(glob.glob("logs/install_*.txt"), reverse=True)
        if not files: print(f"{INFO} No logs\n"); return
        print(f"{OK} {files[0]}\n")
        with open(files[0], encoding='utf-8', errors='replace') as f:
            for line in f.readlines()[-n:]:
                c = Colors.GREEN if "OK" in line else Colors.EMBER if "FAIL" in line else Colors.ASH
                print(f"{c}{line.rstrip()}{Colors.ENDC}")
        print()

    def creds(self):
        print(f"\n=== CREDENTIALS ===\n")
        for s, items in [
            ("SSH (all VMs)", [("vagrant", "vagrant"), ("ansible", "ansible")]),
            ("HA Cluster", [("hacluster", "hacluster")]),
            ("Zabbix Web", [("Admin", "zabbix")]),
            ("Zabbix DB", [("zabbix", "zabbix_password")]),
            ("Windows AD", [("CERBERUS\\Administrator", "Vagrant123!")]),
            ("AD DSRM", [("-", "P@ssw0rd2025!SafeMode")])
        ]:
            print(f"[*] {s}")
            for u, p in items: print(f"    {u}: {p}")
        print()
        print(f"=== IP ADDRESSES ===\n")
        print(f"[*] Admin (Zabbix):  192.168.56.10")
        print(f"[*] Node01:          192.168.56.21")
        print(f"[*] Node02:          192.168.56.22")
        print(f"[*] WinSrv (AD):     192.168.56.30")
        print(f"[*] VIP:             192.168.56.100")
        print()

    def info(self):
        print(f"\n=== ACCESS ===\n")
        print(f"Zabbix:   http://192.168.56.10/ (Admin/zabbix)")
        print(f"Node01:   http://192.168.56.21/")
        print(f"Node02:   http://192.168.56.22/")
        print(f"VIP:      http://192.168.56.100/")
        print(f"RDP:      192.168.56.30:3389 (CERBERUS\\Administrator)\n")

    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
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
         @@@@@%##@@@@@*=-##      %%%#*                        _                           @@#@@*-===+@*#*##***#@#======+****+*@@@#%#%###%%@@     
           #@@@@@@@@@@@@*=%-    -%*+                         | |                           @*##%@@%===@#****##+@===========***@@@@%#%%%##@@@      
               -@@@+   %@@@@-..-@*+              ___ ___ _ __| |__   ___ _ __ _   _ ___      *##%@@@=-*@##*#@%==========-=*+@@@@@###%#@@@-     
                                                / __/ _ \ '__| '_ \ / _ \ '__| | | / __|
                                               | (_|  __/ |  | |_) |  __/ |  | |_| \__|
                                                \___\___|_|  |_.__/ \___|_|   \__,_|___/
                                             
        """)
        time.sleep(1)
    def status(self):
        try:
            out = subprocess.check_output(f"{self.vagrant} status", shell=True, text=True, 
                                         encoding='utf-8', errors='replace', timeout=10)
            st = "running" if "running" in out else "stopped" if "poweroff" in out else "not created"
            c = Colors.GREEN if st == "running" else Colors.EMBER
        except: st, c = "unknown", Colors.ASH
        print(f"[*] cerberus | {self.provider} | {c}{st}{Colors.ENDC}\n")

    def help(self):
        print(f"\nCommands:")
        for cmd, desc in [
            ("start [-v]", "deploy"), ("stop", "halt VMs"), ("cleanup", "destroy"),
            ("status", "VM status"), ("check", "prerequisites"), ("info", "access info"),
            ("passwd", "credentials"), ("logs [-n N]", "view logs"),
            ("ssh <vm>", "connect"), ("rdp", "Windows RDP"),
            ("provider", "change provider"), ("clear", "refresh"), ("exit", "quit")
        ]:
            print(f"  {cmd:<15} {desc}")
        print()

    def menu(self):
        self.banner()
        self.status()
        while True:
            try:
                inp = input(f"Cerberus/{self.provider} > ").strip().split()
                if not inp: continue
                cmd, args = inp[0].lower(), inp[1:]
                
                if cmd == "start": self.start("-v" in args)
                elif cmd == "stop": self.stop()
                elif cmd in ["cleanup", "destroy"]: self.cleanup()
                elif cmd == "status": subprocess.run(f"{self.vagrant} status", shell=True)
                elif cmd == "check": self.check()
                elif cmd == "info": self.info()
                elif cmd in ["passwd", "creds"]: self.creds()
                elif cmd == "logs":
                    n = 50
                    if "-n" in args:
                        try: n = int(args[args.index("-n")+1])
                        except: pass
                    self.logs(n)
                elif cmd == "ssh" and args: subprocess.run(f"{self.vagrant} ssh {args[0]}", shell=True)
                elif cmd == "rdp":
                    print(f"RDP: 192.168.56.30:3389 | CERBERUS\\Administrator | Vagrant123!")
                    if shutil.which("mstsc.exe"): subprocess.Popen(["mstsc.exe", "/v:192.168.56.30"])
                elif cmd == "provider":
                    print(f"\n[1] vmware\n[2] virtualbox\n")
                    c = input("Choice: ")
                    if c == "1": self._save_cfg("vmware_desktop"); print(f"{OK} VMware\n")
                    elif c == "2": self._save_cfg("virtualbox"); print(f"{OK} VirtualBox\n")
                elif cmd in ["help", "?"]: self.help()
                elif cmd == "clear": self.banner(); self.status()
                elif cmd in ["exit", "q"]: print("Goodbye!"); break
                else: print(f"{ERR} Unknown. Type help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    lab = Lab()
    if len(sys.argv) == 1:
        lab.menu()
    else:
        p = argparse.ArgumentParser()
        sub = p.add_subparsers(dest="cmd")
        s = sub.add_parser("start"); s.add_argument("-v", action="store_true")
        sub.add_parser("stop"); sub.add_parser("cleanup"); sub.add_parser("check")
        sub.add_parser("info"); sub.add_parser("passwd")
        l = sub.add_parser("logs"); l.add_argument("-n", type=int, default=50)
        args = p.parse_args()
        if args.cmd == "start": lab.start(args.v)
        elif args.cmd == "stop": lab.stop()
        elif args.cmd == "cleanup": lab.cleanup()
        elif args.cmd == "check": lab.check()
        elif args.cmd == "info": lab.info()
        elif args.cmd == "passwd": lab.creds()
        elif args.cmd == "logs": lab.logs(args.n)
