# Plugin Assets

These are the official WordPress.org plugin assets for AI Fraud Detection.

## 📁 Current Files

### Icons
- **icon-256x256.png** (1.1 MB) - Plugin icon (high-res)
  - Source: `Gemini_Generated_Image_m6hxgjm6hxgjm6hx.png`
  - Design: Shield with circuit board patterns
  - Status: ✅ Ready (needs optimization)

- **icon-128x128.png** - Plugin icon (standard-res)
  - Status: ⚠️ **NEEDS TO BE CREATED** (resize from 256x256)

### Banners
- **banner-1544x500.png** (1.6 MB) - Plugin banner (retina)
  - Source: `Gemini_Generated_Image_mpzvaampzvaampzv.png`
  - Design: Dashboard with shield and checkmark
  - Status: ✅ Ready (needs optimization)

- **banner-772x250.png** - Plugin banner (standard)
  - Status: ⚠️ **NEEDS TO BE CREATED** (resize from 1544x500)

### Screenshots
- **screenshot-1.png** (893 KB) - WordPress admin dashboard
- **screenshot-2.png** (1.4 MB) - E-commerce store protection
- **screenshot-3.png** (1.6 MB) - Dashboard theme
- **screenshot-4.png** (1.7 MB) - Shield with gradient
- **screenshot-5.png** (1.4 MB) - Shopping cart protection

## ⚠️ Required Actions

### 1. Create Resized Versions

**Option A: Use Online Tool (Easiest)**
1. Go to https://www.iloveimg.com/resize-image
2. Upload `icon-256x256.png`
3. Resize to 128x128 pixels
4. Save as `icon-128x128.png`
5. Upload `banner-1544x500.png`
6. Resize to 772x250 pixels
7. Save as `banner-772x250.png`

**Option B: Use PowerShell (Windows)**
```powershell
# Install ImageMagick first
winget install ImageMagick.ImageMagick

# Then resize
magick icon-256x256.png -resize 128x128 icon-128x128.png
magick banner-1544x500.png -resize 772x250 banner-772x250.png
```

**Option C: Use Photoshop/GIMP**
- Open each file
- Image → Image Size
- Resize to target dimensions
- Save as PNG

### 2. Optimize File Sizes

**Current sizes are TOO LARGE for web:**
- Icons: Target <50 KB each
- Banner: Target <200 KB each
- Screenshots: Target <300 KB each

**Optimization Tools:**

**Online (Free & Easy):**
1. Go to https://tinypng.com
2. Upload all PNG files
3. Download optimized versions
4. Replace original files

**Desktop:**
```powershell
# Install PNGQuant
winget install pngquant

# Optimize all PNGs
pngquant --quality=65-80 *.png --ext .png --force
```

### 3. Final Checklist

Before WordPress.org submission:
- [ ] icon-128x128.png created
- [ ] icon-256x256.png created ✅
- [ ] banner-772x250.png created
- [ ] banner-1544x500.png created ✅
- [ ] All files optimized (<50 KB icons, <200 KB banners)
- [ ] Screenshots optimized (<300 KB each)
- [ ] All files tested in WordPress locally

## 📊 File Size Targets

| File | Current | Target | Status |
|------|---------|--------|--------|
| icon-128x128.png | - | <30 KB | ⚠️ Not created |
| icon-256x256.png | 1.1 MB | <50 KB | ❌ Too large |
| banner-772x250.png | - | <150 KB | ⚠️ Not created |
| banner-1544x500.png | 1.6 MB | <200 KB | ❌ Too large |
| screenshot-1.png | 893 KB | <300 KB | ❌ Too large |
| screenshot-2.png | 1.4 MB | <300 KB | ❌ Too large |
| screenshot-3.png | 1.6 MB | <300 KB | ❌ Too large |
| screenshot-4.png | 1.7 MB | <300 KB | ❌ Too large |
| screenshot-5.png | 1.4 MB | <300 KB | ❌ Too large |

## 🎨 Design Details

### Icon Design
- **Shield with circuit board** represents AI-powered security
- **Purple to blue gradient** (#764ba2 to #667eea)
- **White outline and patterns** for contrast
- **Minimal, clean design** works at small sizes

### Banner Design
- **Dashboard theme with security elements**
- **Shield icon on left** with checkmark
- **Tech patterns in background** (graphs, charts, HUD elements)
- **Space on right** for text overlay (WordPress.org adds plugin name automatically)

### Screenshot Content
1. WordPress admin dashboard (settings page mockup)
2. E-commerce store protection visualization
3. Dashboard theme with shield
4. Clean shield gradient banner
5. Shopping cart with shield protection

## 📝 WordPress.org Upload

Once optimized, these files go to your SVN repository:

```
/assets/
  ├── icon-128x128.png
  ├── icon-256x256.png
  ├── banner-772x250.png
  ├── banner-1544x500.png
  ├── screenshot-1.png
  ├── screenshot-2.png
  ├── screenshot-3.png
  ├── screenshot-4.png
  └── screenshot-5.png
```

**SVN commands:**
```bash
svn add assets/*
svn ci -m "Add plugin assets (icons, banners, screenshots)"
```

## 🔧 Quick Optimization Script

Save as `optimize.ps1` and run in this directory:

```powershell
# Download TinyPNG CLI (requires API key - free tier available)
# Or use online: https://tinypng.com

# Alternative: Use ImageMagick
foreach ($file in Get-ChildItem *.png) {
    magick $file.FullName -strip -quality 85 -define png:compression-level=9 "optimized_$($file.Name)"
}
```

## ✅ Next Steps

1. **Resize images** (create 128x128 icon and 772x250 banner)
2. **Optimize all files** using TinyPNG or similar
3. **Test locally** by uploading to test WordPress site
4. **Verify sizes** (check file sizes meet targets)
5. **Ready for WordPress.org submission!**

---

**Original Gemini files are kept in this folder for backup.**
**Do NOT upload the `Gemini_Generated_Image_*` files to WordPress.org - only use the renamed files.**
