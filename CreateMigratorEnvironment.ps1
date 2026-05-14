# Create env file for genrevive
$genreviveDir = $PSScriptRoot

$envContent = @"

# Monitoring and Evaluation of your application
LANGFUSE_TRACING=false 
LANGFUSE_PUBLIC_KEY=`""`
LANGFUSE_SECRET_KEY=`""`
LANGFUSE_AUTH=`""`

#open telemetry headers and endpoint
OTEL_EXPORTER_OTLP_HEADERS=`""`
OTEL_EXPORTER_OTLP_ENDPOINT=`"http://localhost:3005/api/public/otel"`
# Disable OpenTelemetry
OTEL_SDK_DISABLED=true

# Enable/Disable Training Mode
TRAINING_MODE=false
TRAINING_ITERATIONS=1

# Logging
LOG_PATH=`"./logfile.log"`

WHITELISTED_PATHS=`"`${TARGET_PROJECT_PATH}, `${LOCAL_TARGET_PROJECT_PATH}"` 

# Context (Used for agent creation)
ORIGIN_TECHNOLOGY=`"Java Swing"`
TARGET_TECHNOLOGY=`"Angular TypeScript"`
ORIGIN_INPUT=`"Swing MVP files"`
TARGET_OUTPUT=`"Angular components"`
COMPILER_TECHNOLOGY=`"Angular CLI"`

# Inputs (Use specific variable names)
SWING_PROJECT_PATH=`"$genreviveDir/input/websocket_swing"`

# Outputs (Use specific variable names)
ANGULAR_APP_NAME=demo-angular-app
NODE_MODULES_PATH=`"`${ANGULAR_PROJECT_PATH}/node_modules"`

# Shell execution
USE_SHELL=false

#Executes the ng build either locally or in a Docker container
USE_LOCAL_NPM=True

#Deleting the old anular project {ANGULAR_APP_NAME}
DELETING_OUTPUT=True

OPENAPI_FILE_PATH="`${SWING_PROJECT_PATH}/api.yml"

####################################################################################################################################
#
# If Docker/Rancher is used the /home paths have to be used. If the migrator will run locally, set the paths same as the local paths
#
####################################################################################################################################
#ORIGIN_PROJECT_PATH = "/home/migrator/origin"
ORIGIN_PROJECT_PATH = `${SWING_PROJECT_PATH}
LOCAL_ORIGIN_PROJECT_PATH = `${SWING_PROJECT_PATH}

#TARGET_PROJECT_PATH = "/home/migrator/target"
TARGET_PROJECT_PATH = "$genreviveDir/output"
LOCAL_TARGET_PROJECT_PATH = `${TARGET_PROJECT_PATH}

#ANGULAR_PROJECT_PATH = "/home/migrator/target/demo-angular-app"
ANGULAR_PROJECT_PATH = `${TARGET_PROJECT_PATH}/`${ANGULAR_APP_NAME}
LOCAL_ANGULAR_PROJECT_PATH = `${ANGULAR_PROJECT_PATH}

LOCAL_GENREVIVE_PATH = "$genreviveDir/genrevive"
"@

$migratorDir = "$genreviveDir\migrator"

# Save the env content
$envFilePath = "$migratorDir\.env"
Set-Content -Path $envFilePath -Value $envContent -Force
Write-Host "env file created at $envFilePath" -ForegroundColor Cyan
#Get-Content -Path $envFilePath

# create output folder
$outputDir = "$genreviveDir\output"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Get the latest file version of genrevive
$latestGenRevive = Get-ChildItem -Path "$genreviveDir\genrevive\*.tar.gz" | Sort-Object Name -Descending | Select-Object -First 1 | Select-Object -ExpandProperty Name
Write-Host "Latest genrevive file found: $latestGenRevive" -ForegroundColor Cyan

# adapt the project toml
$projectTomlPath = "$migratorDir\pyproject.toml"
if (Test-Path -Path $projectTomlPath) {
    Write-Host "pyproject.toml found at $projectTomlPath. Updating genrevive version..." -ForegroundColor Cyan
    $newEntry = "genrevive = { path = `"../genrevive/$latestGenRevive`", develop = false }"
    (Get-Content -Path $projectTomlPath) -replace '^genrevive\s*=.*', $newEntry | 
                                            Set-Content -Path $projectTomlPath -Encoding utf8
    Write-Host "pyproject.toml updated with most recent genrevive version." -ForegroundColor Cyan
} else {
    Write-Host "pyproject.toml not found at $projectTomlPath. Please check the path and try again." -ForegroundColor Red
}

# Retrieve llm api key from vault
Set-PSRepository -Name "PSGallery" -InstallationPolicy Trusted

Connect-AzAccount

$agentModel = (Get-AzAppConfigurationKeyValue -Endpoint https://app-conf-devbox.azconfig.io -Key "agent_model").Value
if ([string]::IsNullOrEmpty($agentModel)) {
    Write-Error "No AGENT_MODEL could be retrieved from azure app config."
    exit    
}

$apiKey = Get-AzKeyVaultSecret -VaultName "kv-appmod-devbox" -Name "genrevive-migrator-key" -AsPlainText
if ([string]::IsNullOrEmpty($apiKey)) {
    Write-Error "No API_KEY could be retrieved from azure app config."
    exit
}

$apiVersion = (Get-AzAppConfigurationKeyValue -Endpoint https://app-conf-devbox.azconfig.io -Key "azure_api_version").Value
if ([string]::IsNullOrEmpty($apiVersion)) {
    Write-Error "No API_VERSION could be retrieved from azure app config."
    exit    
}

$azureEndpoint = (Get-AzAppConfigurationKeyValue -Endpoint https://app-conf-devbox.azconfig.io -Key "azure_endpoint").Value
if ([string]::IsNullOrEmpty($azureEndpoint)) {
    Write-Error "No AZURE_ENDPOINT could be retrieved from azure app config."
    exit    
}

$llmProvider = (Get-AzAppConfigurationKeyValue -Endpoint https://app-conf-devbox.azconfig.io -Key "llm_provider").Value
if ([string]::IsNullOrEmpty($llmProvider)) {
    Write-Error "No LLM_PROVIDER could be retrieved from azure app config."
    exit    
}

# Set env variables only in the scope of this powershell process
[System.Environment]::SetEnvironmentVariable("AGENT_MODEL", $agentModel, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("AZURE_API_KEY", $apiKey, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("AZUE_API_VERSION", $apiVersion, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("AZURE_ENDPOINT", $azureEndpoint, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("LLM_PROVIDER", $llmProvider, [System.EnvironmentVariableTarget]::Process)

# Create the virtual environment for the migrator
$venvPath = "$migratorDir\venv"

cd $migratorDir

if (-not (Test-Path -Path $venvPath)) {
    Write-Host "No venv found. Create new and install dependencies..." -ForegroundColor Cyan
    py -m venv venv
    .\venv\Scripts\activate
    poetry lock
    poetry install
}
else {
    Write-Host "Venv found. Activate..." -ForegroundColor Cyan
    .\venv\Scripts\activate
}

# Run Migrator
Write-Host "Start Migration..." -ForegroundColor Cyan
py main.py

# Run Result
Write-Host "Start angular dev server..." -ForegroundColor Cyan
cd $outputDir\demo-angular-app
ng serve & Start-Process "msedge.exe" "http://localhost:4200"