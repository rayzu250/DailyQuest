# Prepara el diseño aprobado como icono estático adaptable, sin redibujarlo.
Add-Type -AssemblyName System.Drawing
$root = Split-Path $PSScriptRoot -Parent
$source = [Drawing.Image]::FromFile((Join-Path $root 'art/android/dailyquest-icon-concept.png'))
try {
    $background = [Drawing.Bitmap]::new(1080, 1080)
    $graphics = [Drawing.Graphics]::FromImage($background)
    try {
        $graphics.Clear([Drawing.ColorTranslator]::FromHtml('#00391B'))
        $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        # El arte queda dentro de la zona central para conservar cuaderno y estrella.
        $graphics.DrawImage($source, [Drawing.Rectangle]::new(108, 108, 864, 864))
        $background.Save((Join-Path $root 'android-icon_background.png'), [Drawing.Imaging.ImageFormat]::Png)
    } finally { $graphics.Dispose(); $background.Dispose() }
    $foreground = [Drawing.Bitmap]::new(1080, 1080, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        $foreground.Save((Join-Path $root 'android-icon_foreground.png'), [Drawing.Imaging.ImageFormat]::Png)
    } finally { $foreground.Dispose() }
} finally { $source.Dispose() }
