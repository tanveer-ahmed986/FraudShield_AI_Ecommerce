# Production Deployment Checklist

## Pre-Deployment Setup

### 1. Supabase Database Setup (5 min)
- [ ] Create Supabase account
- [ ] Create new project: `fraud-detection-db`
- [ ] Copy connection string (Session mode)
- [ ] Save both async and sync connection strings

**Connection String Format:**
```
Async:  postgresql+asyncpg://postgres.[REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
Sync:   postgresql://postgres.[REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

---

### 2. GitHub Repository (2 min)
- [ ] Create GitHub repository: `fraud-detection-system`
- [ ] Push code to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/fraud-detection-system.git
git push -u origin main
```

---

### 3. Render Backend Deployment (10 min)

#### Create Web Service
- [ ] Go to https://dashboard.render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure service:
  - Name: `fraud-detection-api`
  - Region: `Oregon` (or nearest to you)
  - Root Directory: `backend`
  - Build Command: `./build.sh`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Add Environment Variables
- [ ] `DATABASE_URL` = (Supabase async connection string)
- [ ] `DATABASE_URL_SYNC` = (Supabase sync connection string)
- [ ] `API_KEY` = (generate random 32-char string)
- [ ] `MODEL_DIR` = `/opt/render/project/src/models`
- [ ] `FRAUD_THRESHOLD` = `0.10`
- [ ] `RATE_LIMIT_PER_SECOND` = `100`
- [ ] `LOG_LEVEL` = `INFO`

#### Deploy & Verify
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (~5-10 min)
- [ ] Copy backend URL: `https://fraud-detection-api-xxxx.onrender.com`
- [ ] Test health endpoint:
```bash
curl https://fraud-detection-api-xxxx.onrender.com/api/v1/health
```

---

### 4. Vercel Frontend Deployment (5 min)

#### Update Environment Variables
- [ ] Edit `frontend/.env.production`
- [ ] Set `VITE_API_URL` to your Render backend URL
```bash
VITE_API_URL=https://fraud-detection-api-xxxx.onrender.com/api/v1
```

#### Deploy to Vercel
- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Navigate to frontend: `cd frontend`
- [ ] Deploy: `vercel --prod`
- [ ] Or deploy via Vercel Dashboard: https://vercel.com/new

#### Verify Deployment
- [ ] Copy frontend URL: `https://fraud-detection-dashboard.vercel.app`
- [ ] Open in browser and verify dashboard loads
- [ ] Check API connection (should show metrics)

---

### 5. Upload Model Files (5 min)

Choose one method:

#### Option A: Git Commit (Recommended if <100MB)
```bash
git add backend/models/v6.0_model.pkl
git add backend/models/v6.0_metadata.json
git commit -m "Add trained model v6.0"
git push
```
- [ ] Wait for Render to redeploy automatically

#### Option B: Render Disk (If model >100MB)
- [ ] In Render Dashboard → Disks
- [ ] Add disk: mount to `/opt/render/project/src/models`
- [ ] Upload model files via SSH or API

#### Verify Model Loaded
```bash
curl https://fraud-detection-api-xxxx.onrender.com/api/v1/health
# Should show: "model_version": "6.0"
```

---

### 6. Update CORS Settings (2 min)
- [ ] Go to Render Dashboard → Environment
- [ ] Update `ALLOWED_ORIGINS` to include Vercel URL:
```
https://fraud-detection-dashboard.vercel.app,http://localhost:3000
```
- [ ] Save and redeploy

---

### 7. WooCommerce Plugin Configuration (5 min)

#### Install Plugin
- [ ] Upload `plugin/woo-fraud-detect.zip` to WordPress
- [ ] Activate plugin in WordPress admin

#### Configure Settings
- [ ] Go to WooCommerce → Fraud Detection
- [ ] Set API Endpoint: `https://fraud-detection-api-xxxx.onrender.com`
- [ ] Set Fraud Threshold: `0.10`
- [ ] Enable Auto-hold Fraud Orders
- [ ] Enable Email Notifications
- [ ] Click "Save Changes"

#### Verify Plugin
- [ ] Check API connection status (should show ✅ green)
- [ ] Create test order
- [ ] Verify fraud check in order notes

---

## Post-Deployment Testing

### Test 1: Health Check
```bash
curl https://fraud-detection-api-xxxx.onrender.com/api/v1/health
```
Expected:
```json
{
  "status": "healthy",
  "model_version": "6.0",
  "database": "connected"
}
```
- [ ] Status is "healthy"
- [ ] Model version is "6.0"
- [ ] Database is "connected"

---

### Test 2: Fraud Prediction API
```bash
curl -X POST https://fraud-detection-api-xxxx.onrender.com/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_id": "test_store",
    "amount": 2500.0,
    "payment_method": "credit_card",
    "user_id_hash": "test123",
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
- [ ] Returns `"label": "fraud"`
- [ ] Confidence > 0.90
- [ ] top_features array populated

---

### Test 3: Frontend Dashboard
- [ ] Visit `https://fraud-detection-dashboard.vercel.app`
- [ ] Dashboard loads without errors
- [ ] Metrics display (may show 0 initially)
- [ ] Test transaction form works
- [ ] Predictions show fraud/legitimate correctly

---

### Test 4: WooCommerce Integration
- [ ] Create legitimate order (low amount, existing customer)
  - Order should process normally
  - Order note shows "LEGITIMATE"
- [ ] Create fraud order (high amount, new user, different addresses)
  - Order should be held
  - Order note shows "FRAUD"
  - Admin email notification received

---

## Monitoring Setup (Optional)

### Uptime Monitoring
- [ ] Create [UptimeRobot](https://uptimerobot.com) account
- [ ] Add monitor for backend health endpoint
- [ ] Add monitor for frontend URL
- [ ] Configure email alerts

### Error Tracking
- [ ] Create [Sentry](https://sentry.io) account (optional)
- [ ] Add Sentry DSN to backend environment
- [ ] Add Sentry to frontend

### Database Monitoring
- [ ] Supabase Dashboard → Database → Health
- [ ] Check CPU, Memory, Active connections
- [ ] Set up alerts for 80% usage

---

## Security Review

- [ ] API_KEY is strong and random
- [ ] Database password is strong and unique
- [ ] CORS is restricted to specific domains (not *)
- [ ] No sensitive data in git history
- [ ] SSL/TLS enabled (automatic on Vercel/Render)
- [ ] Rate limiting enabled (100 req/s)

---

## Documentation Updates

- [ ] Update README.md with production URLs
- [ ] Document any custom configuration
- [ ] Add screenshots to PROJECT_DOCUMENTATION.md
- [ ] Create demo video (optional)

---

## Final Verification

- [ ] All tests passing ✅
- [ ] No errors in logs
- [ ] Performance acceptable (<500ms response)
- [ ] Email notifications working
- [ ] WooCommerce plugin operational

---

## 🎉 Deployment Complete!

**Your fraud detection system is now live:**

- 🎨 **Dashboard**: https://fraud-detection-dashboard.vercel.app
- ⚙️ **API**: https://fraud-detection-api-xxxx.onrender.com
- 📚 **API Docs**: https://fraud-detection-api-xxxx.onrender.com/docs
- 🛒 **WooCommerce**: Configured and active

**Next Steps:**
1. Share dashboard URL with stakeholders
2. Monitor initial transactions
3. Adjust fraud threshold if needed (0.1-0.5)
4. Set up weekly model retraining
5. Add to portfolio/resume

**Support:**
- Full guide: `DEPLOYMENT.md`
- Troubleshooting: See DEPLOYMENT.md → Troubleshooting section
- GitHub Issues: Create issue for bugs or questions

---

**Estimated Total Time: 30-45 minutes**

| Task | Time | Status |
|------|------|--------|
| Supabase setup | 5 min | ☐ |
| GitHub push | 2 min | ☐ |
| Render backend | 10 min | ☐ |
| Vercel frontend | 5 min | ☐ |
| Model upload | 5 min | ☐ |
| CORS update | 2 min | ☐ |
| WooCommerce config | 5 min | ☐ |
| Testing | 10 min | ☐ |
| **Total** | **44 min** | |
