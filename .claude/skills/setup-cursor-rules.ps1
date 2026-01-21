# setup-cursor-rules.ps1
# Converts n8n-skills to Cursor MDC format rules
#
# Usage: 
#   .\setup-cursor-rules.ps1 -TargetProject "C:\path\to\your\n8n-project"
#   .\setup-cursor-rules.ps1  # Uses current directory

param(
    [string]$TargetProject = ".",
    [switch]$IncludeReferences = $false,
    [switch]$AlwaysApply = $false
)

$ErrorActionPreference = "Stop"

# Find skills directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsPath = Join-Path $scriptDir "n8n-mcp-skills-v1.0.0\skills"

if (-not (Test-Path $skillsPath)) {
    Write-Error "Skills directory not found at: $skillsPath"
    exit 1
}

# Create target rules directory
$rulesPath = Join-Path $TargetProject ".cursor\rules"
New-Item -ItemType Directory -Force -Path $rulesPath | Out-Null
Write-Host "Creating rules in: $rulesPath" -ForegroundColor Cyan

# Skill definitions with descriptions for semantic matching
$skills = @(
    @{
        name = "n8n-expression-syntax"
        desc = "n8n expression syntax, {{}} double curly braces, `$json variables, `$node references, webhook body data access, `$now datetime, `$env environment variables"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**")
    },
    @{
        name = "n8n-mcp-tools-expert"
        desc = "n8n-mcp MCP server tools, search_nodes, get_node, validate_node, validate_workflow, n8n_create_workflow, n8n_update_partial_workflow, template search, nodeType format"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**")
    },
    @{
        name = "n8n-workflow-patterns"
        desc = "n8n workflow patterns, webhook processing, HTTP API integration, database sync, AI agent workflows, scheduled tasks, workflow architecture"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**")
    },
    @{
        name = "n8n-validation-expert"
        desc = "n8n validation errors, validation profiles, false positives, auto-sanitization, error interpretation, fixing validation failures"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**")
    },
    @{
        name = "n8n-node-configuration"
        desc = "n8n node configuration, property dependencies, operation-specific settings, AI connection types, conditional fields"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**")
    },
    @{
        name = "n8n-code-javascript"
        desc = "n8n Code node JavaScript, `$input.all, `$input.first, `$json, `$helpers.httpRequest, return format, webhook body gotcha, built-in functions"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**", "*.js")
    },
    @{
        name = "n8n-code-python"
        desc = "n8n Code node Python, _input, _json, standard library only, no external packages, Python limitations in n8n"
        globs = @("*.json", "workflows/**/*.json", "**/n8n/**", "*.py")
    }
)

# Reference files to include if requested
$referenceFiles = @{
    "n8n-expression-syntax" = @("COMMON_MISTAKES.md", "EXAMPLES.md")
    "n8n-mcp-tools-expert" = @("SEARCH_GUIDE.md", "VALIDATION_GUIDE.md", "WORKFLOW_GUIDE.md")
    "n8n-workflow-patterns" = @("webhook_processing.md", "http_api_integration.md", "database_operations.md", "ai_agent_workflow.md", "scheduled_tasks.md")
    "n8n-validation-expert" = @("ERROR_CATALOG.md", "FALSE_POSITIVES.md")
    "n8n-node-configuration" = @("DEPENDENCIES.md", "OPERATION_PATTERNS.md")
    "n8n-code-javascript" = @("DATA_ACCESS.md", "COMMON_PATTERNS.md", "ERROR_PATTERNS.md", "BUILTIN_FUNCTIONS.md")
    "n8n-code-python" = @("DATA_ACCESS.md", "COMMON_PATTERNS.md", "ERROR_PATTERNS.md", "STANDARD_LIBRARY.md")
}

function Convert-ToMDC {
    param(
        [string]$SourceFile,
        [string]$Description,
        [string[]]$Globs,
        [bool]$Always = $false
    )
    
    if (-not (Test-Path $SourceFile)) {
        return $null
    }
    
    # Read content
    $content = Get-Content $SourceFile -Raw -Encoding UTF8
    
    # Remove existing YAML frontmatter if present
    if ($content -match "(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n") {
        $content = $content -replace "(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n", ""
    }
    
    # Build globs string
    $globsJson = ($Globs | ForEach-Object { "`"$_`"" }) -join ", "
    
    # Build frontmatter
    $frontmatter = @"
---
description: $Description
globs: [$globsJson]
"@
    
    if ($Always) {
        $frontmatter += "`nalwaysApply: true"
    }
    
    $frontmatter += "`n---`n`n"
    
    return $frontmatter + $content.TrimStart()
}

$createdFiles = @()

foreach ($skill in $skills) {
    $skillDir = Join-Path $skillsPath $skill.name
    $skillFile = Join-Path $skillDir "SKILL.md"
    
    if (Test-Path $skillFile) {
        # Convert main skill file
        $mdcContent = Convert-ToMDC -SourceFile $skillFile `
                                    -Description $skill.desc `
                                    -Globs $skill.globs `
                                    -Always $AlwaysApply
        
        if ($mdcContent) {
            $outputFile = Join-Path $rulesPath "$($skill.name).mdc"
            $mdcContent | Out-File -FilePath $outputFile -Encoding utf8 -NoNewline
            $createdFiles += $outputFile
            Write-Host "  ✓ Created: $($skill.name).mdc" -ForegroundColor Green
        }
        
        # Include reference files if requested
        if ($IncludeReferences -and $referenceFiles.ContainsKey($skill.name)) {
            foreach ($refFile in $referenceFiles[$skill.name]) {
                $refPath = Join-Path $skillDir $refFile
                if (Test-Path $refPath) {
                    $refName = [System.IO.Path]::GetFileNameWithoutExtension($refFile).ToLower()
                    $refDesc = "$($skill.name) - $refName reference"
                    
                    $refContent = Convert-ToMDC -SourceFile $refPath `
                                               -Description $refDesc `
                                               -Globs $skill.globs `
                                               -Always $false
                    
                    if ($refContent) {
                        $refOutputFile = Join-Path $rulesPath "$($skill.name)-$refName.mdc"
                        $refContent | Out-File -FilePath $refOutputFile -Encoding utf8 -NoNewline
                        $createdFiles += $refOutputFile
                        Write-Host "    ✓ Created: $($skill.name)-$refName.mdc" -ForegroundColor DarkGreen
                    }
                }
            }
        }
    }
    else {
        Write-Host "  ✗ Skipped: $($skill.name) (SKILL.md not found)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Created $($createdFiles.Count) rule files in: $rulesPath" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open your project in Cursor"
Write-Host "  2. Rules will activate automatically based on file patterns"
Write-Host "  3. Test by asking: 'How do I access webhook data in n8n?'"
Write-Host ""

if (-not $IncludeReferences) {
    Write-Host "Tip: Run with -IncludeReferences to add detailed reference files" -ForegroundColor DarkGray
}

