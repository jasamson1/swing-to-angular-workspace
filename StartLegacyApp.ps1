<#
    StartLegacyApp.ps1
    - Builds runtime classpath via Maven
    - Compiles the project
    - Launches Java with the generated classpath
#>
Set-Location "$PSScriptRoot\input\websocket_swing"

# ---------------- CONFIG ----------------
# Main class (package-qualified)
$MainClass = "com.Main"

# JDK to use (match VS Code's, if you want the same)
# Example Zulu 25 (adjust to your path)
$JavaExe  = "C:\Program Files\Zulu\zulu-25\bin\java.exe"

# Maven goals
$MavenCompileGoal = "compile"   # or "package" if you want to build a jar
# ---------------------------------------

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Err ($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# 1) Verify java/mvn
if (-not (Test-Path $JavaExe)) {
    Write-Err "Java not found at '$JavaExe'. Adjust `$JavaExe` to your JDK."
    exit 1
}
if (-not (Get-Command mvn -ErrorAction SilentlyContinue)) {
    Write-Err "Maven (mvn) is not on PATH. Install Maven or add it to PATH."
    exit 1
}

# 2) Generate runtime classpath via Maven
#    Writes the classpath into a file we can read
$mdepOutput = Join-Path $PWD ".mvn-runtime-cp.txt"
Write-Info "Building runtime classpath via Maven…"
$mvnArgs = @(
    "dependency:build-classpath",
    "-q",
    "-DincludeScope=runtime",
    "-Dmdep.outputFile=$mdepOutput"
)
# You can also add -DexcludeTransitive=false if needed
$mvnProc = Start-Process -FilePath "mvn" -ArgumentList $mvnArgs -NoNewWindow -PassThru -Wait
if ($mvnProc.ExitCode -ne 0 -or -not (Test-Path $mdepOutput)) {
    Write-Err "Failed to build classpath via Maven."
    exit 1
}

# Read the runtime classpath string (Windows separator is ;)
$runtimeCp = Get-Content $mdepOutput -Raw
Write-Info "Runtime CP entries: $((($runtimeCp -split ';').Count))"

# 3) Compile project
Write-Info "Compiling project: mvn $MavenCompileGoal…"
$mvnProc2 = Start-Process -FilePath "mvn" -ArgumentList @($MavenCompileGoal, "-DskipTests") -NoNewWindow -PassThru -Wait
if ($mvnProc2.ExitCode -ne 0) {
    Write-Err "Maven $MavenCompileGoal failed."
    exit 1
}

# 4) Compute final classpath = target\classes + runtime deps
$targetClasses = Join-Path $PWD "swing\target\classes"
if (-not (Test-Path $targetClasses)) {
    Write-Err "$targetClasses not found. Are you in the project root? Did compile succeed?"
    exit 1
}
$finalCp = "$targetClasses;$runtimeCp"

# 5) Launch app (use quotes to handle umlauts/spaces in paths)
Write-Info "Starting $MainClass…"
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName  = $JavaExe
$psi.Arguments = "-XX:+ShowCodeDetailsInExceptionMessages -cp `"$finalCp`" $MainClass"
$psi.UseShellExecute        = $false
$psi.RedirectStandardOutput = $false
$psi.RedirectStandardError  = $false

$p = [System.Diagnostics.Process]::Start($psi)
$p.WaitForExit()
$exit = $p.ExitCode

if ($exit -eq 0) { Write-Info "Application exited successfully." }
else { Write-Err "Application exited with code $exit." }

exit $exit