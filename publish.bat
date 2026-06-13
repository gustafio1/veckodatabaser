@echo off
REM Publicerar Veckodatabaser till GitHub Pages.
REM Dubbelklicka, eller lat Windows Task Scheduler kora filen efter veckokorningen.
cd /d "%~dp0"

git add -A
git diff --cached --quiet
if %errorlevel%==0 (
  echo Inga andringar att publicera.
) else (
  git commit -m "Veckouppdatering %date%"
  git push
  echo Klart - sidan ar publicerad.
)
pause
