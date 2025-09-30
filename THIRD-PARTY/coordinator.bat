@echo off
REM coordinator_run.bat — wrapper for coordinator.py (calibrate + mark)
setlocal EnableExtensions EnableDelayedExpansion

REM --- Python resolver (python -> py fallback) ---
set "PY=python"
where %PY% >nul 2>&1 || set "PY=py"

REM --- Paths & defaults (edit if needed) ---
set "HERE=%~dp0"
cd /d "%HERE%"
set "MAP=map.png"
set "CALIB=ryl_calib.json"
REM Known world anchors (in order) used during calibration:
set "CAL_POINTS=1724,3353; 1115,2896; 3439,1822"

if not exist "%MAP%" (
  echo [ERROR] "%MAP%" not found in "%HERE%".
  echo Place your map as map.png or change MAP variable inside this .bat.
  pause
  exit /b 1
)

REM --- Mode selection: argument or interactive prompt ---
if /I "%~1"=="CALIB" goto :CALIBRATE

set "COORD=%~1"
if "%COORD%"=="" (
  echo.
  echo Usage:
  echo   %~n0 CALIB                 ^> run calibration (click blue squares in order)
  echo   %~n0 X,Y                   ^> mark coordinate using saved calibration
  echo.
  set /p COORD=Enter coordinate X,Y (or type CALIB to calibrate): 
  if /I "!COORD!"=="CALIB" goto :CALIBRATE
)

REM --- Ensure calibration exists; if not, run it once ---
if not exist "%CALIB%" (
  echo [INFO] No "%CALIB%" found. Starting calibration first...
  call :CALIBRATE
)

REM --- Mark the requested coordinate ---
echo [RUN] Marking (!COORD!) using "%CALIB%" on "%MAP%"
"%PY%" coordinator.py -c "!COORD!" --calib "%CALIB%" -m "%MAP%"
goto :END

:CALIBRATE
echo [RUN] Calibration on "%MAP%"
echo [INFO] Anchors: %CAL_POINTS%
"%PY%" coordinator.py --calibrate "%CAL_POINTS%" -m "%MAP%" -O "%CALIB%"
echo [OK] Saved calibration to "%CALIB%"
goto :END

:END
echo.
echo Done.
pause