# 🚀 Guía de Deployment - Lead Generator Pro

## ⚡ Deploy Rápido en Streamlit Cloud

### 1. Crear Repositorio en GitHub
```bash
# El código ya está listo localmente
# Crear repositorio en GitHub: https://github.com/new
# Nombre sugerido: lead-generator-pro
```

### 2. Subir Código a GitHub
```bash
# Ejecutar desde la terminal:
git remote add origin https://github.com/TU_USUARIO/lead-generator-pro.git
git branch -M main
git push -u origin main
```

### 3. Crear App en Streamlit Cloud
1. Ve a: https://share.streamlit.io
2. Clic en "New app"
3. Conecta con GitHub
4. Selecciona el repositorio: `lead-generator-pro`
5. Configurar:
   - **Branch**: main
   - **Main file**: streamlit_app.py
   - **App URL**: lead-generator-pro (o el que prefieras)

### 4. Configurar Secrets en Streamlit Cloud

**⚠️ IMPORTANTE: Copia exactamente este contenido en la sección "Secrets" de Streamlit Cloud:**

```toml
[google]
places_api_key = "AIzaSyDsovxSO5Qk65EwsRwzjrSIdaPjmQuumek"

[google_sheets]
spreadsheet_id = "1KjQMeQQ_3EO0MtfrSO7waTHtiZdTb7futHIA4yk6Xf8"
credentials_file = "google_credentials.json"

[google_service_account]
type = "service_account"
project_id = "n8n-testing-459319"
private_key_id = "b9d4f8d1301a8fdcb237cd4ef28accdd098032d0"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDjK06lDNZypWqD
mfz1KbhrmE1dQl6bGEeYd0ghQu/rsaejXEueJTacnoPeeEJJYBoE8BBiFp93WgfP
0wS9tLrGEbfIK2y0Vk3DoHBwI9v5B1TW3nomtaSwsor87qHVAGgtMBR8mpTRQo3s
TtTMZ84Pk/mDwvgwifzt8Sxob5QNFOHIoGqTiUh/UJlSxbSVqNKtbLGDaOuKw6F2
F4HMGJcwQIMBqaqyHYZBHP/SsVxPVmoHd8E/6ww3P2+geX/AEEbIxEaeaA10Irvn
miMYe40cbIbRex+ufKucOfKqfJStW9bW4EPgBGw84J2O1R/FUyzJ/KasVobY4HAg
F/ti5B7PAgMBAAECggEAANBowq7lrskQ5O2RFz/8jhvNlEWCYf210DWN2eoTYNvf
5GSHdWTiULVzYoK3WSf3/bTGOQBQ2g/mdNXQ9MTFyJ5w+CqOGrQMeX2gkG3YoFEi
hts6gZ8L2Qa7FqnmnkFieIsQeAtqUobB8czaIUczwoLslCVIuckjjdkYPGRIZ714
yOLl/2N8ejmn80M3gcgXnfu6xfk8MWI8/kSiDLfz1zi+TXCefnZtfITiJ5Mnv5Jf
W96FMwIPnNjVcNCxJmBokdpa7X0Xq/iE0oT16PSSemkmIFs651QydA/BjsXtJE7Z
3kIk+JUKYC5pi68ellcCdXTulK7xt/5dIIkMnZTAIQKBgQD+l+DGokNqlHZsvt0h
np6FoHBPpMBmrar/tKivsQGgbvwxnjx5rTOXgRXcxwycZsbWjK+PwB5T1520OlLD
d0P8459xMuuZKsjEpeE8VbP11duH0iMXAqTlUFEmpsnXdS2CsbZmPINdatnpUIAl
gR8nkxA16bXzUQ6zShOGVR4mqQKBgQDkbKNHAEiI6a5MJe+OwZ5MaaR8ZWGjIvEb
96gCWFdIsx9vR/Z5njf/dRPTFT54zOa+pSVTAzEtqMt6xDd8oFnaxbOFRa11Ivjs
zoEqAUKhUWcTf6Ok760jf3zwU5hqVn62BNWkoxBoELqoub0QssvrqFlbS0m1Ib1d
xi40SrwctwKBgQDT8l53HpifPs9EArUXCvUPa5x0QUTHdibYT27rLKGdDSg4qnHQ
HgfIRfeMX8042zsHXAG/24Gj7OlmI/PItB5OhrSyyWBnl72iMDJNR0/VBd+Ht8Hs
ow/hs7aLRejczLlBh27At/noqE6XNKQqFM95461oJJOL51wkmDOe7nd2WQKBgQCz
udq6abmoqByw44RakXMo8lIuYmJxRnPpKnIx7io3FGDeYQPIaznqMMc5ZVSzHZ1M
UYpNh4xxPYdkf/CciVpJrRZz/P/e03aCdHTihP1VCkSM7ffnNYHIFW5LdarNuGKY
erNSh87H4qnLSeE9u0CBmgM8tr822mYx21XNZSQffwKBgApfOfQfrMqt5dihm3O/
ZceaepRE+pc8uFUU2zTVOck7KDLvcriA+91awCiIdEtTwpr4Wqwm4O7kFxC7GJKa
yOgkXSQqjBz8C4xiq62REoXZ3dqygertdnU+qr0bnO44B5qxgxDQ0TkIhSwnCVJf
ep/b8fixZqnWq/n8AgJaDNDd
-----END PRIVATE KEY-----"""
client_email = "google-leads-b2b@n8n-testing-459319.iam.gserviceaccount.com"
client_id = "116294668329830644224"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/google-leads-b2b%40n8n-testing-459319.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

### 5. Deploy Final
1. Clic en "Deploy!"
2. Espera 2-3 minutos
3. ¡Tu app estará lista!

## 🎯 URL Final
Tu aplicación estará disponible en:
**`https://lead-generator-pro.streamlit.app`**

## 🔧 Verificación Post-Deploy
1. Prueba hacer una búsqueda pequeña
2. Verifica que se guarde en Google Sheets
3. Revisa los logs si hay errores

## 📞 Soporte
Si hay problemas, revisa:
- Logs en Streamlit Cloud
- Configuración de secrets (copia exacta)
- Permisos de Google Sheets

---
**¡Listo para producción! 🚀** 