<#
.SYNOPSIS
    Converts raw Flowise export files to full ExportData format for import.

.DESCRIPTION
    Flowise "Load Data" (Settings → Load Data) expects the full ExportData format
    with 15 categorized arrays. This script converts raw workflow files and tools
    into that format.

.PARAMETER Path
    Path to a single JSON file or directory containing JSON files.
    Defaults to current directory.

.PARAMETER OutputFile
    Optional output filename. If not specified, generates based on input.

.EXAMPLE
    .\wrap_flowise.ps1 -Path ".\flowise\MyWorkflow.json"
    Converts a single file to ExportData format.

.EXAMPLE
    .\wrap_flowise.ps1 -Path ".\flowise"
    Converts all JSON files in directory, creates combined ExportData file.

.EXAMPLE
    .\wrap_flowise.ps1 -Path ".\flowise" -OutputFile "all-flows.json"
    Converts all files and saves to specified output file.
#>

param(
    [Parameter(Position=0)]
    [string]$Path = ".",

    [Parameter()]
    [string]$OutputFile
)

function New-Guid {
    return [guid]::NewGuid().ToString()
}

function Get-FlowType {
    param([PSCustomObject]$Json)

    foreach ($node in $Json.nodes) {
        if ($node.type -eq "agentFlow" -or $node.type -eq "iteration") {
            return "AGENTFLOW"
        }
    }
    return "CHATFLOW"
}

function Test-IsRawFlowFile {
    param([PSCustomObject]$Json)

    if ($Json.PSObject.Properties.Name -contains "flowData") {
        return $false  # Already wrapped
    }
    if ($Json.PSObject.Properties.Name -contains "func" -and $Json.PSObject.Properties.Name -contains "schema") {
        return $false  # Tool file
    }
    if ($Json.PSObject.Properties.Name -contains "nodes") {
        return $true   # Raw flow file
    }
    return $false
}

function Test-IsToolFile {
    param([PSCustomObject]$Json)

    return ($Json.PSObject.Properties.Name -contains "func" -and
            $Json.PSObject.Properties.Name -contains "schema" -and
            $Json.PSObject.Properties.Name -contains "name")
}

function New-EmptyExportData {
    return [ordered]@{
        AgentFlow = @()
        AgentFlowV2 = @()
        AssistantFlow = @()
        AssistantCustom = @()
        AssistantOpenAI = @()
        AssistantAzure = @()
        ChatFlow = @()
        ChatMessage = @()
        ChatMessageFeedback = @()
        CustomTemplate = @()
        DocumentStore = @()
        DocumentStoreFileChunk = @()
        Execution = @()
        Tool = @()
        Variable = @()
    }
}

function Convert-FlowToExportFormat {
    param(
        [string]$FilePath,
        [PSCustomObject]$Json,
        [string]$Name
    )

    $flowType = Get-FlowType $Json

    # Pretty-print the flowData (matching ExportData.json format)
    $flowData = $Json | ConvertTo-Json -Depth 100

    return @{
        id = New-Guid
        name = $Name
        flowData = $flowData
        type = $flowType
    }
}

function Convert-ToolToExportFormat {
    param([PSCustomObject]$Json)

    # Tool format is already correct, just ensure all fields exist
    return @{
        name = $Json.name
        description = $Json.description
        color = if ($Json.color) { $Json.color } else { "" }
        iconSrc = if ($Json.iconSrc) { $Json.iconSrc } else { "" }
        schema = $Json.schema
        func = $Json.func
    }
}

# Main execution
$resolvedPath = Resolve-Path $Path -ErrorAction SilentlyContinue

if (-not $resolvedPath) {
    Write-Host "Path not found: $Path" -ForegroundColor Red
    exit 1
}

$item = Get-Item $resolvedPath
$exportData = New-EmptyExportData
$processedFiles = @()

if ($item.PSIsContainer) {
    # Directory - process all JSON files
    $jsonFiles = Get-ChildItem -Path $resolvedPath -Filter "*.json" -File

    foreach ($file in $jsonFiles) {
        # Skip already processed files
        if ($file.Name -match "-(wrapped|exportdata)\.json$") {
            Write-Host "Skipping processed file: $($file.Name)" -ForegroundColor Yellow
            continue
        }

        try {
            $json = Get-Content $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
        }
        catch {
            Write-Host "Error parsing $($file.Name): $_" -ForegroundColor Red
            continue
        }

        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)

        if (Test-IsToolFile $json) {
            $tool = Convert-ToolToExportFormat $json
            $exportData.Tool += $tool
            $processedFiles += @{ Name = $baseName; Type = "Tool" }
            Write-Host "Added tool: $baseName" -ForegroundColor Cyan
        }
        elseif (Test-IsRawFlowFile $json) {
            $flow = Convert-FlowToExportFormat -FilePath $file.FullName -Json $json -Name $baseName

            if ($flow.type -eq "AGENTFLOW") {
                $exportData.AgentFlowV2 += $flow
                $processedFiles += @{ Name = $baseName; Type = "AgentFlowV2" }
                Write-Host "Added agentflow: $baseName" -ForegroundColor Green
            }
            else {
                $exportData.ChatFlow += $flow
                $processedFiles += @{ Name = $baseName; Type = "ChatFlow" }
                Write-Host "Added chatflow: $baseName" -ForegroundColor Green
            }
        }
        else {
            Write-Host "Skipping (unknown format): $($file.Name)" -ForegroundColor Gray
        }
    }

    # Determine output filename
    if (-not $OutputFile) {
        $OutputFile = Join-Path $resolvedPath "flowise-import.json"
    }
}
else {
    # Single file
    try {
        $json = Get-Content $resolvedPath -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    catch {
        Write-Host "Error parsing file: $_" -ForegroundColor Red
        exit 1
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($item.Name)
    $directory = [System.IO.Path]::GetDirectoryName($resolvedPath)

    if (Test-IsToolFile $json) {
        $tool = Convert-ToolToExportFormat $json
        $exportData.Tool += $tool
        $processedFiles += @{ Name = $baseName; Type = "Tool" }
        Write-Host "Added tool: $baseName" -ForegroundColor Cyan
    }
    elseif (Test-IsRawFlowFile $json) {
        $flow = Convert-FlowToExportFormat -FilePath $resolvedPath -Json $json -Name $baseName

        if ($flow.type -eq "AGENTFLOW") {
            $exportData.AgentFlowV2 += $flow
            $processedFiles += @{ Name = $baseName; Type = "AgentFlowV2" }
            Write-Host "Added agentflow: $baseName" -ForegroundColor Green
        }
        else {
            $exportData.ChatFlow += $flow
            $processedFiles += @{ Name = $baseName; Type = "ChatFlow" }
            Write-Host "Added chatflow: $baseName" -ForegroundColor Green
        }
    }
    else {
        Write-Host "File is not a raw flow or tool: $($item.Name)" -ForegroundColor Red
        exit 1
    }

    # Determine output filename
    if (-not $OutputFile) {
        $OutputFile = Join-Path $directory "$baseName-exportdata.json"
    }
}

# Check if we have anything to export
$totalItems = $exportData.AgentFlowV2.Count + $exportData.ChatFlow.Count + $exportData.Tool.Count

if ($totalItems -eq 0) {
    Write-Host "`nNo valid files to convert." -ForegroundColor Yellow
    exit 0
}

# Write output file
$exportData | ConvertTo-Json -Depth 100 | Set-Content $OutputFile -Encoding UTF8

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "AgentFlowV2: $($exportData.AgentFlowV2.Count)" -ForegroundColor Green
Write-Host "ChatFlow: $($exportData.ChatFlow.Count)" -ForegroundColor Green
Write-Host "Tool: $($exportData.Tool.Count)" -ForegroundColor Cyan
Write-Host "`nOutput: $OutputFile" -ForegroundColor White
Write-Host "`nImport via: Flowise UI → Settings → Load Data" -ForegroundColor Yellow
