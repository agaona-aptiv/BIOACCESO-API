SET mypath=%~dp0
echo %mypath:~0,-1%
cd %mypath:~0,-1%  >>log.log
python38 post_lost_users.py >>log.log