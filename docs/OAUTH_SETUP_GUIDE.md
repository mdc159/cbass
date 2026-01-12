# OAuth Setup Guide for CBass

A beginner-friendly guide to setting up OAuth authentication, written for anyone learning how to add "Sign in with GitHub/Google" to their projects.

## What is OAuth?

OAuth (Open Authorization) lets users sign into your app using their existing accounts from services like GitHub, Google, or Facebook - instead of creating yet another username and password.

**Why use it?**
- Users don't need to remember another password
- You don't have to store passwords (less security risk)
- Users trust signing in with Google/GitHub more than random sites
- It's the "Sign in with..." buttons you see everywhere

## How OAuth Works (Simple Version)

```
1. User clicks "Sign in with GitHub" on your site
         ↓
2. User is redirected to GitHub's login page
         ↓
3. User logs into GitHub (if not already)
         ↓
4. GitHub asks: "Allow CBass to access your account?"
         ↓
5. User clicks "Authorize"
         ↓
6. GitHub redirects back to your site with a secret code
         ↓
7. Your site exchanges that code for user info
         ↓
8. User is now logged in!
```

## What We Set Up

We added GitHub OAuth to the CBass dashboard, which uses **Supabase Auth** as its authentication backend.

### The Players

| Component | Role |
|-----------|------|
| **GitHub** | The OAuth provider (where users have accounts) |
| **Supabase Auth** | Our authentication service (handles the OAuth flow) |
| **CBass Dashboard** | Our app (has the "Sign in with GitHub" button) |

## Step-by-Step Setup

### Step 1: Create a GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in the form:

| Field | Value | Why |
|-------|-------|-----|
| **Application name** | CBass Dashboard | Shows on the GitHub authorization screen |
| **Homepage URL** | `https://cbass.space` | Your app's main URL |
| **Authorization callback URL** | `https://supabase.cbass.space/auth/v1/callback` | Where GitHub sends users after they authorize |

4. Click **"Register application"**
5. Copy the **Client ID** (public, okay to share)
6. Click **"Generate a new client secret"**
7. Copy the **Client Secret** (private, keep safe!)

> **Important**: GitHub only shows the secret once! Copy it immediately.

### Step 2: Configure Supabase Auth

For self-hosted Supabase, we added these environment variables:

```bash
# Added to /opt/cbass/supabase/docker/.env
GOTRUE_EXTERNAL_GITHUB_ENABLED=true
GOTRUE_EXTERNAL_GITHUB_CLIENT_ID=Ov23liSGR5PfN5O3MGfB
GOTRUE_EXTERNAL_GITHUB_SECRET=your_secret_here
GOTRUE_EXTERNAL_GITHUB_REDIRECT_URI=https://supabase.cbass.space/auth/v1/callback
```

And added them to the docker-compose.yml for the auth service:

```yaml
# In supabase/docker/docker-compose.yml under auth service
GOTRUE_EXTERNAL_GITHUB_ENABLED: true
GOTRUE_EXTERNAL_GITHUB_CLIENT_ID: your_client_id
GOTRUE_EXTERNAL_GITHUB_SECRET: your_secret
GOTRUE_EXTERNAL_GITHUB_REDIRECT_URI: https://supabase.cbass.space/auth/v1/callback
```

### Step 3: Restart the Auth Service

```bash
# Stop and remove the old container
docker stop supabase-auth
docker rm supabase-auth

# Recreate with new config
cd /opt/cbass
docker compose -p localai up -d
```

### Step 4: Test It

1. Go to https://cbass.space
2. Click "GitHub" button
3. Authorize the app on GitHub
4. You should be logged in!

## The Callback URL Explained

The callback URL is crucial and must match **exactly** in both places:
- What you entered in GitHub's OAuth app settings
- What Supabase is configured to expect

```
https://supabase.cbass.space/auth/v1/callback
        └─────────┬─────────┘└──────┬──────┘
              Your domain      Supabase's
                               auth endpoint
```

If these don't match, you'll get errors like "redirect_uri mismatch".

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "redirect_uri mismatch" | Callback URL doesn't match | Check URLs match exactly in GitHub and Supabase |
| "Application suspended" | GitHub disabled your app | Check GitHub developer settings |
| "Invalid client_id" | Wrong Client ID | Double-check the Client ID |
| Kong errors | Auth service not configured | Restart supabase-auth after config changes |

## Adding Google OAuth (Similar Process)

1. Go to https://console.cloud.google.com
2. Create a new project (or select existing)
3. Go to **APIs & Services** → **Credentials**
4. Click **"Create Credentials"** → **"OAuth client ID"**
5. Application type: **Web application**
6. Add authorized redirect URI: `https://supabase.cbass.space/auth/v1/callback`
7. Copy Client ID and Client Secret
8. Add to Supabase config:

```bash
GOTRUE_EXTERNAL_GOOGLE_ENABLED=true
GOTRUE_EXTERNAL_GOOGLE_CLIENT_ID=your_google_client_id
GOTRUE_EXTERNAL_GOOGLE_SECRET=your_google_secret
GOTRUE_EXTERNAL_GOOGLE_REDIRECT_URI=https://supabase.cbass.space/auth/v1/callback
```

## Security Notes

- **Client ID**: Public - okay to be in code/visible
- **Client Secret**: Private - never commit to git, never share
- **Callback URL**: Must use HTTPS in production
- Store secrets in environment variables, not in code

## How the Dashboard Code Uses It

The CBass dashboard has a simple button that triggers the OAuth flow:

```typescript
// In the login page
const handleGithubLogin = async () => {
  await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${window.location.origin}/dashboard`
    }
  })
}
```

That's it! Supabase handles all the complex OAuth handshake behind the scenes.

## Vocabulary

| Term | Meaning |
|------|---------|
| **OAuth** | Protocol for authorization (letting apps access accounts) |
| **OAuth Provider** | Service that has user accounts (GitHub, Google) |
| **Client ID** | Your app's public identifier |
| **Client Secret** | Your app's private password |
| **Callback URL** | Where users return after authorizing |
| **Access Token** | Temporary key to access user's data |
| **Scope** | What permissions your app is requesting |

## Resources

- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/) - Great beginner explanation
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth) - Official documentation
- [GitHub OAuth Docs](https://docs.github.com/en/developers/apps/building-oauth-apps)

---

*Created for the CBass AI learning project - January 2026*
