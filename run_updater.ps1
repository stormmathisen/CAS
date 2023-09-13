$env:EPICS_CA_ADDR_LIST = "192.168.83.246"
$env:EPICS_CA_SERVER_PORT = "6020"
Start-Job -Name "updater" -ScriptBlock { python .\test\temp_updater.py }