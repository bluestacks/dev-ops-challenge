


$Line = (Get-Content -Path 'Desktop\logfile.log') ##sourcepath
$ip = ($Line  |  Select-String -Pattern "\d{1,3}(\.\d{1,3}){3}" -AllMatches).Matches.Value 
$ip | Group-Object | Sort-Object -Property Count -Descending | Select-Object -first 8 | ft Name,count


