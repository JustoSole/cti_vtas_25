# 🎯 Lead Generator Pro - Aplicación de Generación de Leads

## 📋 Descripción

**Lead Generator Pro** es una aplicación web moderna desarrollada en **Streamlit** que permite generar leads de negocios argentinos de manera inteligente y automatizada. La aplicación utiliza Google Places API + Web Scraping para obtener información completa de contacto.

## ✨ Características Principales

### 🔍 Búsqueda Exhaustiva
- **Algoritmo mejorado** que supera las limitaciones de la API de Google Places
- **División geográfica** en sub-áreas para obtener hasta 500% más resultados
- **Búsqueda sin límites** - encuentra TODOS los lugares disponibles automáticamente
- **Deduplicación inteligente** para evitar resultados repetidos

### 🌐 Enriquecimiento de Datos
- **Web scraping inteligente** que extrae emails y redes sociales
- **Procesamiento paralelo** para máxima eficiencia
- **Formateo automático** de números argentinos

### ☁️ Integración con la Nube
- **Google Sheets** - Guardado automático con detección de duplicados
- **Múltiples formatos** de exportación (CSV, Google Sheets)
- **Configuración segura** usando Streamlit secrets

### 🎨 Interfaz Profesional
- **Diseño moderno** con CSS personalizado y gradientes
- **Progreso en tiempo real** con métricas actualizadas
- **Filtros interactivos** para refinar resultados
- **Centro de ayuda** integrado

## 🚀 Guía de Instalación y Uso

### 1. Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd Lead_google_places_app

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración de APIs

#### Google Places API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo o selecciona uno existente
3. Habilita la **Places API**
4. Crea una API Key y agrégala a `.streamlit/secrets.toml`

#### Configuración de Streamlit Secrets
Crea el archivo `.streamlit/secrets.toml`:
```toml
[google]
places_api_key = "tu_google_places_api_key_aqui"

[google_sheets]
spreadsheet_id = "tu_spreadsheet_id_aqui"
credentials_file = "google_credentials.json"

[google_service_account]
type = "service_account"
project_id = "tu_project_id"
# ... resto de credenciales del service account
```

### 3. Configuración de Google Sheets
1. Crea un **Service Account** en Google Cloud Console
2. Descarga las credenciales JSON
3. Comparte tu hoja de Google Sheets con el email del service account
4. Copia el ID de la hoja desde la URL

### 4. Ejecutar la Aplicación
```bash
streamlit run streamlit_app.py
```

## 🔧 Cómo Funciona

### Búsqueda Inteligente
- **📍 Google Places**: Encuentra lugares usando división geográfica
- **🌐 Web Scraping**: Extrae emails y redes sociales de sitios web
- **☁️ Google Sheets**: Guarda automáticamente los resultados

### Proceso de Búsqueda
1. La aplicación busca **TODOS** los lugares disponibles (sin límite)
2. Muestra progreso en tiempo real con 3 métricas
3. Procesa sitios web en paralelo
4. Guarda automáticamente en Google Sheets

### Exportación de Datos
- **CSV Completo**: Todos los datos encontrados
- **CSV Filtrado**: Solo resultados que pasan filtros
- **Google Sheets**: Acceso directo a hoja de cálculo

## 📊 Estructura de Archivos

```
Lead_google_places_app/
├── streamlit_app.py              # 🎯 Aplicación principal
├── main_orchestrator.py          # 🔄 Orquestador del flujo
├── google_places_fetcher.py      # 📍 Google Places API
├── website_scraper.py            # 🌐 Web scraping
├── google_sheets_manager.py      # ☁️ Google Sheets
├── pages/
│   └── 2_❓_Ayuda.py             # ❓ Página de ayuda
├── .streamlit/
│   ├── config.toml               # ⚙️ Configuración UI
│   └── secrets.toml              # 🔐 Credenciales
├── google_credentials.json       # 🔑 Credenciales Google
├── requirements.txt              # 📦 Dependencias
└── README.md                     # 📖 Este archivo
```

## 🔧 Arquitectura Técnica

### Flujo de Trabajo
```
📍 Google Places API → 🌐 Web Scraping → ☁️ Google Sheets
```

### Componentes Principales

#### 1. **GooglePlacesFetcher**
- Búsqueda exhaustiva por grillas geográficas
- Manejo de paginación y límites de API
- Deduplicación por place_id

#### 2. **WebsiteScraper**
- Procesamiento paralelo de sitios web
- Extracción de emails con múltiples patrones
- Detección inteligente de páginas de contacto
- Filtrado de emails falsos/de prueba

#### 3. **GoogleSheetsManager**
- Conexión segura usando Service Account
- Deduplicación automática de registros
- Formateo y limpieza de datos
- Manejo robusto de errores

#### 4. **MainOrchestrator**
- Coordinación del flujo completo
- Manejo de progreso en tiempo real
- Recuperación ante errores
- Logging detallado

## 📈 Resultados Esperados

### Tipos de Datos Extraídos
- **Información básica**: Nombre, dirección, teléfono
- **Calificaciones**: Rating y número de reseñas
- **Contacto digital**: Emails, sitio web
- **Redes sociales**: Facebook, Instagram, etc.
- **Metadatos**: Fecha de extracción, query de búsqueda

### Métricas de Performance
- **50-200 lugares**: 5-10 minutos típicos
- **200+ lugares**: 10-20 minutos
- **Tasa de éxito**: 95%+ para Google Places
- **Emails encontrados**: 30-60% de sitios web

## 🛠️ Troubleshooting

### Problemas Comunes

**Error de API Key**
- Verificar que la API key esté en `secrets.toml`
- Confirmar que Places API esté habilitada
- Revisar límites de cuota

**Error de Google Sheets**
- Verificar credenciales del service account
- Confirmar permisos de escritura en la hoja
- Revisar formato del spreadsheet_id

**Sitios web no cargan**
- Algunos sitios bloquean scraping
- Esto es normal, el proceso continúa automáticamente

## 🔐 Seguridad

- **API Keys**: Nunca hardcodear en el código
- **Credenciales**: Usar siempre Streamlit secrets
- **Service Account**: Principio de menor privilegio
- **Rate Limiting**: Respeto a límites de APIs

## 📞 Soporte

Para reportar issues o solicitar features:
1. Revisar la documentación
2. Verificar logs de la aplicación
3. Consultar el centro de ayuda integrado

---

**¡Genera leads de manera inteligente y automatizada! 🚀** 