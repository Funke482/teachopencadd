param([Parameter(Mandatory=$true)][string]$Nr)
$py = Join-Path $HOME "miniforge3\envs\tocadd\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "Runner fehlt. Einmalig: conda create -n tocadd python=3.11 -y; conda activate tocadd; pip install -e ." -ForegroundColor Red
    exit 1
}
& $py (Join-Path $PSScriptRoot "start_talktorial.py") $Nr
