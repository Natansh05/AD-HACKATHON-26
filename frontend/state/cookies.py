from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="audio_app_",
    password="change-this-secret"
)
