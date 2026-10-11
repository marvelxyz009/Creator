param([int]$Chapter)
# Runs bible -> continuity for one chapter from work/chNN/*.md, approves the edit and publishes chapter-NN.md.
$ErrorActionPreference = 'Stop'
$p = 'dacefb742553477eb6cd299d122bf212'
Set-Location D:\Creator
$proj = "stories\projects\$p"
$T = "$proj\tasks"
$W = "$proj\work\ch{0:D2}" -f $Chapter
$map = [ordered]@{ bible='bible.md'; outline='outline.md'; characters='characters.md'; art='art.md'; draft='draft.md'; edit='edit.md'; continuity='continuity.json' }
$edit = $null
foreach ($s in $map.Keys) {
    py -m story_studio prompt $p $Chapter $s "$W\packet.json" | Out-Null
    if ($LASTEXITCODE) { throw "prompt $s failed" }
    $f = (Get-ChildItem $T | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
    $id = (py -m story_studio submit $p $Chapter $s $f "$W\$($map[$s])") -replace '"', ''
    if ($LASTEXITCODE) { throw "submit $s failed" }
    "$s $id"
    if ($s -eq 'edit') { $edit = $id }
}
py -m story_studio approve $p $edit | Out-Null
if ($LASTEXITCODE) { throw "approve failed" }
py -m story_studio checkpoint $p --chapter $Chapter | Out-Null
py -m story_studio export $p | Out-Null
Remove-Item "$W\packet.json" -ErrorAction SilentlyContinue
Copy-Item "$W\edit.md" ("$proj\chapter-{0:D2}.md" -f $Chapter)
"approved $edit"
