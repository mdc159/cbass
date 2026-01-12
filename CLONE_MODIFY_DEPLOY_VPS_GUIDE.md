# Clone → New Repo → Modify → Deploy to a VPS (Working Guide)

This is our shared playbook for taking an existing repository, creating a new repository based on it, making changes, and deploying it to a cloud VPS.

It also includes a collaboration protocol: what information you provide so an agent can execute the workflow safely and predictably.

---

## 0) First decision: what does “clone into a new repo” mean?

There are four common intents. Pick one because the git steps differ significantly.

1. **Fork** (preserve history, keep upstream relationship)
   - Best when you want to keep syncing upstream changes.
2. **Template / “Use this template”** (copy code, new history)
   - Best when starting a new project from a starter kit.
3. **Mirror with history but new origin** (copy full history, no fork relationship)
   - Best when you want full commit history but do not want a fork relationship.
4. **Subtree/submodule** (embed one repo inside another)
   - Best when you need a vendored dependency while keeping repositories separate.

**Default recommendation** (when unsure):
- **Template** for “starter kit → my product”.
- **Fork** for “I will keep syncing upstream”.

---

## 1) End-to-end workflow (high level)

### A) Create the new repository
- Create an empty repo on GitHub/GitLab.
- Populate it using one of the methods above.
- Update project metadata:
  - `README`, name, license
  - package name/app name
  - CI badges (if applicable)

### B) Modify the project
- Implement changes on a feature branch.
- Run tests/lint/build locally (or confirm CI passes).
- Create a PR (recommended even for solo work).

### C) Prepare the VPS
- Provision VPS (Ubuntu 22.04 LTS is a solid default).
- Configure SSH access (keys), disable password auth.
- Configure firewall.
- Install runtime (Docker is usually the simplest).
- Create a deployment user (non-root).

### D) Deploy
Two common deployment styles:

- **Docker Compose** (most straightforward for VPS deployments)
  - `docker compose up -d`
  - Reverse proxy with TLS: Caddy (simple) or Nginx

- **systemd service** (good for a single binary or a simple app process)
  - `systemctl enable --now yourapp`
  - Manage env vars and view logs via `journalctl`

### E) Operate
- Logs and monitoring
- Backups (especially for DB/uploads)
- Secrets management
- Update strategy (manual deploy vs CI/CD)

---

## 2) Collaboration protocol: what you provide so the agent can do it end-to-end

If you want an agent to execute this safely, provide a “deployment brief” with the following.

### Repo + git intent
- **Source repo URL**: `https://...`
- **Destination host**: GitHub or GitLab
- **Destination repo name/org**: e.g. `org/new-repo`
- **Method**: `fork | template | mirror | subtree`
- **Preserve history**: `yes/no`
- **Do we need to pull upstream later?** (yes/no)

### App + stack
- Stack: Node/Python/Go/Rails/etc.
- How it runs locally (one command): e.g. `npm run dev` or `docker compose up`
- Listen port: e.g. `3000`
- Persistence needs: DB, uploads directory, Redis, etc.
- Domain: `example.com` (or “none yet”)

### VPS details
- Provider: DigitalOcean / Hetzner / Linode / AWS Lightsail / etc.
- OS: Ubuntu version (22.04 recommended)
- SSH access: key-based (recommended)
- Deploy style: Docker Compose vs systemd

### Security / secrets
- List required env vars (do not paste secret values unless you want them stored in chat)
- Where secrets live:
  - server-side `.env`
  - GitHub Actions secrets
  - a secret manager (advanced)

### Approval boundaries (important)
Confirm what the agent is allowed to do:
- Create repos via `gh` / GitHub API
- Push to remote (and to which branches)
- Create PRs
- SSH into VPS and modify server state

---

## 3) A reusable command prompt (copy/paste template)

Fill this in and send it whenever you want the full cycle executed.

```text
Create a new repo from this source and deploy to my VPS.

- Source repo: ...
- Destination repo: ... (GitHub/GitLab)
- Method: template | fork | mirror | subtree
- Preserve history: yes/no
- Changes to make:
  1) ...
  2) ...
- Deployment target: VPS on ..., Ubuntu ...
- Domain: ... (or none)
- Deploy style: docker compose (preferred) / systemd
- App port: ...
- Data persistence: ...
- Secrets: I will provide via ... (GitHub secrets / server .env)
- Constraints: don’t commit secrets; don’t force-push; open a PR before merging.
```

---

## 4) Common default: Docker Compose on Ubuntu

This is the most typical pattern for a small-to-medium web app on a VPS.

- App runs in a container
- Reverse proxy container terminates TLS (Caddy is the easiest)
- `docker-compose.yml` defines services
- Server directory like `/opt/yourapp`
- Deploy is usually:
  - `git pull` (or pulling a container image)
  - `docker compose up -d`

---

## 5) Next input needed (to proceed with exact commands)

Pick one:
- **fork**, **template**, **mirror**, or **subtree/submodule**

Then provide:
- Source repo URL
- Destination repo location (org/user + name)
- VPS provider (and whether you already have it provisioned)
