# Windows launcher — prose linter for drafts.
# AI agents on Windows: run this (or: python scripts/run.py lint …).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/windows/lint.ps1 Drafts\

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root

if ($args.Count -lt 1) {
    Write-Error "Usage: lint.ps1 <file_or_directory> [extra linter args...]"
    exit 2
}

function Invoke-PythonScript {
    param([string]$ScriptPath, [string[]]$ScriptArgs)
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 $ScriptPath @ScriptArgs
        return $LASTEXITCODE
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        & python $ScriptPath @ScriptArgs
        return $LASTEXITCODE
    }
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        & python3 $ScriptPath @ScriptArgs
        return $LASTEXITCODE
    }
    throw "Python 3 not found on PATH. Install Python 3 or the Windows py launcher."
}

$script = Join-Path $Root "Framework\linter.py"
$code = Invoke-PythonScript -ScriptPath $script -ScriptArgs $args
exit $code
