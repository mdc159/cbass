# CBass Deployment Guide for cbass.space

## Step 1: Configure DNS Records

**IMPORTANT: Do this FIRST before deploying!**

Log into your DNS provider (where you registered cbass.space) and add these A records:

| Subdomain | Type | Value | TTL |
|-----------|------|-------|-----|
| n8n.cbass.space | A | 191.101.0.164 | 300 |
| openwebui.cbass.space | A | 191.101.0.164 | 300 |
| flowise.cbass.space | A | 191.101.0.164 | 300 |
| supabase.cbass.space | A | 191.101.0.164 | 300 |
| langfuse.cbass.space | A | 191.101.0.164 | 300 |
| neo4j.cbass.space | A | 191.101.0.164 | 300 |
| searxng.cbass.space | A | 191.101.0.164 | 300 |

**Wait 5-10 minutes for DNS propagation before proceeding to Step 2.**

You can check DNS propagation with:
Server:  UnKnown
Address:  fe80::1

Server:  UnKnown
Address:  fe80::1

---

## Step 2: SSH into Your VPS



---

## Step 3: Run Deployment Commands

Copy and paste these commands one by one:

# Executing docker install script, commit: f381ee68b32e515bb4dc034b339266aff1fbc460

ERROR: Unsupported distribution ''

[?2004h[?1049h[22;0;0t[1;24r(B[m[4l[?7h[39;49m[?1h=[?1h=[?25l[39;49m(B[m[H[2J[22;35H(B[0;1m[37m[42m[ New File ][39;49m(B[m[?12l[?25h[24;1H[?1049l[23;0;0t[?1l>[?2004l

---

## Step 4: Paste .env Content

When nano opens, paste this entire content:



**Save and exit**: Press , then , then 

---

## Step 5: Deploy CBass



This will:
- Clone Supabase repository
- Start all services
- Configure Caddy for automatic HTTPS
- Obtain Let''s Encrypt certificates

---

## Step 6: Verify Deployment

Check that all services are running:

NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS

You should see all services in Up state.

---

## Step 7: Access Your Services

After deployment completes (5-10 minutes), access your services:

- **n8n**: https://n8n.cbass.space
- **Open WebUI**: https://openwebui.cbass.space
- **Flowise**: https://flowise.cbass.space
- **Supabase**: https://supabase.cbass.space
- **Langfuse**: https://langfuse.cbass.space
- **Neo4j**: https://neo4j.cbass.space
- **SearXNG**: https://searxng.cbass.space

All will have automatic HTTPS via Let''s Encrypt!

---

## Step 8: Initial Setup

### n8n Setup
1. Go to https://n8n.cbass.space
2. Create your admin account
3. Set up credentials for Ollama, Supabase, etc.

### Open WebUI Setup
1. Go to https://openwebui.cbass.space
2. Create your admin account
3. Configure Ollama connection (http://ollama:11434)

### Supabase Setup
1. Go to https://supabase.cbass.space
2. Login with:
   - Username: admin
   - Password: HCLsR1NUJeqrsV-8dApBPA

---

## Troubleshooting

### Check logs


### Restart a service


### Check Caddy status
caddy  | {"level":"info","ts":1767736740.2752888,"msg":"maxprocs: Leaving GOMAXPROCS=20: CPU quota undefined"}
caddy  | {"level":"info","ts":1767736740.2761443,"msg":"GOMEMLIMIT is updated","package":"github.com/KimMachineGun/automemlimit/memlimit","GOMEMLIMIT":30137031475,"previous":9223372036854775807}
caddy  | {"level":"info","ts":1767736740.2777946,"msg":"using config from file","file":"/etc/caddy/Caddyfile"}
caddy  | {"level":"warn","ts":1767736740.2798617,"msg":"No files matching import glob pattern","pattern":"/etc/caddy/addons/*.conf"}
caddy  | {"level":"info","ts":1767736740.2812052,"msg":"adapted config to JSON","adapter":"caddyfile"}
caddy  | {"level":"warn","ts":1767736740.2812486,"msg":"Caddyfile input is not formatted; run 'caddy fmt --overwrite' to fix inconsistencies","adapter":"caddyfile","file":"/etc/caddy/Caddyfile","line":2}
caddy  | {"level":"info","ts":1767736740.3052688,"logger":"admin","msg":"admin endpoint started","address":"localhost:2019","enforce_origin":false,"origins":["//[::1]:2019","//127.0.0.1:2019","//localhost:2019"]}
caddy  | {"level":"info","ts":1767736740.305648,"logger":"tls.cache.maintenance","msg":"started background certificate maintenance","cache":"0xc0005dd100"}
caddy  | {"level":"warn","ts":1767736740.3061583,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8011"}
caddy  | {"level":"warn","ts":1767736740.3061864,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8011"}
caddy  | {"level":"info","ts":1767736740.30619,"logger":"http.log","msg":"server running","name":"srv8","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3062143,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8002"}
caddy  | {"level":"warn","ts":1767736740.3062165,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8002"}
caddy  | {"level":"info","ts":1767736740.306218,"logger":"http.log","msg":"server running","name":"srv1","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3062294,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8003"}
caddy  | {"level":"warn","ts":1767736740.3062305,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8003"}
caddy  | {"level":"info","ts":1767736740.3062315,"logger":"http.log","msg":"server running","name":"srv2","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3062398,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8007"}
caddy  | {"level":"warn","ts":1767736740.3062408,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8007"}
caddy  | {"level":"info","ts":1767736740.3062418,"logger":"http.log","msg":"server running","name":"srv4","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3062508,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8010"}
caddy  | {"level":"warn","ts":1767736740.3062518,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8010"}
caddy  | {"level":"info","ts":1767736740.3062527,"logger":"http.log","msg":"server running","name":"srv7","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3062787,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8001"}
caddy  | {"level":"warn","ts":1767736740.3062956,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8001"}
caddy  | {"level":"info","ts":1767736740.3062978,"logger":"http.log","msg":"server running","name":"srv0","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3063102,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8005"}
caddy  | {"level":"warn","ts":1767736740.3063118,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8005"}
caddy  | {"level":"info","ts":1767736740.3063133,"logger":"http.log","msg":"server running","name":"srv3","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.3063447,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8008"}
caddy  | {"level":"warn","ts":1767736740.3063612,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8008"}
caddy  | {"level":"info","ts":1767736740.3063636,"logger":"http.log","msg":"server running","name":"srv5","protocols":["h1","h2","h3"]}
caddy  | {"level":"warn","ts":1767736740.306379,"logger":"http","msg":"HTTP/2 skipped because it requires TLS","network":"tcp","addr":":8009"}
caddy  | {"level":"warn","ts":1767736740.306381,"logger":"http","msg":"HTTP/3 skipped because it requires TLS","network":"tcp","addr":":8009"}
caddy  | {"level":"info","ts":1767736740.3063827,"logger":"http.log","msg":"server running","name":"srv6","protocols":["h1","h2","h3"]}
caddy  | {"level":"info","ts":1767736740.3065073,"msg":"autosaved config (load with --resume flag)","file":"/config/caddy/autosave.json"}
caddy  | {"level":"info","ts":1767736740.3065321,"msg":"serving initial configuration"}
caddy  | {"level":"info","ts":1767736740.3085506,"logger":"tls","msg":"storage cleaning happened too recently; skipping for now","storage":"FileStorage:/data/caddy","instance":"6fe001ee-8032-4860-aea3-2b0221df228b","try_again":1767823140.3085482,"try_again_in":86399.999999676}
caddy  | {"level":"info","ts":1767736740.3086932,"logger":"tls","msg":"finished cleaning storage units"}
caddy  | {"level":"info","ts":1767779921.1961703,"msg":"shutting down apps, then terminating","signal":"SIGTERM"}
caddy  | {"level":"warn","ts":1767779921.2449775,"msg":"exiting; byeee!! 👋","signal":"SIGTERM"}
caddy  | {"level":"info","ts":1767779921.3610392,"logger":"http","msg":"servers shutting down with eternal grace period"}
caddy  | {"level":"info","ts":1767779921.5679095,"logger":"admin","msg":"stopped previous server","address":"localhost:2019"}
caddy  | {"level":"info","ts":1767779921.5818298,"msg":"shutdown complete","signal":"SIGTERM","exit_code":0}

### DNS not resolving?
Wait longer (up to 1 hour for full propagation) or check your DNS provider settings.

---

## Next Steps

1. Install OpenCode (see OPENCODE_SETUP.md)
2. Set up n8n workflows
3. Configure Open WebUI with n8n integration
4. Set up backups

