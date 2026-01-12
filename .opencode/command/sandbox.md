---
description: Create a safe environment for experimentation
agent: build
---

Create a sandbox environment for safe experimentation:

1. **Create experiment branch**:
   ```bash
   git checkout -b sandbox/[experiment-name]
   ```

2. **Document the experiment**:
   - What are we trying to do?
   - What do we expect to happen?
   - What could go wrong?

3. **Make the changes**:
   - Implement the experiment
   - Explain each step clearly
   - Show what files are being modified

4. **Test thoroughly**:
   - Run validation commands
   - Check for errors
   - Verify expected behavior

5. **Evaluate results**:
   - Did it work as expected?
   - What did we learn?
   - Should we keep or discard?

6. **Clean up**:
   - If successful: `git checkout master && git merge sandbox/[name]`
   - If failed: `git checkout master && git branch -D sandbox/[name]`
   - Explain what happened and why

Remember: Experiments are for learning. Failure is valuable data!
