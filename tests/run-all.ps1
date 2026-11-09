# Ejecuta todas las suites en una copia aislada y resume el estado de cada una.
# Uso: powershell -ExecutionPolicy Bypass -File tests\run-all.ps1 [-ProjectDir <copia>]
#
# Fases:
#   A) arranque musical: exige un savedir virgen y dos procesos encadenados.
#   B) cadena de suites; quest deja el documento que hereda quest_restore.
#   C) ocean_theme aislado.
param(
    [string]$ProjectDir = (Join-Path (Split-Path $PSCommandPath) 'runtime-project\fase1')
)

$runner = Join-Path (Split-Path $PSCommandPath) 'run-one.ps1'
$saves = Join-Path $ProjectDir 'tests\runtime-saves'

function Reset-Savedir {
    Remove-Item -Recurse -Force $saves -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $saves | Out-Null
}

function Invoke-Suite {
    param([string]$Name, [int]$TimeoutSec)
    $output = powershell -ExecutionPolicy Bypass -File $runner -TestCase $Name -ProjectDir $ProjectDir -TimeoutSec $TimeoutSec
    $status = ($output | Where-Object { $_ -match 'Status:' } | Select-Object -First 1)
    if (-not $status) { $status = '(sin status)' }
    $failed = ($output | Where-Object { $_ -match '^\s+FAILED  ' } | ForEach-Object { $_.Trim() }) -join ', '
    '{0,-24} {1} {2}' -f $Name, $status.Trim(), $failed
}

Reset-Savedir
'--- fase A: arranque musical ---'
Invoke-Suite 'music_first_launch' 70
Invoke-Suite 'music_resume_launch' 70

Reset-Savedir
'--- fase B: cadena de suites ---'
$chain = @(
    @{ t = 'quest'; s = 90 },
    @{ t = 'quest_restore'; s = 40 },
    @{ t = 'secondary'; s = 80 },
    @{ t = 'base_rooms'; s = 60 },
    @{ t = 'expanded_worlds'; s = 70 },
    @{ t = 'help_notifications'; s = 60 },
    @{ t = 'illustrated_themes'; s = 70 },
    @{ t = 'options_guide'; s = 70 },
    @{ t = 'reminders'; s = 70 },
    @{ t = 'rename_task'; s = 60 },
    @{ t = 'startup'; s = 60 }
)
foreach ($item in $chain) {
    Invoke-Suite $item.t $item.s
}

Reset-Savedir
'--- fase C: ocean_theme ---'
Invoke-Suite 'ocean_theme' 90
