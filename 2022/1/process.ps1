
$calories = Get-Content ./input.txt

$elves = @()
$elf = 0
$elves += 0

foreach ($c in $calories) {
    if ($c -eq '') {
        $elf++
        $elves += 0
    }

    $elves[$elf] += $c

}
Write-Host "Calories carried by elf with the most:"
$elves |Sort-Object | Select-Object -last 1

Write-Host "Calories carried by the 3 elves with the most:"
($elves |Sort-Object |Select-Object -last 3 |Measure-Object -Sum).Sum