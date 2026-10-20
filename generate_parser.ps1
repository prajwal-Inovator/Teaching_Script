# generate_parser.ps1
# Regenerates the ANTLR Python lexer, parser and visitor for TeachingScript.
# Run from the project root in PowerShell.

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $Root

$Jar = "antlr-4.13.2-complete.jar"
if (-not (Test-Path $Jar)) {
    Write-Host "ERROR: $Jar not found in $Root" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "generated")) {
    New-Item -ItemType Directory -Path "generated" | Out-Null
}

Write-Host "Cleaning old generated files..." -ForegroundColor Cyan
Get-ChildItem -Path "generated" -Filter "TeachingScript*" -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host "Running ANTLR4 (Python3 target, visitor, no listener)..." -ForegroundColor Cyan
java -jar $Jar -Dlanguage=Python3 -visitor -no-listener -o generated `
    TeachingScriptLexer.g4 TeachingScriptParser.g4

if ($LASTEXITCODE -ne 0) {
    Write-Host "ANTLR generation FAILED." -ForegroundColor Red
    exit 1
}

Write-Host "Generated files:" -ForegroundColor Green
Get-ChildItem generated | Format-Table Name, Length