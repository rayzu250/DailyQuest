# Ejecuta un testcase de Ren'Py con timeout duro y captura la salida en out.log.
# Uso: powershell -ExecutionPolicy Bypass -File tests\run-one.ps1 "quest::data_integrity" [-ProjectDir <copia aislada>]
param(
    [Parameter(Mandatory=$true)][string]$TestCase,
    [string]$ProjectDir = (Split-Path $PSCommandPath),
    [int]$TimeoutSec = 180
)
$sdkParent = (Resolve-Path (Join-Path $ProjectDir '..\..\..\..\..\')).Path
$python = Join-Path $sdkParent 'lib\py3-windows-x86_64\python.exe'
$renpy = Join-Path $sdkParent 'renpy.py'
$q = [char]34
$out = Join-Path $ProjectDir 'out.log'
$err = Join-Path $ProjectDir 'err.log'
Remove-Item $out, $err -ErrorAction SilentlyContinue
$renpyArgs = $q + $renpy + $q + ' ' + $q + '.' + $q + ' test ' + $TestCase + ' --savedir tests\runtime-saves --report-detailed --overwrite-screenshots'
$p = Start-Process -FilePath $python -ArgumentList $renpyArgs -WorkingDirectory $ProjectDir -PassThru -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError $err
if (-not $p.WaitForExit($TimeoutSec * 1000)) {
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
    Write-Host 'KILLED-TIMEOUT'
} else {
    ('exit=' + $p.ExitCode)
}
Get-Content $out -ErrorAction SilentlyContinue | Select-String -Pattern 'PASSED|FAILED|Status:|AssertionError|Exception' | Select-Object -First 25 | ForEach-Object { $_.Line }
