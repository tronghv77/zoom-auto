#!/usr/bin/env pwsh
<#
  Build Inno Setup Installer for Zoom Auto Scheduler
  Run this after installing Inno Setup
#>

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
$issFile = "D:\Projects\zoom-auto\installer.iss"
$outputDir = "D:\Projects\zoom-auto\dist"

if (-not (Test-Path $issFile)) {
    Write-Host "Error: installer.iss not found at $issFile" -ForegroundColor Red
    exit 1
}

Write-Host "Building installer..." -ForegroundColor Cyan
& $isccPath $issFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Installer built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output files:" -ForegroundColor Cyan
    Get-ChildItem "$outputDir\ZoomAuto-Setup-*.exe" | ForEach-Object { Write-Host "  - $($_.Name)" }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test the installer by running: $outputDir\ZoomAuto-Setup-*.exe"
    Write-Host "2. Upload to GitHub Releases"
    Write-Host "3. Update version in version.py for next build"
} else {
    Write-Host "Error: Build failed!" -ForegroundColor Red
    exit 1
}
