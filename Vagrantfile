# -*- mode: ruby -*-
# vi: set ft=ruby :

DOMAIN = "cerberus.local"

Vagrant.configure("2") do |config|
  config.vm.box_check_update = false
  config.vm.boot_timeout = 600

  # Admin
  config.vm.define "admin", primary: true do |admin|
    admin.vm.box = "bento/ubuntu-22.04"
    admin.vm.hostname = "admin"
    admin.vm.network "private_network", ip: "192.168.56.10"
    admin.vm.network "forwarded_port", guest: 80, host: 8080
    admin.vm.network "forwarded_port", guest: 443, host: 8443

    admin.vm.provider "vmware_desktop" do |vmware|
      vmware.vmx["displayName"] = "CERBERUS-Admin"
      vmware.vmx["memsize"] = "2048"
      vmware.vmx["numvcpus"] = "2"
    end

    admin.vm.provider "virtualbox" do |vb|
      vb.name = "CERBERUS-Admin"
      vb.memory = "2048"
      vb.cpus = 2
    end

    admin.vm.synced_folder "./ansible", "/home/vagrant/ansible", owner: "vagrant", group: "vagrant"

    admin.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y software-properties-common python3-pip sshpass
      apt-add-repository -y ppa:ansible/ansible
      apt-get update
      apt-get install -y ansible
      su - vagrant -c "ansible-galaxy collection install ansible.windows community.windows community.general ansible.posix"
      
      pip3 install pywinrm requests-ntlm passlib 2>/dev/null || pip3 install pywinrm requests-ntlm passlib --break-system-packages
      
      if [ ! -f /home/vagrant/.ssh/id_rsa ]; then
        su - vagrant -c "ssh-keygen -t rsa -b 4096 -f /home/vagrant/.ssh/id_rsa -N ''"
      fi
      cat >> /etc/hosts << 'HOSTS'
192.168.56.10 admin admin.cerberus.local
192.168.56.21 node01 node01.cerberus.local
192.168.56.22 node02 node02.cerberus.local
192.168.56.30 winsrv winsrv.cerberus.local
192.168.56.100 vip vip.cerberus.local
HOSTS
      chmod 755 /home/vagrant/ansible
    SHELL
  end

  # Nodes
  (1..2).each do |i|
    config.vm.define "node0#{i}" do |node|
      node.vm.box = "bento/rockylinux-9"
      node.vm.hostname = "node0#{i}"
      node.vm.network "private_network", ip: "192.168.56.2#{i}"
      node.vm.network "forwarded_port", guest: 80, host: 8080 + i

      node.vm.provider "vmware_desktop" do |vmware|
        vmware.vmx["displayName"] = "CERBERUS-Node0#{i}"
        vmware.vmx["memsize"] = "1024"
        vmware.vmx["numvcpus"] = "1"
      end

      node.vm.provider "virtualbox" do |vb|
        vb.name = "CERBERUS-Node0#{i}"
        vb.memory = "1024"
        vb.cpus = 1
      end

      node.vm.provision "shell", inline: <<-SHELL
        dnf install -y python3 python3-pip
        cat >> /etc/hosts << 'HOSTS'
192.168.56.10 admin admin.cerberus.local
192.168.56.21 node01 node01.cerberus.local
192.168.56.22 node02 node02.cerberus.local
192.168.56.30 winsrv winsrv.cerberus.local
192.168.56.100 vip vip.cerberus.local
HOSTS
        sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
        systemctl restart sshd
        
        if ! id ansible &>/dev/null; then
          useradd -m -s /bin/bash ansible
          echo "ansible:ansible" | chpasswd
          echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible
        fi
      SHELL
    end
  end

  # Windows Server
  config.vm.define "winsrv" do |winsrv|
    winsrv.vm.box = "gusztavvargadr/windows-server-2022-standard"
    winsrv.vm.hostname = "winsrv"
    winsrv.vm.network "private_network", ip: "192.168.56.30"
    winsrv.vm.network "forwarded_port", guest: 3389, host: 53389
    winsrv.vm.boot_timeout = 1800

    winsrv.vm.communicator = "winrm"
    winsrv.winrm.transport = :plaintext
    winsrv.winrm.basic_auth_only = true
    winsrv.winrm.username = "vagrant"
    winsrv.winrm.password = "vagrant"
    winsrv.winrm.timeout = 3600
    winsrv.winrm.retry_limit = 60
    winsrv.winrm.retry_delay = 10

    winsrv.vm.provider "vmware_desktop" do |vmware|
      vmware.vmx["displayName"] = "CERBERUS-WinSrv"
      vmware.vmx["memsize"] = "2048"
      vmware.vmx["numvcpus"] = "2"
      vmware.gui = true
    end

    winsrv.vm.provider "virtualbox" do |vb|
      vb.name = "CERBERUS-WinSrv"
      vb.memory = "2048"
      vb.cpus = 2
      vb.gui = true
    end

    # Script 1: Configure WinRM for Ansible
    winsrv.vm.provision "shell", path: "scripts/ConfigureRemotingForAnsible.ps1", privileged: true

    # Script 2: Fix IP address for VMware (Last Step!)
    # Attention: Ce script va changer l'IP en arrière-plan après 10 secondes.
    # Vagrant se terminera avec succès avant que la connexion ne coupe.
    winsrv.vm.provision "shell", path: "scripts/fix_ip.ps1", privileged: true, args: "192.168.56.30"

  end

end
