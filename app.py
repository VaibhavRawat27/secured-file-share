import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
import qrcode
from io import BytesIO
import time
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="SecureShare | Safe File Hosting", layout="centered")
st.title("🔐 SecureShare")
st.caption("Upload any file securely with password and expiry control.")
st.markdown("📁 Files auto-delete after the selected time. Each file has a secure access link & QR code.")

# --- INIT CONFIG ---
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

UPLOAD_FOLDER = st.secrets["cloudinary"]["UPLOAD_FOLDER"]

# --- FILE ACCESS FROM QUERY PARAMS ---
query_params = st.query_params
file_id = query_params.get("file")

if file_id:
    st.markdown("### 🔗 File Access")
    st.info(f"Accessing file ID: `{file_id}`")

    password_input = st.text_input("Enter password to access file", type="password")

    try:
        file_details = cloudinary.api.resource(file_id, resource_type="raw")
        metadata = file_details.get("context", {}).get("custom", {})

        if not metadata:
            st.error("❌ No metadata found. File may be expired or not uploaded via SecureShare.")
            st.stop()

        original_password = metadata.get("password")
        expires_raw = metadata.get("expires_at")

        try:
            expires_at = int(float(expires_raw)) if expires_raw else 0
        except ValueError:
            expires_at = 0

        current_time = int(time.time())

        if expires_at and current_time > expires_at:
            st.error("⏰ This file has expired and is no longer accessible.")
            st.stop()

        if str(password_input).strip() == str(original_password).strip():
            time_left = expires_at - current_time
            mins_left = max(1, int(time_left / 60))
            st.success(f"✅ Access granted! Time remaining: {mins_left} minutes")

            file_url = file_details["secure_url"]
            file_name = file_details.get("original_filename", "download")

            st.markdown("🔗 **Secure Download Link:**")
            st.code(file_url)

            # ✅ Download link as button
            st.markdown(f"[⬇️ Click to Download File]({file_url})", unsafe_allow_html=True)

            # QR Code
            qr = qrcode.make(file_url)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, caption="📱 Scan to download", width=180)

            st.markdown(f"**🆔 File ID:** `{file_id}`")

        elif password_input:
            st.error("❌ Incorrect password.")
        st.stop()

    except cloudinary.exceptions.NotFound:
        st.error("⚠️ File not found. It might have been deleted or the ID is invalid.")
        st.stop()

# --- UPLOADER SECTION ---
st.markdown("### 📤 Upload New Files")

file_password = st.text_input("🔑 Set a password to access the file(s)", type="password")

if file_password.strip():
    expiry_hours = st.slider("⏰ Set expiry time (hours)", 1, 48, 6)
    uploaded_files = st.file_uploader("📂 Select file(s) to upload", type=None, accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown("---")
            st.info(f"Uploading `{uploaded_file.name}`...")

            expires_at = int(time.time() + expiry_hours * 3600)

            try:
                context_str = f"password={file_password}|expires_at={str(expires_at)}"

                result = cloudinary.uploader.upload(
                    uploaded_file,
                    folder=UPLOAD_FOLDER,
                    resource_type="raw",
                    use_filename=True,
                    unique_filename=True,
                    context=context_str
                )

                file_url = result.get("secure_url")
                public_id = result.get("public_id")

                base_url = "https://secured-file-share.streamlit.app/"
                access_url = f"{base_url}?file={urllib.parse.quote(public_id)}"

                st.success("✅ Upload successful!")

                st.markdown("🔗 **Secure Access Link (share this):**")
                st.code(access_url)

                qr = qrcode.make(access_url)
                buf = BytesIO()
                qr.save(buf, format="PNG")
                buf.seek(0)
                st.image(buf, caption="📱 Scan to access file", width=180)

                time_left_min = int((expires_at - time.time()) / 60)
                st.markdown(f"""
**🆔 Public ID:** `{public_id}`  
**⏱️ Time left:** {time_left_min} minutes  
**📂 Folder:** `{UPLOAD_FOLDER}`
                """)

            except Exception as e:
                st.error(f"❌ Upload failed: {str(e)}")
    else:
        st.info("📂 Please select at least one file to upload.")
else:
    st.warning("🔐 Please set a password to enable file upload.")

# --- FOOTER ---
st.markdown("---")
st.markdown("### ℹ️ About SecureShare")
st.write("""
**SecureShare** is a privacy-first file sharing tool built with **Streamlit** and **Cloudinary**.

Features include:

✅ Upload any file format (PDF, EXE, ZIP, DOCX, etc.)  
✅ Set custom expiry time  
✅ Password-protect every upload  
✅ QR code & shareable secure link  
✅ Files auto-delete after expiry  
✅ No login required
""")

st.markdown("""
---
🛠️ **Open Source:**  
View or contribute on GitHub 👉 [github.com/vaibhavrawat27/SecureShare](https://github.com/vaibhavrawat27/SecureShare)
""")

st.markdown("📧 Built by Vaibhav Rawat • ☁️ Powered by Cloudinary • 🐍 Made with Python & Streamlit")
