$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Test-Path '.env')) {
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example. Set LLM_PROVIDER and Gemini/Ollama values before using AI.' -ForegroundColor Yellow
}

function New-NexoraVenv {
    if (Test-Path '.venv') { Remove-Item '.venv' -Recurse -Force }
    $created = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.13 -m venv .venv
        if ($LASTEXITCODE -eq 0) { $created = $true }
        if (-not $created) {
            if (Test-Path '.venv') { Remove-Item '.venv' -Recurse -Force }
            py -3.11 -m venv .venv
            if ($LASTEXITCODE -eq 0) { $created = $true }
        }
    }
    if (-not $created) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create .venv. Install Python 3.11 or newer.' }
    }
}

if (-not (Test-Path '.venv\Scripts\python.exe')) { New-NexoraVenv }
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $python -m pip --version *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'The existing virtual environment has a broken pip installation. Recreating it…' -ForegroundColor Yellow
    New-NexoraVenv
    $python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
}

& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'Could not upgrade pip. Delete .venv and run this script again.' }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check your Python version and internet connection.' }
& $python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
