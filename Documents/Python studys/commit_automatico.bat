@echo off

git add .
set DATAHORA=%date% %time%
git commit -m "Commit automático em %DATAHORA%"
git push

pause
