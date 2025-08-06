# 🔒 AVISO DE SEGURIDAD

## ⚠️ **CREDENCIALES NO INCLUIDAS**

**Este repositorio NO contiene credenciales sensibles por razones de seguridad.**

### 📋 **Archivos Requeridos Localmente:**

1. **`.streamlit/secrets.toml`** - Configuración completa de la aplicación
2. **`google_credentials_coti.json`** - Service Account de Google Cloud

### 🛡️ **Archivos Protegidos en .gitignore:**
- `.streamlit/secrets.toml`
- `google_credentials_coti.json`
- `google_credentials.json`
- `.env`
- `DEPLOYMENT_GUIDE.md`

### 🚀 **Para Configurar la Aplicación:**

1. **Copia el archivo de ejemplo:**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Edita `.streamlit/secrets.toml` con tus credenciales reales**

3. **Agrega tu archivo de Service Account como `google_credentials_coti.json`**

### 📖 **Documentación Completa:**
Ver `FINAL_DEPLOYMENT_CHECKLIST.md` para instrucciones detalladas.

---

**🔐 La seguridad de las credenciales es nuestra prioridad.**