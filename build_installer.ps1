# Internet Monitor Installer Builder (PowerShell Version)

Write-Host "Internet Monitor Installer Builder" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Check if Inno Setup is installed
$innoCompiler = $null

# Try to find Inno Setup in common installation locations
$possiblePaths = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 5\ISCC.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $innoCompiler = $path
        break
    }
}

if ($null -eq $innoCompiler) {
    Write-Host "ERROR: Inno Setup not found. Please install Inno Setup from https://jrsoftware.org/isdl.php" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check if the executable exists
if (-not (Test-Path "dist\internetm.exe")) {
    Write-Host "ERROR: internetm.exe not found in the dist folder." -ForegroundColor Red
    Write-Host "Please build the executable first using PyInstaller." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Create installer directory if it doesn't exist
if (-not (Test-Path "installer")) {
    New-Item -Path "installer" -ItemType Directory | Out-Null
}

Write-Host "Building installer using Inno Setup..." -ForegroundColor Green
Write-Host ""

# Run Inno Setup Compiler
try {
    & $innoCompiler "setup.iss"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Installer successfully created in the 'installer' folder." -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "ERROR: Failed to build the installer." -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: An exception occurred while building the installer:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")