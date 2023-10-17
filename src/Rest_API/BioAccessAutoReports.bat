SET mypath=%~dp0
echo %mypath:~0,-1%
cd %mypath:~0,-1%  >>log.log
python38 BioAccessAutoReports.py >>log.log
python38 GetRecords.py >>log.log
