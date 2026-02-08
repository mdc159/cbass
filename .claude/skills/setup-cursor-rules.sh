#!/bin/bash
# setup-cursor-rules.sh
# Converts n8n-skills to Cursor MDC format rules
#
# Usage:
#   ./setup-cursor-rules.sh                           # Uses current directory
#   ./setup-cursor-rules.sh /path/to/n8n-project     # Specify target project
#   ./setup-cursor-rules.sh -r                        # Include reference files
#   ./setup-cursor-rules.sh -a                        # Always apply rules

set -e

# Parse arguments
TARGET_PROJECT="."
INCLUDE_REFS=false
ALWAYS_APPLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--refs)
            INCLUDE_REFS=true
            shift
            ;;
        -a|--always)
            ALWAYS_APPLY=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [TARGET_PROJECT]"
            echo ""
            echo "Options:"
            echo "  -r, --refs     Include reference files (detailed docs)"
            echo "  -a, --always   Set alwaysApply: true on all rules"
            echo "  -h, --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                              # Setup in current directory"
            echo "  $0 /path/to/project             # Setup in specific project"
            echo "  $0 -r /path/to/project          # Include all reference files"
            exit 0
            ;;
        *)
            TARGET_PROJECT="$1"
            shift
            ;;
    esac
done

# Find skills directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_PATH="$SCRIPT_DIR/n8n-mcp-skills-v1.0.0/skills"

if [[ ! -d "$SKILLS_PATH" ]]; then
    echo "Error: Skills directory not found at: $SKILLS_PATH"
    exit 1
fi

# Create target rules directory
RULES_PATH="$TARGET_PROJECT/.cursor/rules"
mkdir -p "$RULES_PATH"
echo -e "\033[36mCreating rules in: $RULES_PATH\033[0m"

# Function to convert file to MDC format
convert_to_mdc() {
    local source_file="$1"
    local description="$2"
    local globs="$3"
    local always="$4"
    
    if [[ ! -f "$source_file" ]]; then
        return 1
    fi
    
    # Read content and remove existing YAML frontmatter
    local content
    content=$(sed '1{/^---$/!b};1,/^---$/d' "$source_file" | sed '1{/^---$/d}')
    
    # Build frontmatter
    local frontmatter="---
description: $description
globs: [$globs]"
    
    if [[ "$always" == "true" ]]; then
        frontmatter="$frontmatter
alwaysApply: true"
    fi
    
    frontmatter="$frontmatter
---

"
    
    echo -n "$frontmatter"
    echo "$content"
}

# Skill definitions
declare -A SKILL_DESCS=(
    ["n8n-expression-syntax"]='n8n expression syntax, {{}} double curly braces, $json variables, $node references, webhook body data access, $now datetime, $env environment variables'
    ["n8n-mcp-tools-expert"]='n8n-mcp MCP server tools, search_nodes, get_node, validate_node, validate_workflow, n8n_create_workflow, n8n_update_partial_workflow, template search, nodeType format'
    ["n8n-workflow-patterns"]='n8n workflow patterns, webhook processing, HTTP API integration, database sync, AI agent workflows, scheduled tasks, workflow architecture'
    ["n8n-validation-expert"]='n8n validation errors, validation profiles, false positives, auto-sanitization, error interpretation, fixing validation failures'
    ["n8n-node-configuration"]='n8n node configuration, property dependencies, operation-specific settings, AI connection types, conditional fields'
    ["n8n-code-javascript"]='n8n Code node JavaScript, $input.all, $input.first, $json, $helpers.httpRequest, return format, webhook body gotcha, built-in functions'
    ["n8n-code-python"]='n8n Code node Python, _input, _json, standard library only, no external packages, Python limitations in n8n'
)

GLOBS='"*.json", "workflows/**/*.json", "**/n8n/**"'

# Reference files for each skill
declare -A SKILL_REFS=(
    ["n8n-expression-syntax"]="COMMON_MISTAKES.md EXAMPLES.md"
    ["n8n-mcp-tools-expert"]="SEARCH_GUIDE.md VALIDATION_GUIDE.md WORKFLOW_GUIDE.md"
    ["n8n-workflow-patterns"]="webhook_processing.md http_api_integration.md database_operations.md ai_agent_workflow.md scheduled_tasks.md"
    ["n8n-validation-expert"]="ERROR_CATALOG.md FALSE_POSITIVES.md"
    ["n8n-node-configuration"]="DEPENDENCIES.md OPERATION_PATTERNS.md"
    ["n8n-code-javascript"]="DATA_ACCESS.md COMMON_PATTERNS.md ERROR_PATTERNS.md BUILTIN_FUNCTIONS.md"
    ["n8n-code-python"]="DATA_ACCESS.md COMMON_PATTERNS.md ERROR_PATTERNS.md STANDARD_LIBRARY.md"
)

created_count=0

for skill in "${!SKILL_DESCS[@]}"; do
    skill_file="$SKILLS_PATH/$skill/SKILL.md"
    
    if [[ -f "$skill_file" ]]; then
        output_file="$RULES_PATH/$skill.mdc"
        convert_to_mdc "$skill_file" "${SKILL_DESCS[$skill]}" "$GLOBS" "$ALWAYS_APPLY" > "$output_file"
        echo -e "  \033[32m✓ Created: $skill.mdc\033[0m"
        ((created_count++))
        
        # Include reference files if requested
        if [[ "$INCLUDE_REFS" == "true" && -n "${SKILL_REFS[$skill]}" ]]; then
            for ref_file in ${SKILL_REFS[$skill]}; do
                ref_path="$SKILLS_PATH/$skill/$ref_file"
                if [[ -f "$ref_path" ]]; then
                    ref_name=$(basename "$ref_file" .md | tr '[:upper:]' '[:lower:]')
                    ref_desc="$skill - $ref_name reference"
                    ref_output="$RULES_PATH/$skill-$ref_name.mdc"
                    
                    convert_to_mdc "$ref_path" "$ref_desc" "$GLOBS" "false" > "$ref_output"
                    echo -e "    \033[32m✓ Created: $skill-$ref_name.mdc\033[0m"
                    ((created_count++))
                fi
            done
        fi
    else
        echo -e "  \033[33m✗ Skipped: $skill (SKILL.md not found)\033[0m"
    fi
done

echo ""
echo -e "\033[36m═══════════════════════════════════════════════════════════════\033[0m"
echo -e "\033[32mSetup Complete!\033[0m"
echo -e "\033[36m═══════════════════════════════════════════════════════════════\033[0m"
echo ""
echo -e "Created $created_count rule files in: $RULES_PATH"
echo ""
echo -e "\033[33mNext Steps:\033[0m"
echo "  1. Open your project in Cursor"
echo "  2. Rules will activate automatically based on file patterns"
echo "  3. Test by asking: 'How do I access webhook data in n8n?'"
echo ""

if [[ "$INCLUDE_REFS" != "true" ]]; then
    echo -e "\033[90mTip: Run with -r to add detailed reference files\033[0m"
fi

