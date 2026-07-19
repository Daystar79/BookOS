@echo off
setlocal
cd /d "%~dp0..\.."
python -m Framework.midlayer %*
exit /b %ERRORLEVEL%
