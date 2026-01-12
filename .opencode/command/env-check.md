---
description: Verify environment configuration is complete
agent: build
---

Check that all required environment variables are properly configured:

1. Read env.example and list all required variables
2. Check if .env exists (warn if missing)
3. For each required variable in env.example:
   - Check if it has a placeholder value that needs replacing
   - Identify which are secrets (passwords, keys, tokens)
   - Identify which are hostnames (for production deployment)
4. Verify no @ symbol in POSTGRES_PASSWORD
5. Check that all *_HOSTNAME variables follow correct format
6. Report any missing or incomplete configuration
7. Provide a checklist of what needs to be set before deployment
