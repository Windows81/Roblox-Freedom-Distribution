tasklist /fi "ImageName eq UwAmp.exe" /fo csv 2>NUL | find /I "UwAmp.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM UwAmp.exe /F
tasklist /fi "ImageName eq mysqld.exe" /fo csv 2>NUL | find /I "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM mysqld.exe /F
tasklist /fi "ImageName eq httpd.exe" /fo csv 2>NUL | find /I "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM httpd.exe /F
tasklist /fi "ImageName eq httpd.exe" /fo csv 2>NUL | find /I "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM httpd.exe /F
tasklist /fi "ImageName eq httpd.exe" /fo csv 2>NUL | find /I "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM httpd.exe /F
tasklist /fi "ImageName eq httpd.exe" /fo csv 2>NUL | find /I "httpd.exe">NUL
if "%ERRORLEVEL%"=="0" Taskkill /IM httpd.exe /F
cd Webserver
start /min UwAmp.exe