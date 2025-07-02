@echo off
REM Script para commit automático no Git

REM Adiciona todos os arquivos alterados
git add .

REM Cria um commit com data e hora atuais
set DATAHORA=%date% %time%
git commit -m "Commit automático em %DATAHORA%"

REM Envia para o repositório remoto
git push

pause
