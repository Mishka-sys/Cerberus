# ConfigureRemotingForAnsible.ps1
# Based on GOAD project - Simple WinRM configuration

Write-Host "=== Configuring WinRM for Ansible ==="

# Set WinRM service to start automatically
Set-Service -Name "WinRM" -StartupType Automatic
Start-Service -Name "WinRM"

# Configure WinRM
winrm quickconfig -q
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'

# Firewall rules for WinRM
netsh advfirewall firewall add rule name="WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow 2>$null
netsh advfirewall firewall add rule name="WinRM-HTTPS" dir=in localport=5986 protocol=TCP action=allow 2>$null
netsh advfirewall firewall add rule name="WinRM-HTTP-Any" dir=in localport=5985 protocol=TCP action=allow profile=any 2>$null

# Force Network Category to Private (Fixes Public Network blocking WinRM)
Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private

Write-Host "WinRM configured successfully."
