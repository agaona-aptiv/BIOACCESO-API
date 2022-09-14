SET mypath=%~dp0
SETLOCAL
set file=%0
FOR %%i IN ("%file%") DO (
SET host=%%~ni
)
echo CD %mypath:~0,-1%
cd %mypath:~0,-1%
ECHO executing %host%
python3 %host%.py
pause