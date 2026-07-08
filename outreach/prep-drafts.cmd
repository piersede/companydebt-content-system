@echo off
REM On-demand: prep today's outreach drafts and open the review page.
REM Runs scan in write mode (drafts -> outbox/*.eml + board rows -> "Ready to contact"),
REM builds the review page, and opens it. Never sends. Double-click, or ask Claude to run it.
setlocal
cd /d "%~dp0"
set "OUTREACH_REVIEW=write"
"C:\Program Files\nodejs\node.exe" conductor.js scan --process
"C:\Program Files\nodejs\node.exe" build-review.js
start "" "%~dp0outbox\drafts.html"
endlocal
