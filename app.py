import streamlit as st
import cloudinary
import cloudinary.uploader
import qrcode
from io import BytesIO
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="SecureShare | All Format Uploader", layout="centered")
st.title("🔐 SecureShare")
st.subheader("Upload any file securely. Auto-deletes after 6 hours.")
st.caption("All formats supported: PDF, ZIP, DOCX, MP4, EXE, RAW, CSV, etc.")
st.markdown("📁 You can upload multiple files. Each will have a secure link & QR code.")

# --- PASSWORD PROTECTION ---
CORRECT_PASSWORD = st.secrets["CORRECT_PASSWORD"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.warning("🔒 This site is password protected. To request access, email: **rawatvaibhav27@gmail.com**")
    password = st.text_input("Enter password to continue", type="password")
    if password == CORRECT_PASSWORD:
        st.session_state.authenticated = True
        st.success("✅ Access granted!")
        st.rerun()
    elif password:
        st.error("❌ Incorrect password.")
    st.stop()

# --- CLOUDINARY CONFIG ---
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

UPLOAD_FOLDER = st.secrets["cloudinary"]["UPLOAD_FOLDER"]

# --- FILE UPLOADER ---
uploaded_files = st.file_uploader("📂 Upload files", type=None, accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown("---")
        st.info(f"📄 Uploading: `{uploaded_file.name}` ({uploaded_file.size / 1024:.2f} KB)")

        expires_at = int(time.time() + 6 * 60 * 60)  # 6 hours from now

        try:
            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                folder=UPLOAD_FOLDER,
                resource_type="raw",
                use_filename=True,
                unique_filename=True,
                expires_at=expires_at
            )

            file_url = upload_result.get("secure_url")
            public_id = upload_result.get("public_id")

            st.success(f"✅ Uploaded `{uploaded_file.name}` successfully!")

            st.markdown("🔗 **Secure Download Link:**")
            st.code(file_url)

            qr = qrcode.make(file_url)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            buf.seek(0)
            st.image(buf, caption="📱 Scan to download", width=180)

            st.markdown(f"""
            **🗂️ Folder:** `{UPLOAD_FOLDER}`  
            **🕒 Auto-deletes after:** 6 hours  
            **🆔 Public ID:** `{public_id}`
            """)

        except Exception as e:
            st.error(f"❌ Failed to upload `{uploaded_file.name}`")
            st.error(str(e))

# --- FOOTER ---
st.markdown("---")
st.markdown("### ℹ️ About SecureShare")
st.write("""
SecureShare is a file sharing app built with **Streamlit** and **Cloudinary**, supporting **any file format**.
It creates secure download links and QR codes. Files auto-delete after 6 hours.

✅ **Supports All File Types**  
✅ **QR Code Sharing**  
✅ **No Login Required**
""")

st.markdown("""
---
🔧 **Note:**  
This is an under-development project in test mode.  
Please do not misuse this service. Abuse is monitored.
""")

st.markdown("📧 Built by Vaibhav Rawat • ☁️ Powered by Cloudinary • 🐍 Made with Python")
