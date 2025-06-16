# 🔐 Secure File Share

**Secure File Share** is a lightweight, privacy-focused online file sharing platform built using **Streamlit** and **Cloudinary's API**. It allows users to securely upload files and instantly generate a private link (and QR code) for download. Files are automatically deleted after a defined time, ensuring safety and minimal server load.

---

## 🚀 Features

- 📁 Upload and share files instantly
- 🔒 No login required for sharing
- ⏱️ Files auto-delete after 6 hours
- 🔗 Unique secure download link generated
- 📱 QR Code for instant access on mobile
- 🌐 Hosted entirely on Streamlit with Cloudinary backend
- 💡 Clean and simple UI with Tailwind-inspired design

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **Backend Storage:** Cloudinary (API)
- **QR Code Generation:** `qrcode` Python library
- **File Security & Deletion:** Auto-expiry via timestamp + Cloudinary
- **Others:** Python, UUID, base64, datetime

---

## 📦 How It Works

1. Upload a file through the interface.
2. File is sent to Cloudinary with a unique public ID.
3. A secure download link and QR code are generated.
4. After 6 hours, the file is automatically removed from Cloudinary.
5. You can download the file using the provided link/QR within the valid time.

---
