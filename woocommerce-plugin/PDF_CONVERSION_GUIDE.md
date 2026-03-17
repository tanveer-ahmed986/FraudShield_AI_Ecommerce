# PDF Conversion Guide
## How to Convert USER_MANUAL.md to PDF

This guide explains multiple methods to convert the Markdown user manual to a professional PDF document.

---

## Prerequisites

Before starting, you should have:
- ✅ `USER_MANUAL.md` file
- ✅ All 24 screenshots captured (see `SCREENSHOT_GUIDE.md`)
- ✅ Screenshots inserted into the Markdown file

---

## Method 1: Using Pandoc (Recommended)

### What is Pandoc?
Pandoc is a powerful document converter that creates professional PDFs from Markdown.

### Installation

**Windows:**
```bash
# Using Chocolatey
choco install pandoc

# Or download from: https://pandoc.org/installing.html
```

**Mac:**
```bash
brew install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
```

### Basic Conversion

Navigate to plugin folder and run:

```bash
cd D:\ai_projects\fraud_detection_system\woocommerce-plugin

pandoc USER_MANUAL.md -o USER_MANUAL.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2
```

### Professional Conversion with Styling

Create a file called `pandoc-template.yaml`:

```yaml
---
title: "AI Fraud Detection for WooCommerce"
subtitle: "User Manual v2.2.1"
author: "Tanveer Ahmed"
date: "March 2025"
toc: true
toc-depth: 2
documentclass: article
geometry: "margin=1in"
fontsize: 11pt
linestretch: 1.25
papersize: letter
---
```

Then convert:

```bash
pandoc pandoc-template.yaml USER_MANUAL.md -o USER_MANUAL.pdf \
  --pdf-engine=xelatex \
  --highlight-style=tango \
  -V geometry:margin=1in \
  -V linkcolor:blue
```

### With Custom CSS (HTML → PDF)

Create `manual-style.css`:

```css
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

h2 {
    color: #34495e;
    margin-top: 30px;
}

code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
}

pre {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

table th {
    background: #3498db;
    color: white;
    padding: 10px;
    text-align: left;
}

table td {
    padding: 8px;
    border-bottom: 1px solid #ddd;
}

img {
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
    margin: 10px 0;
}

.screenshot-caption {
    font-style: italic;
    color: #666;
    text-align: center;
    margin-top: 5px;
}
```

Convert to HTML first, then PDF:

```bash
# Convert to HTML with CSS
pandoc USER_MANUAL.md -o USER_MANUAL.html \
  --css=manual-style.css \
  --standalone \
  --toc

# Then convert HTML to PDF using browser or wkhtmltopdf
wkhtmltopdf --enable-local-file-access USER_MANUAL.html USER_MANUAL.pdf
```

---

## Method 2: Using Typora (WYSIWYG)

### What is Typora?
Typora is a Markdown editor with built-in PDF export.

### Installation
Download from: https://typora.io/

### Steps

1. **Open Typora**
2. **File → Open** → Select `USER_MANUAL.md`
3. **Insert Screenshots:**
   - Where you see `[SCREENSHOT X: ...]`
   - Click **Format → Image → Insert Image**
   - Select screenshot file
   - Repeat for all screenshots
4. **File → Export → PDF**
5. **Configure settings:**
   - Page size: Letter or A4
   - Margins: Normal
   - Include table of contents: Yes
6. **Export**

**Pros:**
- ✅ Easy to use
- ✅ WYSIWYG editing
- ✅ Clean output
- ✅ No command line needed

**Cons:**
- ❌ Not free (one-time purchase)
- ❌ Less customization

---

## Method 3: Using Google Docs

### Steps

1. **Convert Markdown to Word:**
   ```bash
   pandoc USER_MANUAL.md -o USER_MANUAL.docx
   ```

2. **Upload to Google Drive:**
   - Open Google Drive
   - Upload `USER_MANUAL.docx`

3. **Open with Google Docs:**
   - Right-click file
   - Open with → Google Docs

4. **Insert Screenshots:**
   - Where you see `[SCREENSHOT X: ...]`
   - Delete placeholder text
   - Insert → Image → Upload from computer
   - Select screenshot
   - Repeat for all 24 screenshots

5. **Format (if needed):**
   - Adjust image sizes
   - Add page breaks
   - Format headings

6. **Export to PDF:**
   - File → Download → PDF Document

**Pros:**
- ✅ Free
- ✅ Easy to use
- ✅ Collaborative (share with team)
- ✅ Cloud storage

**Cons:**
- ❌ Manual screenshot insertion
- ❌ May lose some formatting

---

## Method 4: Using Microsoft Word

### Steps

1. **Convert Markdown to Word:**
   ```bash
   pandoc USER_MANUAL.md -o USER_MANUAL.docx \
     --reference-doc=custom-reference.docx
   ```

2. **Open in Word:**
   - Open `USER_MANUAL.docx`

3. **Insert Screenshots:**
   - Find placeholder text `[SCREENSHOT X: ...]`
   - Delete placeholder
   - Insert → Pictures → This Device
   - Select screenshot
   - Resize and position
   - Repeat for all screenshots

4. **Format:**
   - Apply consistent styles
   - Add headers/footers
   - Add page numbers
   - Table of contents (References → Table of Contents)

5. **Export to PDF:**
   - File → Save As → PDF
   - Or File → Export → Create PDF/XPS

**Pros:**
- ✅ Professional output
- ✅ Full control over formatting
- ✅ Familiar interface

**Cons:**
- ❌ Requires Microsoft Word
- ❌ More manual work

---

## Method 5: Using Markdown to PDF Online Tools

### Recommended Tools

**1. Dillinger (https://dillinger.io/)**
- Paste Markdown text
- Preview in real-time
- Export to PDF
- **Limitation:** Screenshot insertion is manual

**2. MarkdownToPDF (https://www.markdowntopdf.com/)**
- Upload Markdown file
- Converts automatically
- Download PDF
- **Limitation:** May not preserve all formatting

**3. CloudConvert (https://cloudconvert.com/md-to-pdf)**
- Upload Markdown file
- Convert to PDF
- Download result
- **Limitation:** Limited free conversions

**Pros:**
- ✅ No installation needed
- ✅ Quick for simple documents

**Cons:**
- ❌ Limited customization
- ❌ Privacy concerns (uploading to third-party)
- ❌ May not handle images well

---

## Method 6: Using VSCode + Extension

### What You Need
- Visual Studio Code (free)
- Extension: "Markdown PDF" by yzane

### Steps

1. **Install VS Code:**
   Download from: https://code.visualstudio.com/

2. **Install Extension:**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search: "Markdown PDF"
   - Install "Markdown PDF" by yzane

3. **Open File:**
   - File → Open File
   - Select `USER_MANUAL.md`

4. **Insert Screenshots:**
   - Replace `[SCREENSHOT X: ...]` with:
   ```markdown
   ![Screenshot description](screenshots/01-downloaded-zip.png)
   ```

5. **Convert to PDF:**
   - Right-click in editor
   - Select "Markdown PDF: Export (pdf)"
   - PDF saved in same folder

6. **Configure (optional):**
   - Create `.vscode/settings.json`:
   ```json
   {
     "markdown-pdf.displayHeaderFooter": true,
     "markdown-pdf.headerTemplate": "<div style='font-size:9px;width:100%;text-align:center;'>AI Fraud Detection - User Manual</div>",
     "markdown-pdf.footerTemplate": "<div style='font-size:9px;width:100%;text-align:center;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
     "markdown-pdf.format": "Letter",
     "markdown-pdf.margin.top": "1cm",
     "markdown-pdf.margin.bottom": "1cm",
     "markdown-pdf.margin.left": "1cm",
     "markdown-pdf.margin.right": "1cm"
   }
   ```

**Pros:**
- ✅ Free and open source
- ✅ Developer-friendly
- ✅ Customizable

**Cons:**
- ❌ Requires VS Code
- ❌ May need CSS customization

---

## Recommended Workflow

### For Best Results:

1. **Insert Screenshots into Markdown:**
   - Replace all `[SCREENSHOT X: ...]` with:
   ```markdown
   ![Description](screenshots/installation/01-downloaded-zip.png)
   ```

2. **Choose Method Based on Your Needs:**

   **Quick & Simple:**
   → Use **Typora** or **Google Docs**

   **Professional & Customizable:**
   → Use **Pandoc with LaTeX**

   **Developer-Friendly:**
   → Use **VSCode + Markdown PDF**

   **Maximum Control:**
   → Convert to **Word**, format manually, export PDF

3. **Quality Check:**
   - ✅ All screenshots visible
   - ✅ Proper page breaks
   - ✅ Table of contents links work
   - ✅ Headers/footers consistent
   - ✅ No formatting errors
   - ✅ File size reasonable (<10MB)

---

## Pandoc Command Reference

### Basic PDF:
```bash
pandoc USER_MANUAL.md -o USER_MANUAL.pdf
```

### With Table of Contents:
```bash
pandoc USER_MANUAL.md -o USER_MANUAL.pdf --toc --toc-depth=2
```

### With Custom Margins:
```bash
pandoc USER_MANUAL.md -o USER_MANUAL.pdf -V geometry:margin=1in
```

### With Syntax Highlighting:
```bash
pandoc USER_MANUAL.md -o USER_MANUAL.pdf --highlight-style=tango
```

### Full Professional Version:
```bash
pandoc USER_MANUAL.md -o USER_MANUAL.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --highlight-style=tango \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V linkcolor:blue \
  -V urlcolor:blue \
  --metadata title="AI Fraud Detection for WooCommerce" \
  --metadata subtitle="User Manual v2.2.1" \
  --metadata author="Tanveer Ahmed" \
  --metadata date="March 2025"
```

---

## Troubleshooting

### Problem: Images Not Showing in PDF

**Solution:**
- Use relative paths: `![Alt](./screenshots/01-image.png)`
- Or absolute paths: `![Alt](D:/path/to/screenshots/01-image.png)`
- Ensure images exist at specified paths

---

### Problem: Table of Contents Not Working

**Solution:**
- Add `--toc` flag to Pandoc command
- In Word: Use "Heading" styles consistently
- In Google Docs: Insert → Table of Contents

---

### Problem: PDF Too Large

**Solution:**
- Compress images before inserting:
  ```bash
  # Using ImageMagick
  convert input.png -quality 85 output.png
  ```
- Reduce screenshot resolution
- Use JPG instead of PNG for photos

---

### Problem: Pandoc Not Found

**Solution:**
- Verify installation: `pandoc --version`
- Add Pandoc to PATH
- Reinstall Pandoc

---

### Problem: LaTeX Errors with Pandoc

**Solution:**
- Install full TeX distribution (TeX Live or MiKTeX)
- Or use HTML intermediate:
  ```bash
  pandoc USER_MANUAL.md -o temp.html --standalone
  wkhtmltopdf temp.html USER_MANUAL.pdf
  ```

---

## Final Checklist

Before distributing the PDF:

- ✅ All 24 screenshots inserted and visible
- ✅ Table of contents has page numbers
- ✅ Headers are properly formatted
- ✅ Code blocks are readable
- ✅ Tables fit on pages (not cut off)
- ✅ Links are clickable (if interactive PDF)
- ✅ No "TODO" or placeholder text remaining
- ✅ Cover page has correct version number
- ✅ File size is reasonable (<10MB ideal)
- ✅ Test on different devices (Windows, Mac, mobile)
- ✅ Proofread for typos/errors

---

## Distribution

### File Naming:
```
AI_Fraud_Detection_WooCommerce_User_Manual_v2.2.1.pdf
```

### Where to Share:
- WordPress.org plugin documentation
- GitHub repository (releases section)
- Plugin website/support page
- Email to customers
- Knowledge base/help center

### Create Multiple Versions:
- **Full manual:** All screenshots, all sections
- **Quick start:** Just installation + basic usage (10 pages)
- **Video companion:** PDF with QR codes to video tutorials

---

## Next Steps

1. ✅ Capture all screenshots (use SCREENSHOT_GUIDE.md)
2. ✅ Insert images into USER_MANUAL.md
3. ✅ Choose conversion method from this guide
4. ✅ Convert to PDF
5. ✅ Review and quality check
6. ✅ Distribute to merchants

---

**Need Help?**

If you encounter issues with PDF conversion:
- Check Pandoc documentation: https://pandoc.org/MANUAL.html
- Stack Overflow: Tag `pandoc` or `markdown`
- GitHub issues for this project

---

**Good luck creating your PDF user manual!**
