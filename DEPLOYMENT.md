# Fraud Detection System - Production Deployment Guide

## Architecture Overview

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Frontend      │      │    Backend      │      │   Database      │
│   (Vercel)      │─────▶│   (Render)      │─────▶│  (Supabase)     │
│   React + Vite  │      │   FastAPI       │      │  PostgreSQL     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## Prerequisites

Before deploying, ensure you have accounts on:
- ✅ [Vercel](https://vercel.com) - Frontend hosting (free tier available)
- ✅ [Render](https://render.com) - Backend hosting (free tier available)
- ✅ [Supabase](https://supabase.com) - PostgreSQL database (free tier available)
- ✅ [GitHub](https://github.com) - Code repository

---

## Step 1: Setup Supabase Database (5 minutes)

### 1.1 Create Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click **"New Project"**
3. Fill in details:
   - **Name**: `fraud-detection-db`
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users (e.g., `US East`)
4. Click **"Create new project"** (takes ~2 minutes)

### 1.2 Get Database Connection Strings

1. Go to **Project Settings** (gear icon in sidebar)
2. Click **Database** tab
3. Scroll to **Connection String** section
4. Copy **Connection String** (Session mode):

```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

5. Save TWO versions:
   - **Async** (for backend): `postgresql+asyncpg://postgres...`
   - **Sync** (for migrations): `postgresql://postgres...`

### 1.3 Run Database Migrations

Since Supabase tables auto-create on first API call, no manual migration needed.
The backend will create tables automatically on startup.

---

## Step 2: Deploy Backend to Render (10 minutes)

### 2.1 Push Code to GitHub

```bash
# Initialize git (if not already done)
cd D:\ai_projects\fraud_detection_system
git init
git add .
git commit -m "Initial deployment setup"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR-USERNAME/fraud-detection-system.git
git branch -M main
git push -u origin main
```

### 2.2 Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `fraud-detection-api`
   - **Region**: Same as Supabase (e.g., `Oregon`)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.3 Add Environment Variables

In Render Dashboard, go to **Environment** tab and add:

```bash
# Database (from Supabase)
DATABASE_URL=postgresql+asyncpg://postgres.[REF]:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
DATABASE_URL_SYNC=postgresql://postgres.[REF]:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres

# Model Configuration
MODEL_DIR=/opt/render/project/src/models
FRAUD_THRESHOLD=0.10
FALLBACK_AMOUNT_LIMIT=50.0

# Security
API_KEY=your-secure-api-key-here

# Performance
RATE_LIMIT_PER_SECOND=100
LOG_LEVEL=INFO
```

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (~5-10 minutes)
3. Once deployed, copy your backend URL:
   ```
   https://fraud-detection-api-xxxx.onrender.com
   ```

### 2.5 Verify Backend is Running

```bash
# Test health endpoint
curl https://fraud-detection-api-xxxx.onrender.com/api/v1/health

# Expected response:
{
  "status": "healthy",
  "model_version": "6.0",
  "database": "connected"
}
```

---

## Step 3: Deploy Frontend to Vercel (5 minutes)

### 3.1 Update Frontend Environment Variables

1. Edit `frontend/.env.production`:

```bash
VITE_API_URL=https://fraud-detection-api-xxxx.onrender.com/api/v1
```

2. Commit changes:

```bash
git add frontend/.env.production
git commit -m "Update production API URL"
git push
```

### 3.2 Deploy to Vercel

**Option A: Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel --prod

# Follow prompts:
# - Link to existing project? No
# - Project name: fraud-detection-dashboard
# - Directory: ./ (current directory)
# - Override settings? No
```

**Option B: Vercel Dashboard**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://fraud-detection-api-xxxx.onrender.com/api/v1`
6. Click **"Deploy"**

### 3.3 Get Frontend URL

After deployment completes, Vercel will provide your URL:
```
https://fraud-detection-dashboard.vercel.app
```

### 3.4 Update Backend CORS

1. Go to Render Dashboard → Your Service → **Environment**
2. Add environment variable:
   ```
   ALLOWED_ORIGINS=https://fraud-detection-dashboard.vercel.app
   ```
3. Redeploy backend

---

## Step 4: Upload Model to Render (5 minutes)

Your trained model v6.0 needs to be uploaded to Render.

### Option A: Using Render Persistent Disk (Recommended)

1. In Render Dashboard, go to your service
2. Click **"Disks"** tab
3. Add disk:
   - **Name**: `model-storage`
   - **Mount Path**: `/opt/render/project/src/models`
   - **Size**: 1 GB (free)
4. Upload model files via SSH or API

### Option B: Store Model in GitHub (Simple)

```bash
# Add model files to git
git add backend/models/v6.0_model.pkl
git add backend/models/v6.0_metadata.json
git commit -m "Add trained model v6.0"
git push

# Render will automatically redeploy with the model
```

**Note**: If model is >100MB, use Git LFS:
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add backend/models/v6.0_model.pkl
git commit -m "Add model with Git LFS"
git push
```

### Option C: Train Model on Render (Alternative)

```bash
# SSH into Render (requires paid plan)
# Or use Render Shell in dashboard

cd /opt/render/project/src
python scripts/register_v6_model.py
```

---

## Step 5: Configure WooCommerce Plugin

Now that backend is deployed, configure your WooCommerce plugin:

1. Upload `plugin/woo-fraud-detect.zip` to WordPress
2. Activate plugin
3. Go to **WooCommerce → Fraud Detection**
4. Configure:
   - **API Endpoint**: `https://fraud-detection-api-xxxx.onrender.com`
   - **Fraud Threshold**: `0.10` (matches model v6.0)
   - **Auto-hold Fraud Orders**: ✅ Enabled
   - **Email Notifications**: ✅ Enabled

---

## Step 6: Test End-to-End

### Test 1: Dashboard Access

1. Visit: `https://fraud-detection-dashboard.vercel.app`
2. Check dashboard loads
3. Verify metrics display (may be empty initially)

### Test 2: API Health Check

```bash
curl https://fraud-detection-api-xxxx.onrender.com/api/v1/health
```

Expected:
```json
{
  "status": "healthy",
  "model_version": "6.0",
  "database": "connected",
  "threshold": 0.10
}
```

### Test 3: Fraud Prediction

```bash
curl -X POST https://fraud-detection-api-xxxx.onrender.com/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_id": "test_merchant",
    "amount": 2500.0,
    "payment_method": "credit_card",
    "user_id_hash": "abc123",
    "ip_hash": "192.168.1.1",
    "email_domain": "tempmail.com",
    "is_new_user": true,
    "device_type": "mobile",
    "billing_shipping_match": false,
    "hour_of_day": 3,
    "day_of_week": 2,
    "items_count": 1
  }'
```

Expected (fraud detection):
```json
{
  "transaction_id": "...",
  "label": "fraud",
  "confidence": 0.9989,
  "top_features": [
    {"feature": "billing_shipping_match", "contribution": 4.91},
    {"feature": "is_new_user", "contribution": 1.44}
  ]
}
```

### Test 4: WooCommerce Integration

1. Create test order in WooCommerce
2. Check order notes for fraud detection result
3. Verify email notification (if fraud detected)

---

## Monitoring & Maintenance

### Supabase Database

**Check Database Status:**
1. Go to Supabase Dashboard
2. Click **Database** → **Health**
3. Monitor: CPU usage, Memory, Active connections

**View Tables:**
```sql
-- In Supabase SQL Editor
SELECT * FROM transactions LIMIT 10;
SELECT * FROM predictions WHERE label = 'fraud' LIMIT 10;
SELECT version, is_active, recall FROM models;
```

### Render Backend

**View Logs:**
1. Render Dashboard → Your Service → **Logs**
2. Filter by severity (INFO, WARNING, ERROR)

**Monitor Performance:**
- Response times
- Error rates
- Memory usage
- CPU usage

**Auto-scaling** (Paid plan):
- Render automatically scales based on traffic

### Vercel Frontend

**View Analytics:**
1. Vercel Dashboard → Your Project → **Analytics**
2. Monitor: Page views, Load time, Errors

**View Logs:**
- **Functions** tab shows API calls
- **Deployments** tab shows build logs

---

## Cost Breakdown

| Service | Free Tier | Paid Tier | Recommendation |
|---------|-----------|-----------|----------------|
| **Supabase** | 500 MB database, 2 GB bandwidth | $25/month (8 GB DB) | Free tier sufficient for 50K-100K transactions |
| **Render** | 750 hours/month, sleeps after inactivity | $7/month (always on) | Start free, upgrade if <200ms latency needed |
| **Vercel** | 100 GB bandwidth, unlimited deployments | $20/month (Pro) | Free tier sufficient for most use cases |
| **Total** | **$0/month** | **$52/month** | |

**Free Tier Limitations:**
- Render: API sleeps after 15 min inactivity (30-60s wake time)
- Supabase: 500 MB database (~100K-200K transactions)
- Vercel: 100 GB bandwidth (~1M page views)

**Recommendation**: Start on free tier, upgrade Render first ($7/month for always-on).

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError`
- **Fix**: Check `build.sh` ran successfully, verify `pyproject.toml` dependencies

**Error**: `Database connection failed`
- **Fix**: Verify Supabase connection string in Render environment variables
- Check Supabase project is active (not paused)

### Frontend can't reach backend

**Error**: `CORS error` or `Network error`
- **Fix**: Update `ALLOWED_ORIGINS` in Render to include Vercel URL
- Verify `VITE_API_URL` in Vercel environment variables

### Model not loading

**Error**: `No active model found`
- **Fix**: Upload model files to Render (see Step 4)
- Or run `python scripts/register_v6_model.py` on Render

### Predictions taking too long

**Issue**: >2 second response times
- **Cause**: Render free tier (API sleeps)
- **Fix**: Upgrade to Render paid plan ($7/month for always-on)

---

## Security Best Practices

### Environment Variables
- ✅ Never commit `.env` files to git
- ✅ Use strong, randomly generated `API_KEY`
- ✅ Rotate database passwords quarterly

### API Security
- ✅ Enable rate limiting (already configured: 100 req/s)
- ✅ Restrict CORS to specific domains (update `allowed_origins`)
- ✅ Require API key for `/retrain` endpoint (already configured)

### Database Security
- ✅ Use Supabase Row Level Security (RLS) for multi-tenant
- ✅ Enable connection pooling (already enabled with `pooler.supabase.com`)
- ✅ Regular backups (Supabase auto-backups on paid plan)

---

## Next Steps After Deployment

1. ✅ **Register custom domain** (optional)
   - Vercel: Dashboard → Domains → Add domain
   - Render: Dashboard → Settings → Custom domain

2. ✅ **Enable SSL** (already automatic on Vercel/Render)

3. ✅ **Setup monitoring** (optional)
   - Uptime monitoring: [UptimeRobot](https://uptimerobot.com) (free)
   - Error tracking: [Sentry](https://sentry.io) (free tier)

4. ✅ **Schedule model retraining** (recommended monthly)
   - Use Render Cron Jobs (paid plan)
   - Or GitHub Actions workflow

5. ✅ **Add analytics** (optional)
   - Google Analytics for dashboard
   - PostHog for product analytics

---

## Support & Documentation

**API Documentation**: `https://your-backend.onrender.com/docs`
**GitHub Issues**: `https://github.com/YOUR-USERNAME/fraud-detection-system/issues`
**Email**: your-email@example.com

---

**🎉 Congratulations! Your fraud detection system is now live in production!**
