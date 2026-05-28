param(
  [int]$Top = 20,
  [string[]]$ExcludeNames = @()
)

$processes = Get-Process | Where-Object {
  $ExcludeNames -notcontains $_.ProcessName
}

$groups = $processes |
  Group-Object ProcessName |
  ForEach-Object {
    $items = $_.Group
    [PSCustomObject]@{
      Name = $_.Name
      Count = $items.Count
      WorkingSetGB = [math]::Round((($items | Measure-Object WorkingSet64 -Sum).Sum / 1GB), 2)
      PrivateMemoryGB = [math]::Round((($items | Measure-Object PrivateMemorySize64 -Sum).Sum / 1GB), 2)
    }
  } |
  Sort-Object WorkingSetGB -Descending |
  Select-Object -First $Top

$groups | Format-Table -AutoSize
