@echo off
echo Internet Monitor Installer Builder
echo ===============================
echo.

:: Check if Inno Setup is installed
set "INNO_COMPILER="

:: Try to find Inno Setup in common installation locations
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    set "INNO_COMPILER=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    set "INNO_COMPILER=%ProgramFiles%\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe" (
    set "INNO_COMPILER=%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe"
) else if exist "%ProgramFiles%\Inno Setup 5\ISCC.exe" (
    set "INNO_COMPILER=%ProgramFiles%\Inno Setup 5\ISCC.exe"
)

if "%INNO_COMPILER%"=="" (
    echo ERROR: Inno Setup not found. Please install Inno Setup from https://jrsoftware.org/isdl.php
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

:: Check if the executable exists
if not exist "dist\internetm.exe" (
    echo ERROR: internetm.exe not found in the dist folder.
    echo Please build the executable first using PyInstaller.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

:: Create installer directory if it doesn't exist
if not exist "installer" mkdir installer

echo Building installer using Inno Setup...
echo.

:: Run Inno Setup Compiler
"%INNO_COMPILER%" setup.iss

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to build the installer.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
) else (
    echo.
    echo Installer successfully created in the "installer" folder.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 0
)