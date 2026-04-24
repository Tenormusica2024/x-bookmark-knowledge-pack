param(
  [Parameter(Mandatory = $true)][string]$InputJson,
  [Parameter(Mandatory = $true)][string]$OutputDir,
  [string]$PublishDir,
  [switch]$NoHtml,
  [string]$Title = 'X Bookmark Knowledge Pack',
  [string]$Subtitle = 'Portable local bookmark bundle for humans and AI agents'
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$PythonScript = Join-Path $ScriptDir 'refresh_bundle.py'

$Args = @(
  $PythonScript,
  $InputJson,
  $OutputDir,
  '--title', $Title,
  '--subtitle', $Subtitle
)

if ($PublishDir) {
  $Args += @('--publish-dir', $PublishDir)
}
if ($NoHtml) {
  $Args += '--no-html'
}

Push-Location $RepoRoot
try {
  & python @Args
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
