# TruthLens Live Deployment Guide

## Quick Deploy on Render (Free)

### Step 1: Push Latest Code to GitHub
```bash
git add .
git commit -m "Add Render deployment config + mock model support"
git push origin master
```

### Step 2: Deploy on Render
1. Go to https://render.com and sign up with GitHub
2. Click **"New +"** → **"Blueprint"** (uses render.yaml)
3. Select your `fake-news-intelligence-platform` repo
4. Render will auto-detect the `render.yaml` config
5. Click **"Apply"**
6. Add your API keys as environment variables:
   - `GOOGLE_FACT_CHECK_API_KEY` = your key
   - `GOOGLE_SEARCH_API_KEY` = your key  
   - `GOOGLE_SEARCH_ENGINE_ID` = 464e66865ed8f47e7
7. Wait 2-3 minutes for deployment

### Why `USE_MOCK_MODEL=true`?
Render's free tier has only **512MB RAM**. The real transformer model needs ~250MB+ to download. The mock model works instantly with zero memory usage.

### Step 3: Get Your API URL
After deployment, copy your API URL (e.g., `https://truthlens-api.onrender.com`)

### Step 4: Connect Frontend
Edit `frontend/web/lib/api.ts`:
```typescript
const API_BASE = 'https://your-render-url.com/api/v1'
```

Rebuild and redeploy the frontend.

---

## Manual Deploy (Without Blueprint)

If Blueprint doesn't work, use Web Service:

| Setting | Value |
|---------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python -m api.main` |
| **Environment Variables** | `USE_MOCK_MODEL=true` + your API keys |

---

## Test Your Deployed API
```bash
curl -X POST https://your-render-url.com/api/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"query": "The Earth is flat", "type": "text"}'
```

## Troubleshooting

### "Out of memory"
→ Make sure `USE_MOCK_MODEL=true` is set

### "No open ports detected"
→ The port fix is in `api/main.py` - it now uses the `PORT` env var

### CORS errors
→ Already configured to allow all origins

### 403 from Google APIs
→ Enable billing on Google Cloud (required even for free tier)
