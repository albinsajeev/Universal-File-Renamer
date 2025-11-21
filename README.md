# 🔢 Universal File Renamer

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows)
![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Created by [Albin Sajeev](https://github.com/albinsajeev)**

> **The "Nuclear Option" for file organization. Instantly batch rename ALL files in a folder to a clean numerical sequence (1.jpg, 2.png, 3.pdf...).**

[⬇️ **Download Latest App (v1.0)**](https://github.com/albinsajeev/Universal-File-Renamer/releases)

</div>

---

## 🧐 The Problem
Sometimes you don't care about preserving original filenames—you just want order. You might have a folder full of chaotic camera photos (`IMG_2024_Camera_X99.jpg`), mixed download files, or random documents.

Windows sorting is often confusing, and having long, messy filenames makes browsing difficult.

## 💡 The Solution
**Universal File Renamer** takes every single file in a folder (regardless of type), detects the original order, and renames them to a simple sequential number (`1`, `2`, `3`...) while **perfectly preserving the file extension**.

### **See the Difference**

| ❌ Messy (Before) | ✅ Universal (After) |
| :--- | :--- |
| `DCIM_0091.jpg` | `1.jpg` |
| `Screenshot 2025-01.png` | `2.png` |
| `Final_Report_v2.pdf` | `3.pdf` |
| `Movie_Clip.mp4` | `4.mp4` |

---

## 🚀 Key Features

### 🔄 Universal Format Support
Works on **ANY** file type simultaneously. You can have a folder mixed with images, PDFs, scripts, and videos—the tool will rename them all in order while keeping their specific extensions (`.pdf`, `.docx`, `.mkv`) intact.

### 🛡️ Safe 2-Phase Process
To prevent data loss or "File Already Exists" errors, the tool uses a smart renaming engine:
1.  **Phase 1:** Renames all files to a unique temporary ID (`__temp_uuid...`).
2.  **Phase 2:** Renames the temporary files to the final numbers (`1`, `2`, `3`...).

### 🧮 Smart Natural Sorting
The tool respects the original human-readable order. If your files are named `Image 1` and `Image 10`, it sorts them correctly (1 then 10) before renaming, ensuring your files stay in the correct sequence.

---

## 📥 Download & Run
You do not need to install Python to use this tool.

1.  **[Download the .exe file](https://github.com/albinsajeev/Universal-File-Renamer/releases)** from the Releases page.
2.  Double-click to run.
    * *Note: If you see a "Windows protected your PC" warning, click **"More Info"** -> **"Run Anyway"**.*
3.  Select the folder you want to clean.

> [!WARNING]
> **This process is permanent.** Original filenames will be erased and replaced with numbers. Please ensure you select the correct folder before running!

---

## 👨‍💻 Build from Source
If you are a developer and want to modify the code or build it yourself:

```bash
# 1. Clone the repository
git clone [https://github.com/albinsajeev/Universal-File-Renamer.git](https://github.com/albinsajeev/Universal-File-Renamer.git)

# 2. Install PyInstaller
pip install pyinstaller

# 3. Build the executable
python -m PyInstaller --onefile --noconsole --name "Universal Renamer" universal_renamer.py
