..\venv\Scripts\activate.ps1
Remove-Item -Path .\source -Recurse
sphinx-apidoc.exe -o .\source ..\idoitapi --full -a --separate -H "i-doit_API" -A "Martin Vorländer" -R "1.0b7"
$From = Get-Content -Path .\sphinx-init.py
Add-Content -Path source\conf.py $From
Remove-Item -Path .\build -Recurse
sphinx-build.exe -M html .\source .\build
