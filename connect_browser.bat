@echo off
set  "userpath= %SYSTEMDRIVE%%HOMEPATH%"
set "user_dir_path=%SYSTEMDRIVE%%HOMEPATH%\PlaywrightDataDir"
@REM 地址需要手动指定
%userpath%\AppData\Local\ms-playwright\chromium-1140\chrome-win\chrome.exe --remote-debugging-port=9222 --user-data-dir=%user_dir_path%

