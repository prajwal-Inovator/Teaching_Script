# run_tests.ps1
# One-shot pipeline: regenerate the ANTLR parser, then run every test.
# IMPORTANT: run this from the project root directory.

$ErrorActionPreference = "Stop"

Write-Host "Step 1: Activate virtual environment (if present)" -ForegroundColor Cyan
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "No .venv found - using the current Python interpreter." -ForegroundColor Yellow
}

Write-Host "Step 2: Regenerate ANTLR parser" -ForegroundColor Cyan
.\generate_parser.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Parser generation failed. Aborting." -ForegroundColor Red
    exit 1
}

Write-Host "Step 3: Run the test suite" -ForegroundColor Cyan
python -m pytest -v
exit $LASTEXITCODE
