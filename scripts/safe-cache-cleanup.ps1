param(
  [switch]$Execute,
  [switch]$IncludeRecycleBin
)

$targets = @(
  "$env:TEMP",
  "$env:LOCALAPPDATA\Temp",
  "$env:LOCALAPPDATA\pip\Cache",
  "$env:LOCALAPPDATA\npm-cache",
  "$env:LOCALAPPDATA\NVIDIA\DXCache",
  "$env:LOCALAPPDATA\NVIDIA\GLCache"
)

if ($IncludeRecycleBin) {
  $targets += "$env:SystemDrive\`$Recycle.Bin"
}

$targets = $targets | Select-Object -Unique

foreach ($target in $targets) {
  if (-not (Test-Path -LiteralPath $target)) {
    continue
  }

  $size = 0
  Get-ChildItem -LiteralPath $target -Force -Recurse -ErrorAction SilentlyContinue |
    ForEach-Object {
      if (-not $_.PSIsContainer) { $size += $_.Length }
    }

  $gb = [math]::Round($size / 1GB, 2)
  Write-Host "Target: $target"
  Write-Host "Approx size: $gb GB"

  if ($Execute) {
    Get-ChildItem -LiteralPath $target -Force -ErrorAction SilentlyContinue |
      Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cleaned."
  } else {
    Write-Host "Dry run only. Add -Execute to remove files."
  }
  Write-Host ""
}
