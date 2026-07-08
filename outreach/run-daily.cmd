@echo off
REM CompanyDebt outreach — daily scheduled run (auto-draft, human-send; never sends email).
REM Runs scan in WRITE mode so drafts land on the Monday board as "Ready to contact".
REM Manual runs stay in print mode by default; only this scheduled wrapper sets write.

setlocal
set "HERE=%~dp0"
cd /d "%HERE%"
if not exist "state\logs" mkdir "state\logs"

set "OUTREACH_REVIEW=write"
for /f "tokens=1-3 delims=/- " %%a in ("%date%") do set "STAMP=%%c-%%b-%%a"

"C:\Program Files\nodejs\node.exe" conductor.js scan --process >> "state\logs\daily-%STAMP%.log" 2>&1
endlocal
