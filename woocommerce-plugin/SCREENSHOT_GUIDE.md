# Screenshot Guide for User Manual
## Required Screenshots for PDF Conversion

This document lists all 24 screenshots needed to complete the user manual PDF. Follow the instructions for each screenshot.

---

## Screenshot Specifications

- **Format:** PNG or JPG
- **Resolution:** 1920x1080 or higher
- **Quality:** High (no compression artifacts)
- **Browser:** Use Chrome or Firefox
- **Zoom:** 100% (no browser zoom)

---

## Installation Screenshots

### SCREENSHOT 1: Downloaded ZIP file
**File:** `01-downloaded-zip.png`

**Instructions:**
1. Download the plugin ZIP file
2. Open your Downloads folder
3. Show the file: `wc-fraud-detection-v2.2.1-FIXED.zip`
4. Highlight or select the file
5. Take screenshot of the folder view

**What to capture:** File explorer/Finder window showing the downloaded ZIP file

---

### SCREENSHOT 2: Upload Plugin Screen
**File:** `02-upload-plugin.png`

**Instructions:**
1. Log into WordPress Admin
2. Go to **Plugins → Add New**
3. Click **"Upload Plugin"** button
4. Screenshot showing the upload interface with "Choose File" button

**What to capture:** WordPress plugin upload screen before selecting file

---

### SCREENSHOT 3: Plugin Activation
**File:** `03-activate-plugin.png`

**Instructions:**
1. After installing the plugin
2. Capture the "Plugin installed successfully" message
3. Show the **"Activate Plugin"** link/button

**What to capture:** Success message with activation button

---

### SCREENSHOT 4: WooCommerce Menu Items
**File:** `04-woocommerce-menu.png`

**Instructions:**
1. After activating plugin
2. Hover over **WooCommerce** in left sidebar
3. Show submenu with new items:
   - "Fraud Detection"
   - "Bulk Check (CSV)"
4. Highlight these two items

**What to capture:** WooCommerce submenu expanded showing new menu items

---

## Configuration Screenshots

### SCREENSHOT 5: Settings Page Full View
**File:** `05-settings-page-full.png`

**Instructions:**
1. Go to **WooCommerce → Fraud Detection**
2. Take full-page screenshot showing:
   - Page title "🛡️ AI Fraud Detection Settings"
   - All form fields
   - Save button
   - Test Connection button

**What to capture:** Complete settings page (may need scrolling screenshot tool)

---

### SCREENSHOT 6: API Endpoint Field
**File:** `06-api-endpoint.png`

**Instructions:**
1. On settings page
2. Focus on **"API Endpoint"** field
3. Fill in: `http://localhost:8000`
4. Crop to show just this section

**What to capture:** API Endpoint field with example value filled in

---

### SCREENSHOT 7: Fraud Threshold
**File:** `07-fraud-threshold.png`

**Instructions:**
1. On settings page
2. Focus on **"Fraud Threshold"** field
3. Set value to: `0.7`
4. Crop to show this field and description

**What to capture:** Threshold field with 0.7 value and description text

---

### SCREENSHOT 8: Automation Checkboxes
**File:** `08-automation-settings.png`

**Instructions:**
1. On settings page
2. Focus on three checkboxes:
   - "Enable automatic fraud detection"
   - "Automatically place suspicious orders on hold"
   - "Send email alerts when fraud detected"
3. All should be CHECKED
4. Crop to show all three with descriptions

**What to capture:** Three automation checkboxes, all enabled

---

### SCREENSHOT 9: Test Connection Success
**File:** `09-test-connection-success.png`

**Instructions:**
1. On settings page
2. Click **"Test Connection"** button
3. Wait for success response
4. Capture green success message showing:
   - "✅ Connection successful!"
   - Status: healthy
   - Model loaded: Yes

**What to capture:** Success notification box after testing connection

---

### SCREENSHOT 10: Settings Saved
**File:** `10-settings-saved.png`

**Instructions:**
1. After clicking "Save Settings"
2. Capture the WordPress admin notice:
   - "Settings saved." message at top of page

**What to capture:** Green success notification bar

---

## Usage Screenshots - Manual Check

### SCREENSHOT 11: Order List with Fraud Flag
**File:** `11-order-list-on-hold.png`

**Instructions:**
1. Go to **WooCommerce → Orders**
2. Find an order with "On Hold" status
3. If possible, show order that was flagged by fraud detection
4. Highlight the "On Hold" status

**What to capture:** Orders list showing at least one order on hold

---

### SCREENSHOT 12: Orders List
**File:** `12-orders-list.png`

**Instructions:**
1. Go to **WooCommerce → Orders**
2. Show typical orders list with multiple orders
3. Include different statuses (Processing, Completed, On Hold)

**What to capture:** Standard WooCommerce orders list page

---

### SCREENSHOT 13: Fraud Detection Box in Sidebar
**File:** `13-fraud-box-sidebar.png`

**Instructions:**
1. Open any order (click to edit)
2. Scroll to right sidebar
3. Find **"🛡️ AI Fraud Detection"** meta box
4. Highlight/circle the box

**What to capture:** Order edit screen with fraud detection box visible in sidebar

---

### SCREENSHOT 14: Check for Fraud Button
**File:** `14-check-button.png`

**Instructions:**
1. Open an order that hasn't been checked yet
2. Focus on fraud detection box
3. Show the **"🔍 Check for Fraud"** button
4. Crop closely to just the box

**What to capture:** Fraud detection box with unchecked state and button

---

### SCREENSHOT 15: Legitimate Order Results
**File:** `15-legitimate-result.png`

**Instructions:**
1. Check an order that comes back as legitimate
2. After page reloads, capture fraud detection box showing:
   - Last Check timestamp
   - Status: ✅ Legitimate
   - Confidence: ~90%+
   - Top Factors list
   - Latency

**What to capture:** Fraud detection box showing legitimate verdict

---

### SCREENSHOT 16: Fraud Detected Results
**File:** `16-fraud-result.png`

**Instructions:**
1. Check an order that comes back as fraud
2. Capture fraud detection box showing:
   - Status: 🚨 FRAUD DETECTED (in red)
   - Confidence: ~80%+
   - Top Factors list
   - Latency

**What to capture:** Fraud detection box showing fraud verdict in red

**Note:** You may need to create a test order with suspicious values:
- High amount: $5000
- New customer: yes
- Suspicious email: test@tempmail.com

---

## Bulk Upload Screenshots

### SCREENSHOT 17: Bulk Check Page
**File:** `17-bulk-check-page.png`

**Instructions:**
1. Go to **WooCommerce → Bulk Check (CSV)**
2. Take full-page screenshot showing:
   - Page title
   - CSV format requirements
   - Upload form
   - Download template button

**What to capture:** Full bulk check page before upload

---

### SCREENSHOT 18: CSV File Example
**File:** `18-csv-file-example.png`

**Instructions:**
1. Open `test-fraud-transactions.csv` in Excel or Notepad
2. Show the file with headers and several rows of data
3. Make sure formatting is clear

**What to capture:** CSV file opened showing proper format

**Alternative:** Use Excel and format as table for better visualization

---

### SCREENSHOT 19: Download Template Button
**File:** `19-download-template.png`

**Instructions:**
1. On bulk check page
2. Highlight the **"📥 Download CSV Template"** button
3. Crop to show button and surrounding text

**What to capture:** Template download button

---

### SCREENSHOT 20: File Selected
**File:** `20-file-selected.png`

**Instructions:**
1. On bulk check page
2. Click "Choose File" and select CSV
3. Show form with:
   - Filename displayed next to button
   - "🚀 Start Fraud Check" button ready to click

**What to capture:** Upload form with file selected

---

### SCREENSHOT 21: Progress Bar
**File:** `21-progress-bar.png`

**Instructions:**
1. Upload CSV and start checking
2. During processing, capture:
   - Progress bar at ~40-60%
   - Progress text showing "Processing batch X of Y"
   - Percentage and transaction count

**What to capture:** Active progress indicator mid-process

**Note:** This requires quick screenshot during upload. You may need to use a large CSV file to have enough time.

---

### SCREENSHOT 22: Results Summary Cards
**File:** `22-results-summary.png`

**Instructions:**
1. After bulk check completes
2. Scroll to results section
3. Capture the four summary cards:
   - 📊 Total Checked
   - 🚨 Fraud Detected
   - ✅ Legitimate
   - 💰 Fraud Amount

**What to capture:** Summary cards with statistics

---

### SCREENSHOT 23: Results Table
**File:** `23-results-table.png`

**Instructions:**
1. After bulk check completes
2. Scroll to results table
3. Show table with columns:
   - Order ID
   - Amount
   - Status (with colors)
   - Confidence
   - Top Factor

**What to capture:** Full results table with at least 5-10 rows

**Note:** Should include mix of legitimate and fraud results

---

### SCREENSHOT 24: Download Buttons
**File:** `24-download-buttons.png`

**Instructions:**
1. After bulk check completes
2. Focus on download section showing:
   - "⬇️ Download Results (CSV)" button
   - "⚠️ Download Fraud Only" button
3. Highlight both buttons

**What to capture:** Download buttons section

---

## Tips for Taking Screenshots

### Tools Recommended

**Windows:**
- **Greenshot** (free) - Best for annotations and cropping
- **Snagit** (paid) - Professional screenshots with editing
- **Windows Snipping Tool** - Built-in, basic

**Mac:**
- **Cmd+Shift+4** - Built-in screenshot tool
- **CleanShot X** (paid) - Professional tool
- **Skitch** (free) - Simple annotations

**Full-Page Screenshots:**
- **Awesome Screenshot** (Chrome extension)
- **GoFullPage** (Chrome extension)
- **Firefox built-in screenshot** (Right-click → Take Screenshot)

---

### Screenshot Workflow

1. **Prepare WordPress:**
   - Fresh data for clean screenshots
   - Close unnecessary browser tabs
   - Clear notifications
   - Use admin account

2. **Browser Setup:**
   - Use incognito/private window (clean cache)
   - Zoom: 100%
   - Hide bookmarks bar for cleaner look
   - Full screen or maximize window

3. **Naming Convention:**
   - Use provided filenames exactly
   - Format: `01-description.png`
   - Keep in order (01, 02, 03...)

4. **Quality Checks:**
   - No blurry text
   - Proper lighting (not too dark)
   - No sensitive information visible
   - Crop out unnecessary parts

5. **Annotations (optional):**
   - Red arrows pointing to important elements
   - Red boxes highlighting key areas
   - Keep minimal and professional

---

## After Capturing Screenshots

### Organization

Create folder structure:
```
screenshots/
  installation/
    01-downloaded-zip.png
    02-upload-plugin.png
    ...
  configuration/
    05-settings-page-full.png
    ...
  usage/
    11-order-list-on-hold.png
    ...
  bulk/
    17-bulk-check-page.png
    ...
```

### Verification Checklist

Before converting to PDF, verify:
- ✅ All 24 screenshots captured
- ✅ High quality (readable text)
- ✅ Correct filenames
- ✅ No sensitive data visible
- ✅ Consistent browser/theme
- ✅ All in same resolution (roughly)

---

## Inserting Screenshots into Manual

### Method 1: Markdown with Images

Replace placeholders in `USER_MANUAL.md`:

**Before:**
```markdown
**[SCREENSHOT 1: Downloaded ZIP file in downloads folder]**
```

**After:**
```markdown
![Downloaded ZIP file](screenshots/installation/01-downloaded-zip.png)
```

### Method 2: Convert to Word First

1. Convert Markdown to Word using Pandoc (see below)
2. Insert images manually in Word
3. Export Word to PDF

### Method 3: Use Markdown Editor

Use tools like:
- **Typora** - WYSIWYG Markdown editor, can export to PDF
- **Notion** - Import Markdown, add images, export PDF
- **GitBook** - Professional documentation platform

---

## Next Steps

1. ✅ Capture all 24 screenshots following this guide
2. ✅ Organize screenshots in folders
3. ✅ Insert images into USER_MANUAL.md
4. ✅ Convert to PDF (see PDF_CONVERSION_GUIDE.md)
5. ✅ Review final PDF for quality
6. ✅ Distribute to merchants

---

**Good luck with your screenshots!**

If you have questions about any specific screenshot, refer back to this guide or contact support.
