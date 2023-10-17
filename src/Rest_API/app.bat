echo ----------------------------------------------------------------------
echo To deploy the BIOACCESS API open your internet browser and use address
echo             http://localhost:5000/ 
echo -----------------------------------------------------------------------
SET mypath=%~dp0
echo %mypath:~0,-1%
cd %mypath:~0,-1%\
python38 app.py
pause