$json = Get-Content 'X:\GitHub\CBass\flowise\Deep Research Tutorial Agents.json' -Raw | ConvertFrom-Json
$flowData = $json | ConvertTo-Json -Depth 100 -Compress

$wrapped = @{
    name = "Deep Research Tutorial Agents"
    flowData = $flowData
    type = "AGENTFLOW"
}

$wrapped | ConvertTo-Json -Depth 10 | Set-Content 'X:\GitHub\CBass\flowise\Deep Research Tutorial Agents-wrapped.json' -Encoding UTF8
Write-Host "Created wrapped JSON"
