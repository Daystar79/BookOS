# Midlayer runtime (Windows) — integrity, packs, commits
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root
$py = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $py = "py"; $pyArgs = @("-3") }
else { throw "Python 3 not found" }
if ($py -eq "py") {
  & py -3 -m Framework.midlayer @args
} else {
  & python -m Framework.midlayer @args
}
exit $LASTEXITCODE
