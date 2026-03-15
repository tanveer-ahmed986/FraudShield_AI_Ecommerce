# 🚀 Quick Installation Guide

Get the AI Fraud Detection plugin running in 5 minutes!

---

## 📋 Prerequisites

- WordPress 5.8+ installed
- WooCommerce 6.0+ installed and activated
- PHP 7.4+
- Fraud Detection API backend running (see [Backend Setup](#backend-setup))

---

## 🔧 Installation Methods

### Method 1: Upload ZIP (Recommended for Testing)

1. **Package the plugin:**

   ```powershell
   # Navigate to plugin directory
   cd D:\ai_projects\fraud_detection_system\woocommerce-plugin

   # Create ZIP file
   Compress-Archive -Path fraud-detection-plugin.php,readme.txt,README.md,LICENSE -DestinationPath wc-fraud-detection.zip -Force
   ```

2. **Install in WordPress:**
   - Go to WordPress Admin → Plugins → Add New
   - Click "Upload Plugin"
   - Choose `wc-fraud-detection.zip`
   - Click "Install Now"
   - Click "Activate Plugin"

### Method 2: Manual Installation

1. **Copy plugin files:**

   ```powershell
   # Copy to WordPress plugins directory
   Copy-Item -Path "D:\ai_projects\fraud_detection_system\woocommerce-plugin\fraud-detection-plugin.php" -Destination "C:\xampp\htdocs\wordpress\wp-content\plugins\wc-fraud-detection\" -Force
   Copy-Item -Path "D:\ai_projects\fraud_detection_system\woocommerce-plugin\readme.txt" -Destination "C:\xampp\htdocs\wordpress\wp-content\plugins\wc-fraud-detection\" -Force
   ```

2. **Activate in WordPress:**
   - Go to WordPress Admin → Plugins
   - Find "AI Fraud Detection for WooCommerce"
   - Click "Activate"

---

## ⚙️ Configuration

### Step 1: Access Settings

Go to **WooCommerce → Fraud Detection**

### Step 2: Configure API Connection

| Field | Value |
|-------|-------|
| **API Endpoint** | `http://localhost:8000` (local) or your cloud URL |
| **API Key** | Leave blank (optional for production) |
| **Fraud Threshold** | `0.7` (70% confidence) |
| **Auto-Hold Orders** | ✅ Checked |
| **Email Notifications** | ✅ Checked |

### Step 3: Test Connection

1. Click **"Test Connection"** button
2. You should see:
   ```
   ✅ Connection successful!
   Status: healthy
   Model loaded: Yes
   ```

3. If connection fails:
   - Verify backend is running: `docker ps`
   - Check API URL is correct
   - Check firewall/network settings

### Step 4: Save Settings

Click **"Save Settings"**

---

## 🖥️ Backend Setup

The plugin requires the fraud detection API backend.

### Quick Start with Docker

```powershell
# Clone repository (if not already done)
cd D:\ai_projects\fraud_detection_system

# Start backend services
docker compose up -d

# Verify services are running
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE                           STATUS         PORTS
abc123...      fraud_detection_system-backend  Up 2 minutes   0.0.0.0:8000->8000/tcp
def456...      postgres:15-alpine              Up 2 minutes   0.0.0.0:5432->5432/tcp
```

### Verify API Health

```powershell
# Test API endpoint
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "v6.0",
  "database": "connected"
}
```

---

## ✅ Testing

### Test 1: Legitimate Order

1. Go to your WooCommerce store
2. Add product to cart
3. Proceed to checkout
4. Fill normal checkout details:
   - Name: John Doe
   - Email: john@gmail.com
   - Address: Valid address
   - Payment: Credit Card
5. Complete order
6. Go to WooCommerce → Orders
7. Open the order
8. Check "AI Fraud Detection" meta box:
   ```
   ✅ Legitimate
   Fraud Risk: 15.2%

   Top Factors:
   - amount: Normal range
   - is_new_user: False
   - payment_method: credit_card

   Checked: 2026-03-15 10:30:00
   ```

### Test 2: Suspicious Order (Simulated)

Create a test scenario that triggers fraud detection:

1. Use a new customer account
2. Order high-value item ($500+)
3. Use unusual email domain (e.g., temp-mail.com)
4. Complete checkout at odd hours (3 AM)
5. Check order:
   ```
   🚨 FRAUD DETECTED
   Confidence: 87.3%

   Top Factors:
   - amount: 999.99 (unusual for new customer)
   - is_new_user: True (suspicious)
   - hour_of_day: 3 (risky time)

   Checked: 2026-03-15 03:15:00
   ```
6. Order should be automatically on hold
7. Check your email for fraud alert

### Test 3: API Unavailable

1. Stop the backend:
   ```powershell
   docker compose down
   ```
2. Place an order
3. Check order notes:
   ```
   ⚠️ Fraud detection API unavailable. Order requires manual review.
   ```
4. Restart backend:
   ```powershell
   docker compose up -d
   ```

---

## 📊 Dashboard Usage

### Orders List

The orders page now shows fraud indicators:

| Icon | Meaning |
|------|---------|
| ✅ | Legitimate (passed fraud check) |
| 🚨 | Fraud detected (high confidence) |
| ⚠️ | API error (manual review needed) |
| — | Not checked |

### Order Edit Page

Each order has a "AI Fraud Detection" meta box showing:
- Fraud verdict (Legitimate / FRAUD DETECTED)
- Confidence score
- Top 3 contributing factors
- Timestamp of check

### Email Notifications

When fraud is detected, admin receives:

```
Subject: [Fraud Alert] Order #1234 - 87.3% confidence

🚨 Fraud Detection Alert

Order ID: #1234
Customer: John Doe
Email: john@example.com
Amount: $999.99
Fraud Confidence: 87.3%

Top Contributing Factors:
- amount: Unusually high
- is_new_user: True
- hour_of_day: 3am

View Order: [link]
```

---

## 🔧 Troubleshooting

### Plugin Not Appearing

**Problem:** Plugin doesn't show in Plugins list

**Solution:**
1. Check file permissions
2. Verify `fraud-detection-plugin.php` exists
3. Check for PHP errors in WordPress debug log

### API Connection Failed

**Problem:** "Connection failed" error when testing

**Solutions:**

1. **Backend not running:**
   ```powershell
   docker compose up -d
   ```

2. **Wrong API URL:**
   - Check settings: http://localhost:8000 (no trailing slash)
   - Verify port 8000 is accessible

3. **Firewall blocking:**
   - Add exception for port 8000
   - Check Windows Defender Firewall

4. **Docker issues:**
   ```powershell
   # Restart Docker
   docker compose restart

   # Check logs
   docker compose logs backend
   ```

### No Fraud Detection on Orders

**Problem:** Orders don't have fraud detection meta box

**Solutions:**

1. Check plugin is activated
2. Verify API endpoint is configured
3. Check WooCommerce is active
4. Review order notes for error messages

### False Positives

**Problem:** Too many legitimate orders flagged as fraud

**Solution:**
1. Increase threshold: 0.7 → 0.8 or 0.9
2. Retrain model with more data
3. Review top contributing factors

### False Negatives

**Problem:** Fraudulent orders not detected

**Solution:**
1. Decrease threshold: 0.7 → 0.5 or 0.6
2. Retrain model with labeled fraud examples
3. Add more features (if customizing)

---

## 📞 Support

### Documentation
- **Plugin README:** [README.md](README.md)
- **Publishing Guide:** [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)
- **Main Project:** https://github.com/tanveer-ahmed986/fraud_detection_system_ecommerce

### Report Issues
- **GitHub Issues:** https://github.com/tanveer-ahmed986/fraud_detection_system_ecommerce/issues
- **Email:** tanveer030402@gmail.com

---

## 🎉 Success!

Your WooCommerce store is now protected with AI-powered fraud detection!

**Next Steps:**
- Monitor orders for fraud alerts
- Review flagged orders manually
- Adjust threshold based on results
- Retrain model with real data over time

**Need to publish?** See [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)
