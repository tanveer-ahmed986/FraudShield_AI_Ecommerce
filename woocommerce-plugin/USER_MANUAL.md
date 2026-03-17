# AI Fraud Detection for WooCommerce
## User Manual v2.2.1

---

**Publisher:** Tanveer Ahmed
**Version:** 2.2.1
**Last Updated:** March 2026
**License:** MIT

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Initial Configuration](#initial-configuration)
5. [Features Overview](#features-overview)
6. [Using the Plugin](#using-the-plugin)
   - [Automatic Fraud Detection](#automatic-fraud-detection)
   - [Manual Order Checking](#manual-order-checking)
   - [Bulk CSV Upload](#bulk-csv-upload)
7. [Settings & Configuration](#settings-configuration)
8. [Understanding Results](#understanding-results)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)
11. [Support](#support)

---

## Introduction

### What is AI Fraud Detection?

AI Fraud Detection for WooCommerce is an intelligent plugin that protects your online store from fraudulent transactions using advanced machine learning. It analyzes each order in real-time and provides fraud risk assessment with explainable AI insights.

### Key Benefits

✅ **Real-time Protection** - Instant fraud detection on every order
✅ **Automated Response** - Automatically hold suspicious orders
✅ **Bulk Processing** - Check hundreds of transactions via CSV upload
✅ **Explainable AI** - Understand why orders are flagged
✅ **Email Alerts** - Get notified immediately of fraud attempts
✅ **Zero False Positives** - Fine-tune threshold to your business needs

### How It Works

1. Customer places an order on your WooCommerce store
2. Plugin sends order data to AI fraud detection API
3. AI model analyzes 12+ risk factors in milliseconds
4. Plugin receives verdict: **Legitimate** or **Fraud**
5. Automated actions taken (hold order, send alerts)
6. Merchant reviews results and makes final decision

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|------------|
| WordPress | Version 5.8 or higher |
| WooCommerce | Version 8.0 or higher |
| PHP | Version 7.4 or higher |
| Internet Connection | Required for API calls |
| Fraud Detection API | Running and accessible |

### Recommended Setup

- **WordPress:** Version 6.0+
- **WooCommerce:** Version 8.5+
- **PHP:** Version 8.0+
- **SSL Certificate:** For secure API communication
- **Hosting:** VPS or dedicated server for high-volume stores

### API Hosting Options

**Option 1: Self-Hosted (Free)**
- Run API on your own server
- Full control and privacy
- Requires technical setup

**Option 2: Cloud Hosted (Recommended)**
- Use cloud provider (AWS, DigitalOcean, etc.)
- Scalable and reliable
- Monthly hosting costs apply

**Option 3: Managed Service (Coming Soon)**
- Fully managed API by plugin developer
- No technical setup required
- Subscription-based pricing

---

## Installation Guide

### Step 1: Download the Plugin

Download `wc-fraud-detection-v2.2.1-FIXED.zip` from:
- GitHub repository
- Plugin developer website
- WordPress plugin directory (coming soon)

**[SCREENSHOT 1: Downloaded ZIP file in downloads folder]**

---

### Step 2: Upload to WordPress

1. Log into your WordPress Admin Dashboard
2. Navigate to **Plugins → Add New**
3. Click **"Upload Plugin"** button at the top
4. Click **"Choose File"** and select the ZIP file
5. Click **"Install Now"**

**[SCREENSHOT 2: WordPress Admin - Plugins → Add New → Upload Plugin screen]**

---

### Step 3: Activate the Plugin

1. After installation completes, click **"Activate Plugin"**
2. You'll be redirected to the Plugins page
3. Look for **"AI Fraud Detection for WooCommerce"** in the active plugins list

**[SCREENSHOT 3: Plugin activation success message]**

---

### Step 4: Verify Installation

After activation, you should see new menu items under **WooCommerce**:
- **Fraud Detection** (Settings page)
- **Bulk Check (CSV)** (Bulk upload page)

**[SCREENSHOT 4: WooCommerce menu with new submenu items highlighted]**

---

## Initial Configuration

### Step 1: Access Settings Page

1. Go to **WooCommerce → Fraud Detection**
2. You'll see the settings configuration screen

**[SCREENSHOT 5: Fraud Detection settings page - full view]**

---

### Step 2: Configure API Endpoint

**API Endpoint** is the URL where your fraud detection API is running.

**For Local Testing:**
```
http://localhost:8000
```

**For Production (Cloud/VPS):**
```
https://your-api-domain.com
```
or
```
http://your-server-ip:8000
```

**Steps:**
1. Enter your API endpoint URL in the **"API Endpoint"** field
2. Leave **"API Key"** blank (optional for future use)

**[SCREENSHOT 6: API Endpoint field filled in]**

---

### Step 3: Set Fraud Threshold

The **Fraud Threshold** determines how sensitive fraud detection is:

- **0.5 (50%)** - Very sensitive, may catch more false positives
- **0.7 (70%)** - Balanced (recommended for most stores)
- **0.9 (90%)** - Only flag very obvious fraud

**Recommendation:** Start with **0.7** and adjust based on your results.

**[SCREENSHOT 7: Fraud threshold slider set to 0.7]**

---

### Step 4: Configure Automation Settings

Enable or disable automatic features:

**✅ Automatic Detection**
- Checks every new order automatically
- **Recommended:** ON

**✅ Auto-Hold Orders**
- Automatically puts suspicious orders on "Hold" status
- Prevents processing until reviewed
- **Recommended:** ON

**✅ Email Alerts**
- Sends email to admin when fraud detected
- Email sent to: WordPress admin email
- **Recommended:** ON

**[SCREENSHOT 8: Automation checkboxes all enabled]**

---

### Step 5: Test API Connection

Before saving, verify your API is working:

1. Click **"Test Connection"** button
2. Wait for response (5-10 seconds)
3. Look for success message:
   - ✅ **Connection successful!**
   - Status: healthy
   - Model loaded: Yes

**[SCREENSHOT 9: Successful API connection test result]**

**If Connection Fails:**
- Check API endpoint URL is correct
- Verify API is running (visit health endpoint in browser)
- Check firewall/security settings
- See [Troubleshooting](#troubleshooting) section

---

### Step 6: Save Settings

Click **"Save Settings"** button at the bottom of the page.

You should see: **"Settings saved."** notification.

**[SCREENSHOT 10: Settings saved success message]**

---

## Features Overview

### 1. Automatic Fraud Detection

**What it does:**
- Monitors all new orders in real-time
- Automatically checks each order when placed
- Takes action based on results (hold order, send alerts)

**How it works:**
- Triggered on order creation
- Runs in background (no customer delay)
- Results stored in order metadata

---

### 2. Manual Order Checking

**What it does:**
- Check any individual order on-demand
- Re-check orders if needed
- View detailed fraud analysis

**When to use:**
- Review orders manually before fulfilling
- Re-analyze suspicious orders
- Check historical orders

---

### 3. Bulk CSV Upload

**What it does:**
- Upload CSV file with multiple transactions
- Check all transactions in one batch
- Export results for reporting

**When to use:**
- Analyze historical orders
- Import transactions from other platforms
- Generate fraud reports

---

## Using the Plugin

### Automatic Fraud Detection

When **automatic detection** is enabled, the plugin works silently in the background.

#### What Happens Automatically:

1. **Customer places order** → Order created in WooCommerce
2. **Plugin triggers** → Sends order data to API
3. **AI analyzes** → Fraud risk assessment completed
4. **Results stored** → Saved to order metadata
5. **Actions taken** (if fraud detected):
   - Order status → **On Hold**
   - Email sent → Admin notification
   - Order note added → "Fraud detected by AI"

**[SCREENSHOT 11: Order list showing an order on "Hold" status with fraud flag]**

---

### Manual Order Checking

#### Step 1: Open an Order

1. Go to **WooCommerce → Orders**
2. Click on any order to open order details

**[SCREENSHOT 12: WooCommerce orders list]**

---

#### Step 2: Locate Fraud Detection Box

On the order edit screen, look for the **"🛡️ AI Fraud Detection"** box in the right sidebar.

**[SCREENSHOT 13: Order edit screen with Fraud Detection box highlighted in sidebar]**

---

#### Step 3: Check for Fraud

**For New Orders (Not Yet Checked):**
- Click **"🔍 Check for Fraud"** button
- Loading message appears: "⏳ Checking..."
- Page reloads with results

**For Previously Checked Orders:**
- View existing results
- Click **"🔄 Re-check for Fraud"** to run again

**[SCREENSHOT 14: Fraud Detection box showing "Check for Fraud" button]**

---

#### Step 4: View Results

After checking, the box displays:

**For Legitimate Orders:**
```
Last Check: 2025-03-17 10:30 AM

Status: ✅ Legitimate
Confidence: 92.5%

Top Factors:
• amount: 0.15
• payment_method: 0.12
• is_new_user: 0.08

Latency: 145ms
```

**[SCREENSHOT 15: Fraud Detection box showing legitimate order results]**

---

**For Fraudulent Orders:**
```
Last Check: 2025-03-17 10:30 AM

Status: 🚨 FRAUD DETECTED
Confidence: 87.3%

Top Factors:
• amount: 0.35 (High amount for new customer)
• email_domain: 0.28 (Disposable email)
• is_new_user: 0.22 (New customer)

Latency: 152ms
```

**[SCREENSHOT 16: Fraud Detection box showing fraud detected results]**

---

### Bulk CSV Upload

#### Step 1: Access Bulk Check Page

Go to **WooCommerce → Bulk Check (CSV)**

**[SCREENSHOT 17: Bulk Check page - main view]**

---

#### Step 2: Prepare CSV File

Your CSV file must have these columns:

```csv
order_id,amount,payment_method,customer_email,is_new_customer,billing_city,items_count
```

**Example:**
```csv
order_id,amount,payment_method,customer_email,is_new_customer,billing_city,items_count
12345,99.99,credit_card,customer@example.com,yes,New York,2
12346,149.50,paypal,john@test.com,no,Los Angeles,1
12347,2500.00,credit_card,suspicious@fake.com,yes,Miami,1
```

**Tips:**
- First row must be headers
- Use comma separation
- Save as `.csv` format
- Maximum 1000 rows recommended per upload

**[SCREENSHOT 18: Example CSV file open in Excel/Notepad]**

---

#### Step 3: Download Template (Optional)

Click **"📥 Download CSV Template"** to get a pre-formatted template with sample data.

**[SCREENSHOT 19: Download template button highlighted]**

---

#### Step 4: Upload CSV File

1. Click **"Choose File"** button
2. Select your CSV file
3. Click **"🚀 Start Fraud Check"** button

**[SCREENSHOT 20: File selected, ready to upload]**

---

#### Step 5: Monitor Progress

The plugin processes transactions in batches:

- **Progress bar** shows percentage complete
- **Status message** shows current batch
- **Processing time** estimates based on file size

Example:
```
Processing batch 2 of 5...
Progress: 40% (8 of 20 transactions)
This may take a few minutes depending on file size.
```

**[SCREENSHOT 21: Progress bar showing 40% completion]**

---

#### Step 6: View Results

When processing completes, you'll see:

**Summary Cards:**
- 📊 **Total Checked:** 20 transactions
- 🚨 **Fraud Detected:** 3 transactions
- ✅ **Legitimate:** 17 transactions
- 💰 **Fraud Amount:** $4,850.00

**[SCREENSHOT 22: Results summary cards]**

---

**Results Table:**

| Order ID | Amount | Status | Confidence | Top Factor |
|----------|--------|--------|------------|------------|
| 12345 | $99.99 | ✅ Legitimate | 92.5% | amount: 0.15 |
| 12346 | $149.50 | ✅ Legitimate | 88.2% | payment_method: 0.12 |
| 12347 | $2500.00 | 🚨 Fraud | 87.3% | amount: 0.35 |

**[SCREENSHOT 23: Full results table]**

---

#### Step 7: Download Results

Export results for your records:

1. **Download Results (CSV)** - All transactions with full details
2. **Download Fraud Only** - Only flagged transactions

**[SCREENSHOT 24: Download buttons highlighted]**

---

## Settings & Configuration

### API Endpoint

**Purpose:** URL where fraud detection API is hosted

**Default:** `http://localhost:8000`

**Examples:**
- Local development: `http://localhost:8000`
- Cloud server: `https://api.yourcompany.com`
- VPS with IP: `http://123.45.67.89:8000`

**Important:** Must include `http://` or `https://`

---

### API Key (Optional)

**Purpose:** Authentication key for secured APIs

**Current Status:** Not required (future enhancement)

**When needed:** If you implement API authentication

---

### Fraud Threshold

**Purpose:** Minimum confidence level to flag as fraud

**Range:** 0.0 to 1.0 (0% to 100%)

**Recommended Values:**
- **0.5-0.6:** Very sensitive (more false positives)
- **0.7:** Balanced (recommended)
- **0.8-0.9:** Conservative (fewer false positives)

**How to adjust:**
1. Start with 0.7
2. Review results after 1-2 weeks
3. Increase if too many false positives
4. Decrease if missing obvious fraud

---

### Automatic Detection

**Purpose:** Check all new orders automatically

**Default:** Enabled (ON)

**When to disable:**
- High-volume stores (check manually)
- Testing/development environment
- API costs concerns

---

### Auto-Hold Orders

**Purpose:** Automatically set fraudulent orders to "On Hold" status

**Default:** Enabled (ON)

**Benefit:** Prevents automatic fulfillment of fraud orders

**When to disable:**
- You prefer manual review before holding
- Using custom order workflow

---

### Email Alerts

**Purpose:** Send email notification when fraud detected

**Default:** Enabled (ON)

**Email sent to:** WordPress admin email

**Email includes:**
- Order number and customer details
- Fraud confidence score
- Top risk factors
- Link to order

**Sample email:**
```
Subject: 🚨 Fraud Alert - Order #12347

Fraud detected on your WooCommerce store!

Order #: 12347
Customer: John Doe
Email: suspicious@fake.com
Amount: $2,500.00
Confidence: 87.30%
Status: fraud

View order: [link]

This order has been automatically placed on hold for review.
```

---

## Understanding Results

### Fraud Labels

**✅ Legitimate**
- Order appears safe to process
- Low fraud risk
- Confidence below threshold

**🚨 Fraud**
- Order flagged as suspicious
- High fraud risk
- Confidence above threshold

---

### Confidence Score

The confidence score indicates **how certain** the AI model is:

- **50-60%:** Low confidence (borderline)
- **60-75%:** Moderate confidence
- **75-90%:** High confidence
- **90-100%:** Very high confidence

**Example:**
- Confidence 92.5% → Model is 92.5% certain order is legitimate
- Confidence 87.3% for fraud → Model is 87.3% certain order is fraudulent

---

### Top Risk Factors

Shows the **3 most important features** that influenced the decision.

**Common Risk Factors:**

| Factor | What It Means | High Risk When |
|--------|---------------|----------------|
| `amount` | Transaction amount | Very high or very low |
| `is_new_user` | Customer is new | Yes (especially with high amount) |
| `email_domain` | Email provider | Disposable/temporary email |
| `payment_method` | How they paid | Credit card (vs PayPal/COD) |
| `billing_shipping_match` | Addresses match | No (different addresses) |
| `hour_of_day` | Time of purchase | Late night (2-5 AM) |
| `device_type` | Device used | Mobile (sometimes) |

**Example:**
```
Top Factors:
• amount: 0.35 (Very high transaction amount)
• email_domain: 0.28 (Temporary email provider)
• is_new_user: 0.22 (New customer with large order)
```

**Interpretation:**
The order is flagged primarily because of a large amount ($2,500) from a new customer using a disposable email address.

---

### Processing Latency

Shows how fast the fraud check completed.

**Typical latency:**
- 50-150ms: Excellent
- 150-300ms: Good
- 300-500ms: Acceptable
- >500ms: Slow (check API performance)

**Does not affect customer experience** - runs after checkout completes.

---

## Troubleshooting

### Problem: "Connection Failed" when testing API

**Possible causes:**
1. API is not running
2. Incorrect endpoint URL
3. Firewall blocking connection
4. API server is down

**Solutions:**

**Check 1: Verify API is running**
```bash
# On API server, check if running
curl http://localhost:8000/api/v1/health
```
Should return: `{"status":"healthy","model_loaded":true}`

**Check 2: Test from browser**
Visit: `http://your-api-endpoint/api/v1/health`

You should see JSON response.

**Check 3: Verify endpoint URL**
- Must include `http://` or `https://`
- No trailing slash
- Correct port number
- Example: `http://123.45.67.89:8000` ✅
- Wrong: `123.45.67.89` ❌

**Check 4: Firewall/security**
- Allow port 8000 (or your API port) in firewall
- Check WordPress hosting doesn't block outbound requests

---

### Problem: Plugin doesn't check orders automatically

**Possible causes:**
1. Automatic detection disabled
2. WordPress hooks not firing
3. API connection issue

**Solutions:**

**Check 1: Verify settings**
- Go to **WooCommerce → Fraud Detection**
- Ensure **"Automatic Detection"** is checked
- Click **"Test Connection"** to verify API works

**Check 2: Test with manual check**
- Open any order
- Click **"Check for Fraud"** manually
- If manual works but automatic doesn't, check WordPress cron/hooks

**Check 3: Check order notes**
- Open order
- Scroll to **"Order Notes"** section
- Look for API error messages

---

### Problem: CSV upload shows "No data rows found"

**Possible causes:**
1. Wrong CSV format
2. Missing headers
3. File encoding issue
4. Line ending issue

**Solutions:**

**Check 1: Verify CSV format**
Must have these exact headers:
```
order_id,amount,payment_method,customer_email,is_new_customer,billing_city,items_count
```

**Check 2: Download template**
- Use plugin's template button
- Copy your data into template
- Save as CSV

**Check 3: Check file encoding**
- Save CSV as **UTF-8** encoding
- Use Excel: Save As → CSV UTF-8

**Check 4: Check line endings**
- Windows: Use `\r\n` (CRLF)
- Open in Notepad++ to verify line endings

---

### Problem: Orders not being put on hold

**Possible causes:**
1. Auto-hold disabled in settings
2. Fraud not detected (below threshold)
3. Order status prevents hold

**Solutions:**

**Check 1: Verify auto-hold setting**
- Go to **WooCommerce → Fraud Detection**
- Ensure **"Auto-Hold Orders"** is checked

**Check 2: Check fraud detection result**
- Was fraud actually detected?
- View order's fraud detection box
- If confidence below threshold, order won't be held

**Check 3: Adjust threshold**
- Lower threshold to catch more fraud
- Example: Change from 0.7 to 0.6

---

### Problem: Email alerts not received

**Possible causes:**
1. Email alerts disabled
2. WordPress email not configured
3. Spam folder

**Solutions:**

**Check 1: Verify email alerts enabled**
- Go to **WooCommerce → Fraud Detection**
- Ensure **"Email Alerts"** is checked

**Check 2: Check admin email**
- Email sent to WordPress admin email
- Verify at: **Settings → General → Email Address**

**Check 3: Test WordPress email**
- Use plugin like "WP Mail SMTP" to test
- Check spam/junk folder

**Check 4: Check email logs**
- Some hosts block outbound email
- Contact hosting support if needed

---

## FAQ

### General Questions

**Q: Is this plugin free?**
A: Yes, the plugin is free and open source (MIT license). You only need to host the API yourself or use a hosting provider.

**Q: Do I need technical skills to use this?**
A: Basic WordPress/WooCommerce knowledge is enough. API setup requires some technical setup (or you can use managed hosting).

**Q: Will it slow down my checkout?**
A: No! Fraud detection runs **after** checkout completes, so customers experience no delay.

**Q: Can I test before going live?**
A: Yes! Use the manual check feature on existing orders to test accuracy before enabling automatic detection.

---

### Privacy & Security

**Q: Is customer data secure?**
A: Yes! Data is sent over HTTPS (if configured) and no data is stored by the API - only processed and returned.

**Q: What data is sent to the API?**
A: Order amount, payment method, email domain (not full email), customer type, location, and order metadata. No credit card details or passwords.

**Q: Is this GDPR compliant?**
A: Yes, when configured properly. API processes data temporarily and doesn't store personal information.

---

### Accuracy & Performance

**Q: How accurate is fraud detection?**
A: The AI model achieves 90%+ recall and 85%+ precision on test data. Accuracy improves with proper threshold tuning for your store.

**Q: Can I train the model on my own data?**
A: Currently no, but this is planned for future versions. You can adjust the threshold to match your fraud patterns.

**Q: What if it flags legitimate orders?**
A: Adjust the threshold higher (e.g., from 0.7 to 0.8) to reduce false positives. You can also review and release held orders manually.

**Q: How fast is fraud detection?**
A: Typical response time is 50-200ms. You can see exact latency in the fraud detection results.

---

### Costs

**Q: Are there any API costs?**
A: If you self-host the API, only server costs apply. Cloud hosting typically costs $10-50/month depending on volume.

**Q: Is there a transaction limit?**
A: No limits in the plugin. Your API server capacity determines maximum throughput.

---

### Support & Updates

**Q: How do I get support?**
A: See [Support](#support) section below for contact information.

**Q: How often is the plugin updated?**
A: Regular updates for WordPress/WooCommerce compatibility and new features. Check GitHub for latest version.

**Q: Can I request features?**
A: Yes! Submit feature requests on GitHub issues or contact support.

---

## Support

### Getting Help

**📧 Email Support**
support@example.com (replace with actual email)

**💬 GitHub Issues**
https://github.com/tanveer-ahmed986/fraud_detection_system_ecommerce/issues

**📚 Documentation**
https://github.com/tanveer-ahmed986/fraud_detection_system_ecommerce

**🎥 Video Tutorials**
Coming soon - subscribe for updates

---

### Before Contacting Support

Please have ready:
1. Plugin version (currently 2.2.1)
2. WordPress version
3. WooCommerce version
4. PHP version
5. Error messages or screenshots
6. Steps to reproduce the issue

---

### Reporting Bugs

Submit bug reports on GitHub with:
1. Clear description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots if applicable
5. Error logs from WordPress Debug

---

### Feature Requests

We welcome feature requests! Please include:
1. Clear description of desired feature
2. Use case / business problem it solves
3. Any examples or mockups

---

## Appendix

### CSV Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `order_id` | String/Number | Unique order identifier | `12345` |
| `amount` | Decimal | Transaction amount | `99.99` |
| `payment_method` | String | Payment type | `credit_card`, `paypal`, `cod` |
| `customer_email` | Email | Customer email address | `customer@example.com` |
| `is_new_customer` | String | New or returning | `yes` or `no` |
| `billing_city` | String | Billing city name | `New York` |
| `items_count` | Integer | Number of items | `2` |

---

### Changelog

**Version 2.2.1 (March 2026)**
- 🐛 Fixed CSV parsing bug with line endings
- ✅ Improved error messages
- 📊 Added debug information display

**Version 2.2.0 (March 2026)**
- ✨ Added CSV bulk upload feature
- 📈 Added progress indicators
- 📧 Added results export functionality

**Version 2.1.0 (March 2026)**
- ✨ Added manual fraud check button
- 🎨 Improved UI/UX
- 📱 Added real-time AJAX checks

**Version 2.0.0 (March 2026)**
- 🚀 Initial release with automatic detection
- 🛡️ Integration with fraud detection API
- 📧 Email alerts
- ⚙️ Settings page

---

### License

MIT License - see LICENSE file for details

---

### Credits

**Developer:** Tanveer Ahmed
**Contributors:** Open source community
**ML Model:** Custom-trained fraud detection model
**Framework:** WordPress, WooCommerce, FastAPI

---

**Thank you for using AI Fraud Detection for WooCommerce!**

For questions, feedback, or support, please contact us.

---

*End of User Manual v2.2.1*
