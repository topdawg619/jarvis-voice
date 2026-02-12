# Jarvis Voice Client

Minimal web UI for voice chatting with Jarvis via OpenClaw or direct OpenAI calls.

## Remote Config

The page now tries to fetch a secure config bundle before showing the UI. By default it requests:

```
https://soviet-partners-indie-determined.trycloudflare.com/jarvis-voice-config.json
```

That URL should serve JSON shaped like this:

```json
{
  "backend": "openclaw",
  "gatewayUrl": "https://your-tunnel.trycloudflare.com",
  "gatewayToken": "token-here",
  "apiKey": "sk-your-openai-key",
  "ttsKey": "sk-your-openai-key",
  "voice": "echo",
  "model": "gpt-4o"
}
```

- Store the real file somewhere private (same host as your tunnel works great) and keep it outside of source control.  
- The repo includes `config/jarvis-voice-config.sample.json` as a reference; copy it, fill in the real values, and expose it via your tunnel (e.g., `~/public/jarvis-voice-config.json`).  
- The client caches the fetched values in `localStorage`, so once the page loads successfully the settings persist offline per-device.  
- If the fetch fails (URL unreachable, auth block, etc.) the UI falls back to the last saved localStorage values and prompts for manual entry.

## Deployment

1. Update `CONFIG_URL` near the top of `index.html` if you move the private config file.  
2. Commit/push to `main`; GitHub Pages redeploys automatically from the `docs/` or root (current setup: root).  
3. Make sure the private config URL is reachable via HTTPS and allows cross-origin GETs from `https://topdawg619.github.io`.

## Local Dev

```
npx http-server . -p 4173
```

Then browse to `http://localhost:4173` and test.
