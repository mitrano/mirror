@echo off
REM Abre o Mirror no Ubuntu/WSL e executa o Pi

wsl -d Ubuntu -- bash -lc "cd /home/ricardoalvares/repos/mirror && pi"

pause
