# PowerShell Snippets for Local Agents

## Safe Path Handling

```powershell
$path = "F:\Example Folder"
Get-ChildItem -LiteralPath $path
```

## UTF-8 Python Output

```powershell
$env:PYTHONIOENCODING = "utf-8"
python script.py
```

## Check If A Port Is Listening

```powershell
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -eq 3000 }
```

## Process Group Memory

```powershell
Get-Process |
  Group-Object ProcessName |
  ForEach-Object {
    $items = $_.Group
    [PSCustomObject]@{
      Name = $_.Name
      Count = $items.Count
      GB = [math]::Round((($items | Measure-Object WorkingSet64 -Sum).Sum / 1GB), 2)
    }
  } |
  Sort-Object GB -Descending |
  Select-Object -First 20
```

## Avoid Newer Syntax When Compatibility Matters

Some Windows PowerShell environments do not support newer syntax. Prefer simple
intermediate variables when a pipeline becomes brittle.
