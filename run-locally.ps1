# Start PowerShell in admin mode and run: .\run-locally.ps1 to run locally
Start-Process -FilePath "C:\Windows\System32\cmd.exe" -verb runas -ArgumentList {/k python3.8 -u src/main.py 0}
Start-Process -FilePath "C:\Windows\System32\cmd.exe" -verb runas -ArgumentList {/k python3.8 -u src/main.py 1}
Start-Process -FilePath "C:\Windows\System32\cmd.exe" -verb runas -ArgumentList {/k python3.8 -u src/main.py 2}