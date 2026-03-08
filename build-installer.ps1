#!/usr/bin/env pwsh
<#
  Build Inno Setup Installer for Zoom Auto Scheduler
  This script will:
  1. Build EXE using PyInstaller
  2. Build installer using Inno Setup
#>

# Step 1: Build EXE with PyInstaller
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 1: Building EXE with PyInstaller..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$specFile = Join-Path $projectRoot "ZoomAuto.spec"
$requirementsFile = Join-Path $projectRoot "requirements.txt"

# Prefer project .venv to avoid building with missing dependencies
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$venvPyInstaller = Join-Path $projectRoot ".venv\Scripts\pyinstaller.exe"

if (Test-Path $venvPython) {
    $pythonExe = $venvPython
    Write-Host "Using virtual environment: $venvPython" -ForegroundColor Green
} else {
    $pythonExe = "python"
    Write-Host "Warning: .venv not found, using system Python." -ForegroundColor Yellow
}

if (-not (Test-Path $specFile)) {
    Write-Host "Error: ZoomAuto.spec not found!" -ForegroundColor Red
    exit 1
}

# Ensure required dependencies are available in build environment
Write-Host "Checking build dependencies..." -ForegroundColor Cyan
& $pythonExe -c "import PyQt6, apscheduler, requests, sentry_sdk" 2>$null
if ($LASTEXITCODE -ne 0) {
    if (-not (Test-Path $requirementsFile)) {
        Write-Host "Error: requirements.txt not found at $requirementsFile" -ForegroundColor Red
        exit 1
    }
    Write-Host "Installing requirements into build environment..." -ForegroundColor Yellow
    & $pythonExe -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install requirements." -ForegroundColor Red
        exit 1
    }
}

# Run PyInstaller (prefer .venv executable)
if (Test-Path $venvPyInstaller) {
    & $venvPyInstaller --clean --noconfirm $specFile
} else {
    & $pythonExe -m PyInstaller --clean --noconfirm $specFile
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: PyInstaller build failed!" -ForegroundColor Red
    exit 1
}

# Fail fast if critical runtime modules are not bundled
$warnFile = Join-Path $projectRoot "build\ZoomAuto\warn-ZoomAuto.txt"
if (Test-Path $warnFile) {
    $warn = Get-Content $warnFile -Raw
    if ($warn -match "missing module named 'PyQt6\.QtCore'" -or
        $warn -match "missing module named 'PyQt6\.QtGui'" -or
        $warn -match "missing module named 'PyQt6\.QtWidgets'" -or
        $warn -match "missing module named apscheduler") {
        Write-Host "Error: Critical modules missing in PyInstaller analysis. Aborting release build." -ForegroundColor Red
        exit 1
    }
}
Write-Host "EXE built successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Build Installer with Inno Setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 2: Building Installer with Inno Setup..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$isccPath = $null

# Try common Inno Setup installation paths
$possiblePaths = @(
    'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
    'C:\Program Files\Inno Setup 6\ISCC.exe',
    'C:\Program Files (x86)\Inno Setup 5\ISCC.exe',
    'C:\Program Files\Inno Setup 5\ISCC.exe'
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $isccPath = $path
        Write-Host "Found Inno Setup at: $isccPath" -ForegroundColor Green
        break
    }
}

if (-not $isccPath) {
    Write-Host "Error: Inno Setup not found!" -ForegroundColor Red
    Write-Host "Please download and install from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    exit 1
}

# Compile installer
$issFile = Join-Path $projectRoot "installer.iss"
$outputDir = Join-Path $projectRoot "dist"

if (-not (Test-Path $issFile)) {
    Write-Host "Error: installer.iss not found at $issFile" -ForegroundColor Red
    exit 1
}

Write-Host "Building installer..." -ForegroundColor Cyan
& $isccPath $issFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Installer built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output files:" -ForegroundColor Cyan
    Get-ChildItem "$outputDir\ZoomAuto-Setup-*.exe" | ForEach-Object { Write-Host "  - $($_.Name)" }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test the installer"
    Write-Host "2. Upload to GitHub Releases"
} else {
    Write-Host "Error: Build failed!" -ForegroundColor Red
    exit 1
}
