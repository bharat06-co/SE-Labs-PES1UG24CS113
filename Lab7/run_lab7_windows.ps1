# Run from Windows PowerShell after extracting the Lab7 folder.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -Path 'evidence' -ItemType Directory -Force | Out-Null

py -m pip install -r requirements.txt reportlab pillow
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }

Write-Host 'Running original application...'
"medium:6`n3,6,12`n2400|200" | py baseline/processor.py | Out-File -Encoding utf8 evidence/original_program_windows.txt

Write-Host 'Running the Hypothesis tests on original code (failures expected)...'
Copy-Item processor.py processor_fixed_backup.py -Force
try {
    Copy-Item baseline/processor.py processor.py -Force
    cmd /c 'py -m pytest -q test_processor.py --tb=short --color=no > evidence\baseline_hypothesis_results.txt 2>&1'
    $baselineExit = $LASTEXITCODE
}
finally {
    Move-Item processor_fixed_backup.py processor.py -Force
}
if ($baselineExit -eq 0) { throw 'Original source unexpectedly passed; inspect the tests.' }
if (-not (Select-String -Path evidence/baseline_hypothesis_results.txt -Pattern 'failed' -Quiet)) { throw 'The baseline failed for an unexpected reason; inspect the log.' }

Write-Host 'Running corrected application...'
"medium:6`n3,6,12`n2400|200" | py processor.py | Out-File -Encoding utf8 evidence/corrected_program_windows.txt

Write-Host 'Running the Hypothesis tests on corrected code...'
cmd /c 'py -m pytest -q test_processor.py --tb=short --color=no > evidence\final_hypothesis_results.txt 2>&1'
$finalExit = $LASTEXITCODE
if ($finalExit -ne 0) {
    Get-Content evidence/final_hypothesis_results.txt
    throw 'Final Hypothesis tests failed.'
}

Write-Host 'Building the final consolidated report...'
py build_lab7_report.py
if ($LASTEXITCODE -ne 0) { throw 'PDF generation failed.' }

Write-Host ''
Get-Content evidence/baseline_hypothesis_results.txt | Select-Object -Last 5
Get-Content evidence/final_hypothesis_results.txt | Select-Object -Last 5
Write-Host ''
Write-Host 'Final PDF: Lab7_Fuzz_Testing_Report.pdf'
