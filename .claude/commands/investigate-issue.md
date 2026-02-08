---
description: Investigate and resolve service integration issues using parallel subagents to preserve context
argument-hint: <service-name> <issue-description-file>
allowed-tools: Read, Grep, Glob, Bash(git:*), Task, Agent
---

# Service Integration Issue Investigation

You are investigating an issue with the **$1** service.

## Phase 1: Parallel Context Gathering (Use Subagents)

**IMPORTANT**: Launch these explorations as PARALLEL subagents to preserve main agent context for solution planning.

### Subagent 1: Repository Documentation Explorer
Use the **Explore subagent** with "medium" thoroughness to review:
- @CLAUDE.md - Project conventions and guidelines
- @README.md - Project overview and setup
- Return a summary of key conventions, dependencies, and architecture relevant to $1

### Subagent 2: Architecture Explorer  
Use the **Explore subagent** with "thorough" thoroughness to:
- Search `/docs` for architecture maps, system diagrams, or design docs
- Identify how $1 integrates with other services
- Map the data flow and key components involved

### Subagent 3: Issue Context Explorer
Use the **Explore subagent** with "thorough" thoroughness to analyze:
- @$2 - The detailed issue description
- Extract symptoms, error messages, reproduction steps
- Identify the expected vs actual behavior

Wait for all subagents to complete before proceeding.

## Phase 2: Synthesize Findings

Consolidate the subagent findings into:
1. **Service Context**: How $1 works in this codebase
2. **Issue Summary**: Clear problem statement from the issue file
3. **Investigation Targets**: Specific files, functions, or flows to examine

## Phase 3: Root Cause Investigation

Use the **general-purpose subagent** for deep investigation:
1. Search the codebase for relevant code paths related to $1
2. Trace the flow from entry point to failure point
3. Identify potential causes based on code analysis
4. Check git history for recent changes that may have caused regression

The subagent should return:
- Root cause hypothesis with supporting evidence
- Specific code locations involved
- Any related issues found in comments or git history

## Phase 4: Solution Planning

With main context preserved, create a robust plan:

### 4.1 Verification Steps
- How to confirm the root cause before implementing fixes
- Test cases that demonstrate the current failure

### 4.2 Implementation Plan
- Specific files and functions to modify
- Step-by-step changes with rationale
- Potential risks and mitigations

### 4.3 Validation Strategy
- How to verify the fix works
- Regression testing considerations
- Edge cases to test

## Output Format

```markdown
## Subagent Findings Summary
[Consolidated results from parallel exploration]

## Root Cause Analysis
[Findings from investigation subagent]

## Proposed Solution
[Detailed implementation plan]

## Validation Checklist
- [ ] Root cause verified
- [ ] Fix implemented
- [ ] Primary issue resolved
- [ ] No regressions introduced
- [ ] Edge cases handled
```
