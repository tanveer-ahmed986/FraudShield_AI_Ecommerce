# Fraud Detection System - Quick Start

## 🚀 Production Deployment (Vercel + Render + Supabase)

Your fraud detection system is configured for deployment to:
- **Frontend**: Vercel (https://vercel.com)
- **Backend**: Render (https://render.com)
- **Database**: Supabase (https://supabase.com)

All platforms offer generous free tiers to get started!

---

## ⚡ Quick Start (Choose Your Path)

### Path A: Full Deployment (~45 min)
Follow the complete guide: **[DEPLOYMENT.md](DEPLOYMENT.md)**

### Path B: Quick Checklist (~30 min)
Use the interactive checklist: **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**

### Path C: Automated Script
Run the deployment helper:
```bash
# Linux/Mac
./deploy.sh

# Windows
deploy.bat
```

---

## 📋 What's Been Configured

### ✅ Frontend (Vercel)
- `frontend/vercel.json` - Vercel build configuration
- `frontend/.env.example` - Environment variable template
- `frontend/.env.production` - Production environment (update with your URLs)
- `frontend/src/api/client.ts` - Updated to use environment variables

### ✅ Backend (Render)
- `backend/render.yaml` - Render service configuration
- `backend/build.sh` - Build script for Render
- `backend/.env.example` - Environment variable template
- `backend/.env.production` - Production environment (update with Supabase connection)
- `backend/app/config.py` - Updated for Supabase compatibility
- `backend/app/main.py` - Updated CORS for Vercel

### ✅ WooCommerce Plugin
- `plugin/woo-fraud-detect.zip` - Ready to upload (4.4 KB)

### ✅ Documentation
- `DEPLOYMENT.md` - Complete deployment guide (comprehensive)
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `README_DEPLOYMENT.md` - This file (quick reference)

---

## 🎯 Deployment Overview

```
Step 1: Supabase     → Create database, get connection strings
Step 2: Render       → Deploy backend API
Step 3: Vercel       → Deploy frontend dashboard
Step 4: Upload Model → Add trained model to Render
Step 5: Configure    → Update CORS, test endpoints
Step 6: WooCommerce  → Install and configure plugin
```

**Total Time**: 30-45 minutes
**Cost**: $0/month (free tiers)

---

## 🔑 Required Accounts

Before starting, create accounts on:
1. **Supabase** - Database (https://supabase.com/dashboard/sign-up)
2. **Render** - Backend hosting (https://dashboard.render.com/register)
3. **Vercel** - Frontend hosting (https://vercel.com/signup)
4. **GitHub** - Code repository (https://github.com/join)

---

## 🛠️ Prerequisites

- [x] Git installed
- [x] Node.js 18+ installed
- [x] GitHub account
- [ ] Supabase account
- [ ] Render account
- [ ] Vercel account

---

## 📦 What You'll Deploy

### Frontend Dashboard
- Real-time fraud analytics
- Transaction history
- SHAP explanations
- Model metrics

**Tech**: React + TypeScript + Vite

### Backend API
- Fraud prediction endpoint
- Model training API
- Dashboard data API
- Health monitoring

**Tech**: FastAPI + Python 3.11 + XGBoost

### Database
- Transaction storage
- Prediction history
- Audit logs
- Model metadata

**Tech**: PostgreSQL (Supabase)

### WooCommerce Plugin
- Automatic fraud checking
- Order hold on fraud
- Email notifications
- Admin settings panel

**Tech**: PHP 8.0+

---

## 🚦 Deployment Status Tracker

Use this to track your progress:

- [ ] **Supabase**: Database created, connection strings saved
- [ ] **Render**: Backend deployed and healthy
- [ ] **Vercel**: Frontend deployed and accessible
- [ ] **Model**: v6.0 uploaded and loaded
- [ ] **CORS**: Updated with Vercel URL
- [ ] **WooCommerce**: Plugin installed and configured
- [ ] **Testing**: All tests passing
- [ ] **Monitoring**: Uptime monitors configured (optional)

---

## 📊 Expected Performance

| Metric | Target | Free Tier Reality |
|--------|--------|-------------------|
| API Response | <200ms | 50-200ms (cold start: 30-60s) |
| Dashboard Load | <2s | 1-3s |
| Prediction Accuracy | 94.9% recall | ✅ Same |
| Uptime | 99.9% | 99%+ (Render sleeps after 15 min) |

**Note**: Render free tier sleeps after inactivity. Upgrade to $7/month for always-on.

---

## 💰 Cost Breakdown

### Free Forever
- Supabase: 500 MB database, 2 GB bandwidth
- Render: 750 hours/month, sleeps after inactivity
- Vercel: 100 GB bandwidth, unlimited deployments

### When to Upgrade

**Render** ($7/month):
- ✅ Always-on (no cold starts)
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- **Recommended**: If you process >100 transactions/day

**Supabase** ($25/month):
- ✅ 8 GB database
- ✅ 50 GB bandwidth
- ✅ Daily backups
- **Recommended**: If you have >100K transactions

**Vercel** ($20/month):
- ✅ Analytics dashboard
- ✅ 1 TB bandwidth
- ✅ Team collaboration
- **Recommended**: For production businesses only

---

## 🧪 Testing Checklist

After deployment, verify:

### Backend
```bash
# Health check
curl https://your-api.onrender.com/api/v1/health

# Fraud prediction
curl -X POST https://your-api.onrender.com/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":"test","amount":2500,"payment_method":"credit_card",...}'
```

### Frontend
- [ ] Dashboard loads: `https://your-app.vercel.app`
- [ ] Metrics display
- [ ] Predictions page works
- [ ] Test transaction form functional

### WooCommerce
- [ ] Plugin activated
- [ ] API connection ✅ green
- [ ] Test order creates fraud check
- [ ] Admin email received on fraud

---

## 🐛 Common Issues & Fixes

### "CORS error" in frontend
**Fix**: Add Vercel URL to Render environment variable `ALLOWED_ORIGINS`

### "No active model found"
**Fix**: Upload model files to Render (see DEPLOYMENT.md Step 4)

### "Database connection failed"
**Fix**: Verify Supabase connection string in Render environment variables

### "API takes 30+ seconds"
**Fix**: Render free tier sleeps. Upgrade to $7/month or make initial request to wake it

---

## 📚 Full Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete step-by-step guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Interactive checklist
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Full project documentation
- **API Docs**: `https://your-api.onrender.com/docs` (after deployment)

---

## 🆘 Need Help?

1. Check **[DEPLOYMENT.md](DEPLOYMENT.md)** → Troubleshooting section
2. Review **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
3. Create GitHub Issue with:
   - Deployment step you're on
   - Error message/screenshot
   - Platform (Supabase/Render/Vercel)

---

## 🎉 Ready to Deploy?

Choose your path:

```bash
# Option 1: Run automated script
./deploy.sh  # or deploy.bat on Windows

# Option 2: Follow checklist
# Open: DEPLOYMENT_CHECKLIST.md

# Option 3: Read full guide
# Open: DEPLOYMENT.md
```

**Estimated time**: 30-45 minutes
**Cost**: $0 (free tiers)
**Result**: Production-ready fraud detection system

---

**Let's deploy! 🚀**
