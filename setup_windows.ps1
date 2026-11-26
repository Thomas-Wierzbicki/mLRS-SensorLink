# mLRS-SensorLink Windows setup, GPL-3.0.
# Run from any directory. No flashing, source pull or automatic Git commit.
[CmdletBinding()]
param(
    [string]$PythonPath = (Join-Path $env:USERPROFILE '.platformio\penv\Scripts\python.exe')
)
$ErrorActionPreference = 'Stop'
$ProjectRoot = $PSScriptRoot

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed (exit $LASTEXITCODE): $Program $($Arguments -join ' ')"
    }
}

try {
    if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
        throw "PlatformIO Python fehlt: $PythonPath. PlatformIO IDE in VS Code installieren und die Einrichtung abwarten."
    }
    foreach ($item in @('platformio.ini', '.git', 'run_setup.py', 'requirements-setup.txt')) {
        if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $item))) {
            throw "Fehlt im Projektordner: $item. Paket in das geklonte Repository entpacken."
        }
    }
    $null = Get-Command git -ErrorAction Stop
    # No PATH lookup of python; Anaconda/Windows aliases do not choose the interpreter.
    Write-Host "Projekt: $ProjectRoot"
    Write-Host "Python:  $PythonPath"
    Invoke-Checked -Program $PythonPath -Arguments @('-m', 'pip', 'install', '-r', (Join-Path $ProjectRoot 'requirements-setup.txt'))
    Invoke-Checked -Program $PythonPath -Arguments @('-c', 'import sys, em, dronecan, pexpect, lxml.etree, intelhex; print(sys.executable)')
    Invoke-Checked -Program $PythonPath -Arguments @((Join-Path $ProjectRoot 'run_setup.py'), '--nopause')
    Write-Host ''
    Write-Host 'FERTIG: Abhaengigkeiten und Generator-Dateien eingerichtet.' -ForegroundColor Green
    Write-Host 'Jetzt das gewuenschte PlatformIO-Target in VS Code bauen.'
    exit 0
}
catch {
    Write-Host "SETUP FEHLGESCHLAGEN: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
