REM Installation Script for Windows

REM 1. Command Line Python Install
install\python-3.10.8-amd64.exe /passive InstallAllUsers=1 PrependPath=1 Include_test=0 AppendPath=1 DefaultAllUsersTargetDir=C:\PYTHON3

REM 2. Command Line VLC Install
install\vlc-3.0.18-win64.exe /L=1033 /S

REM 3. PATH
setx PATH "C:\Python3;%PROGRAMFILES%\VideoLAN\VLC;%PATH%"
set PATH=%PATH%;C:\Python3

REM 4. PIP stuff: pygame
python -m pip install install\Pillow-8.4.0-cp310-cp310-win_amd64.whl
python -m pip install install\pygame-2.1.2-cp310-cp310-win_amd64.whl

REM 5. Start Item
@echo off
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DMQLaunch.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.WindowStyle = 7 >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\Launch.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.Description = "DMQ Launcher" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs