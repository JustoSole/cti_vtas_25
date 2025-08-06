#!/usr/bin/env python3
"""
🎯 Lead Generator App - Aplicación de Streamlit
Generador inteligente de leads usando Google Places API
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import io

# Importar nuestros módulos
from main_orchestrator import main
from google_sheets_manager import GoogleSheetsManager

# Configuración de la página
st.set_page_config(
    page_title="Lead Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .config-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    
    .instructivo-box {
        background: linear-gradient(45deg, #e3f2fd, #f3e5f5);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .success-banner {
        background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .progress-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .help-tab {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
    

    
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 5rem auto;
        max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .login-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .error-message {
        background: #ff4757;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .dashboard-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid #dee2e6;
    }
    
    .dashboard-header {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .recent-activity {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    if 'search_completed' not in st.session_state:
        st.session_state.search_completed = False
    if 'current_stats' not in st.session_state:
        st.session_state.current_stats = {
            'places_found': 0,
            'emails_found': 0,
            'sheets_uploaded': 0
        }
    # Estado de autenticación
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def create_header():
    """Crea el header principal de la aplicación"""
    st.markdown("""
    <div class="main-header">
        <h1>COTI LEAD GENERATOR</h1>
        <p>Encuentra y enriquece leads de negocios usando Google Maps y web scraping inteligente</p>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    """Muestra el dashboard con estadísticas históricas"""
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.markdown(f"""
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h3>📊 Dashboard Histórico de Búsquedas</h3>
            <p>Resumen de todas las búsquedas realizadas y datos almacenados</p>
            <small style="opacity: 0.8;">Última actualización: {current_time}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Obtener estadísticas del Google Sheets
        with st.spinner("📊 Cargando estadísticas históricas..."):
            sheets_manager = GoogleSheetsManager()
            stats = sheets_manager.get_stats()
            
            # Indicador de estado del sistema
            if stats['total_records'] >= 0:  # Si obtuvimos estadísticas, está funcionando
                st.success("🟢 **Sistema Conectado** - Google Sheets respondiendo correctamente")
            else:
                st.warning("🟡 **Conexión Limitada** - Puede haber problemas de conectividad")
        
        # Métricas principales en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <h2 style="color: #28a745; margin: 0;">📋</h2>
                <h3 style="margin: 0.5rem 0;">{}</h3>
                <p style="margin: 0; color: #6c757d;">Total Registros</p>
            </div>
            """.format(stats['total_records']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <h2 style="color: #007bff; margin: 0;">📧</h2>
                <h3 style="margin: 0.5rem 0;">{}</h3>
                <p style="margin: 0; color: #6c757d;">Emails Extraídos</p>
            </div>
            """.format(stats['emails_found']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card">
                <h2 style="color: #ffc107; margin: 0;">🌐</h2>
                <h3 style="margin: 0.5rem 0;">{}</h3>
                <p style="margin: 0; color: #6c757d;">Sitios Web</p>
            </div>
            """.format(stats['websites_found']), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-card">
                <h2 style="color: #dc3545; margin: 0;">🔍</h2>
                <h3 style="margin: 0.5rem 0;">{}</h3>
                <p style="margin: 0; color: #6c757d;">Búsquedas Únicas</p>
            </div>
            """.format(stats['unique_searches']), unsafe_allow_html=True)
        
        # Métricas de eficiencia
        if stats['total_records'] > 0:
            st.markdown("### 📈 Eficiencia de Extracción")
            eff_col1, eff_col2, eff_col3 = st.columns(3)
            
            email_percentage = (stats['emails_found'] / stats['total_records']) * 100
            website_percentage = (stats['websites_found'] / stats['total_records']) * 100
            avg_per_search = stats['total_records'] / max(stats['unique_searches'], 1)
            
            with eff_col1:
                st.metric(
                    "📧 Tasa de Emails",
                    f"{email_percentage:.1f}%",
                    f"{stats['emails_found']} de {stats['total_records']}"
                )
            
            with eff_col2:
                st.metric(
                    "🌐 Tasa de Websites", 
                    f"{website_percentage:.1f}%",
                    f"{stats['websites_found']} de {stats['total_records']}"
                )
            
            with eff_col3:
                st.metric(
                    "🎯 Promedio por Búsqueda",
                    f"{avg_per_search:.0f}",
                    "registros encontrados"
                )
        
        # Sección de actividad reciente y búsquedas más realizadas
        if stats['recent_activity'] or stats['search_distribution']:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="recent-activity">
                    <h4>🕒 Actividad Reciente</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if stats['recent_activity']:
                    for activity in stats['recent_activity'][:5]:
                        fecha = activity['date'][:16] if len(activity['date']) > 16 else activity['date']
                        st.markdown(f"• **{activity['query']}** - {fecha}")
                else:
                    st.info("No hay actividad reciente registrada")
            
            with col2:
                st.markdown("""
                <div class="recent-activity">
                    <h4>🔥 Búsquedas Más Realizadas</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if stats['search_distribution']:
                    # Mostrar lista de búsquedas
                    for query, count in list(stats['search_distribution'].items())[:5]:
                        st.markdown(f"• **{query}** ({count} veces)")
                    
                    # Gráfico de barras simple si hay datos
                    if len(stats['search_distribution']) > 1:
                        st.markdown("---")
                        st.markdown("**📊 Distribución Visual:**")
                        chart_data = dict(list(stats['search_distribution'].items())[:5])
                        st.bar_chart(chart_data)
                else:
                    st.info("No hay búsquedas registradas aún")
        else:
            st.info("💡 Realiza tu primera búsqueda para ver estadísticas detalladas")
        
        # Botones de acción
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Actualizar Dashboard", use_container_width=True):
                st.rerun()
        
        with col2:
            try:
                sheets_url = sheets_manager.get_sheet_url()
                st.link_button(
                    "📊 Ver en Google Sheets",
                    sheets_url,
                    use_container_width=True,
                    type="secondary"
                )
            except:
                pass
        
        with col3:
            st.button("📈 Nuevo Análisis", use_container_width=True, disabled=True, help="Próximamente: análisis avanzado de datos")
        
    except Exception as e:
        st.error(f"❌ Error cargando el dashboard: {str(e)}")
        st.info("💡 El dashboard se mostrará cuando realices tu primera búsqueda")

def show_instructivo():
    """Muestra el mini instructivo en la parte superior"""
    st.markdown("""
    <div class="instructivo-box">
        <h4>📋 Mini Instructivo</h4>
        <p><strong>1.</strong> Especifica el <strong>tipo de negocio</strong> que buscas (ej: "restaurantes", "gimnasios", "dentistas")</p>
        <p><strong>2.</strong> Ingresa la <strong>ubicación</strong> específica (recomiendo por barrio o ciudad si no es tan grande)</p>
        <p><strong>3.</strong> Haz clic en <strong>"Iniciar Búsqueda"</strong> y observa el progreso en tiempo real</p>
        <p><strong>ℹ️</strong> La búsqueda incluye automáticamente <strong>web scraping</strong> para extraer emails y <strong>guardado en Google Sheets</strong></p>
    </div>
    """, unsafe_allow_html=True)

def show_progress_section():
    """Muestra la sección de progreso mejorada durante la ejecución"""
    st.markdown("""
    <div class="progress-section">
        <h3>🔄 Proceso en Ejecución</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de progreso principal
    main_progress = st.progress(0)
    status_text = st.empty()
    
    # Crear contenedor para estadísticas detalladas
    stats_container = st.container()
    
    with stats_container:
        st.markdown("#### 📊 Estadísticas en Tiempo Real")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            places_metric = st.empty()
        with col2:
            scraped_metric = st.empty()
        with col3:
            sheets_metric = st.empty()
    
    # Contenedor para información detallada
    details_container = st.container()
    
    with details_container:
        st.markdown("#### 📋 Detalles del Proceso")
        details_text = st.empty()
    
    return main_progress, status_text, places_metric, scraped_metric, sheets_metric, details_text

def execute_search(query, location, include_scraping, save_to_sheets):
    """Ejecuta la búsqueda con indicadores de progreso mejorados en tiempo real"""
    
    # Configurar progreso
    main_progress, status_text, places_metric, scraped_metric, sheets_metric, details_text = show_progress_section()
    
    try:
        # Inicializar estadísticas
        st.session_state.current_stats = {
            'places_found': 0,
            'emails_found': 0,
            'sheets_uploaded': 0
        }
        
        # Crear callback mejorado para actualizar progreso
        def update_progress_callback(step, message, count=None):
            if step == "places_searching":
                main_progress.progress(5)
                status_text.text(f"🔍 {message}")
                places_metric.metric("📍 Lugares Encontrados", "0", delta="Iniciando...")
                details_text.info(f"🔍 **Google Places**: {message}")
            
            elif step == "places_progress":
                current_point, total_points, found_count = count
                progress_percentage = 10 + int((current_point / total_points) * 40) # 10% a 50%
                main_progress.progress(progress_percentage)
                status_text.text(f"🔍 Buscando en grilla... ({current_point}/{total_points})")
                places_metric.metric("📍 Lugares Encontrados", str(found_count), delta="Buscando...")
                details_text.info(f"🔍 **Google Places**: {message}")

            elif step == "places_details_progress":
                current, total = count
                progress_percentage = 50 + int((current / total) * 10) # 50% a 60%
                main_progress.progress(progress_percentage)
                status_text.text(f"🛠️ Obteniendo detalles... ({current}/{total})")
                details_text.info(f"🛠️ **Google Places**: {message}")

            elif step == "places_found":
                main_progress.progress(60)
                status_text.text(f"✅ {message}")
                st.session_state.current_stats['places_found'] = count
                places_metric.metric("📍 Lugares Encontrados", count, delta=f"✅ Completado")
                details_text.success(f"✅ **Google Places**: {message} - Total: {count}")
                
            elif step == "scraping_start":
                main_progress.progress(65)
                status_text.text(f"🌐 {message}")
                scraped_metric.metric("🌐 Emails Extraídos", "0", delta="Iniciando...")
                details_text.info(f"🌐 **Web Scraping**: {message}")
                
            elif step == "scraping_progress":
                progress_value = 65 + (count or 0) * 0.25
                main_progress.progress(min(progress_value, 85))
                status_text.text(f"🌐 {message}")
                scraped_metric.metric("🌐 Emails Extraídos", f"~{count or 0}%", delta="Procesando...")
                details_text.info(f"🌐 **Web Scraping**: {message} - Progreso: {count or 0}%")
                
            elif step == "scraping_complete":
                main_progress.progress(85)
                status_text.text(f"✅ {message}")
                st.session_state.current_stats['emails_found'] = count
                scraped_metric.metric("🌐 Emails Extraídos", count, delta="✅ Completado")
                details_text.success(f"✅ **Web Scraping**: {message} - Emails obtenidos: {count}")
                
            elif step == "sheets_start":
                main_progress.progress(90)
                status_text.text(f"☁️ {message}")
                sheets_metric.metric("☁️ Google Sheets", "0", delta="Subiendo...")
                details_text.info(f"☁️ **Google Sheets**: {message}")
                
            elif step == "sheets_complete":
                main_progress.progress(100)
                status_text.text(f"✅ {message}")
                st.session_state.current_stats['sheets_uploaded'] = count
                sheets_metric.metric("☁️ Google Sheets", count, delta="✅ Completado")
                details_text.success(f"✅ **Google Sheets**: {message} - Registros subidos: {count}")
        
        # Ejecutar búsqueda principal con callback mejorado
        result_df, message = main(
            query=query,
            location=location,
            max_results=None,
            progress_callback=update_progress_callback
        )
        
        if result_df is None:
            st.error(f"❌ Error en la búsqueda: {message}")
            return None, message
        
        # Completado con resumen final
        main_progress.progress(100)
        status_text.text("🎉 ¡Proceso completado exitosamente!")
        
        # Mostrar resumen final
        final_stats = st.session_state.current_stats
        details_text.success(f"""
        🎉 **PROCESO COMPLETADO** - Resumen Final:
        - 📍 Lugares encontrados: {final_stats['places_found']}
        - 🌐 Emails extraídos: {final_stats['emails_found']}
        - ☁️ Registros en Sheets: {final_stats['sheets_uploaded']}
        """)
        
        return result_df, message
        
    except Exception as e:
        st.error(f"❌ Error durante la ejecución: {str(e)}")
        return None, str(e)

def show_results_section(df, message):
    """Muestra la sección de resultados mejorada"""
    st.markdown("### 📊 Resultados de la Búsqueda")
    
    if df is not None and not df.empty:
        # Banner de éxito
        st.markdown(f"""
        <div class="success-banner">
            <h3>✅ ¡Búsqueda Completada Exitosamente!</h3>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas resumen mejoradas
        st.markdown("#### 📈 Resumen de Resultados")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🏢 Total Lugares",
                len(df),
                delta="Encontrados"
            )
        
        with col2:
            emails_count = sum(1 for x in df['scraped_emails'] if x and str(x).strip() and str(x) != 'nan')
            st.metric(
                "📧 Con Emails",
                emails_count,
                delta=f"{emails_count/len(df)*100:.1f}%"
            )
        
        with col3:
            websites_count = sum(1 for x in df['websiteUri'] if x and str(x).strip() and str(x) != 'nan')
            st.metric(
                "🌐 Con Website",
                websites_count,
                delta=f"{websites_count/len(df)*100:.1f}%"
            )
        

        
        st.markdown("---")
        
        # Tabla de resultados mejorada
        st.markdown("#### 📋 Tabla de Resultados")
        
        # Preparar datos para mostrar
        display_df = df[[
            'displayName.text',
            'formattedAddress', 
            'nationalPhoneNumber',
            'websiteUri',
            'scraped_emails',
            'rating',
            'userRatingCount'
        ]].copy()
        
        # Renombrar columnas para mejor visualización
        display_df.columns = [
            '🏢 Nombre',
            '📍 Dirección',
            '📞 Teléfono',
            '🌐 Website',
            '📧 Emails',
            '⭐ Rating',
            '👥 Opiniones'
        ]
        
        # Mostrar tabla con configuración mejorada
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                '🌐 Website': st.column_config.LinkColumn("🌐 Website"),
                '⭐ Rating': st.column_config.NumberColumn(
                    "⭐ Rating",
                    format="%.1f ⭐"
                ),
                '👥 Opiniones': st.column_config.NumberColumn(
                    "👥 Opiniones",
                    format="%d"
                )
            }
        )
        
        # Botones de descarga mejorados
        st.markdown("#### 💾 Opciones de Descarga")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV completo
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📄 Descargar CSV Completo",
                data=csv_buffer.getvalue(),
                file_name=f"leads_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # CSV filtrado (solo con emails)
            df_with_emails = df[df['scraped_emails'].notna() & (df['scraped_emails'] != '')]
            if not df_with_emails.empty:
                csv_buffer_filtered = io.StringIO()
                df_with_emails.to_csv(csv_buffer_filtered, index=False)
                st.download_button(
                    label="📧 Solo con Emails",
                    data=csv_buffer_filtered.getvalue(),
                    file_name=f"leads_emails_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Sin registros con emails")
        
        with col3:
            # Link a Google Sheets
            try:
                sheets_manager = GoogleSheetsManager()
                sheets_url = sheets_manager.get_sheet_url()
                st.link_button(
                    "☁️ Ver en Google Sheets",
                    sheets_url,
                    use_container_width=True
                )
            except:
                st.info("Google Sheets no disponible")
    
    else:
        st.error("❌ No se pudieron obtener resultados")

def show_help_section():
    """Muestra la sección de ayuda actualizada"""
    st.markdown("""
    <div class="help-tab">
    
    ### 📖 Guía de Uso Actualizada
    
    **1. Dashboard Histórico:**
    - **📊 Estadísticas:** Ve el resumen de todas tus búsquedas anteriores
    - **📈 Eficiencia:** Analiza las tasas de extracción de emails y sitios web
    - **🕒 Actividad:** Revisa tus búsquedas más recientes y populares
    
    **2. Configuración de Búsqueda:**
    - **Tipo de negocio:** Sé específico (ej: "restaurante italiano", "gimnasio 24 horas")
    - **Ubicación:** Usa barrios o zonas específicas (ej: "Palermo, Buenos Aires")
    
    **3. Proceso Automático:**
    - **🌐 Web Scraping:** Siempre activo - extrae emails y redes sociales automáticamente
    - **☁️ Google Sheets:** Siempre activo - guarda automáticamente en tu hoja de cálculo
    
    **4. Proceso de Búsqueda en Tiempo Real:**
    - **Fase 1:** Búsqueda en Google Places (encuentra todos los lugares disponibles)
    - **Fase 2:** Web scraping para extraer emails y contactos adicionales
    - **Fase 3:** Subida automática a Google Sheets
    
    **5. Interpretación de Resultados:**
    - **📍 Lugares:** Total de negocios encontrados
    - **📧 Emails:** Contactos de email extraídos de sitios web
    - **⭐ Rating:** Calificación promedio del negocio
    
    **6. Consejos para Mejores Resultados:**
    - Usa términos específicos y combinaciones
    - Prueba diferentes ubicaciones (barrios, calles principales)
    - Activa todas las opciones para obtener información completa
    - Descarga en CSV para análisis posterior
    
    **7. Tiempos Estimados:**
    - 10-50 lugares: 1-2 minutos
    - 50-200 lugares: 3-8 minutos
    - 200+ lugares: 8-15 minutos
    
    </div>
    """, unsafe_allow_html=True)

# Configuración de autenticación
def get_admin_password():
    """Obtiene la contraseña de administrador desde secrets o fallback"""
    try:
        return st.secrets["app"]["admin_password"]
    except (KeyError, AttributeError):
        # Fallback para desarrollo local
        return "CotiVentasB2B2025"

def show_login_screen():
    """Muestra la pantalla de login"""
    st.markdown("""
    <div class="login-container">
        <h1>🔐 ACCESO RESTRINGIDO</h1>
        <p>Esta aplicación requiere autenticación para acceder</p>
        <p>COTI Lead Generator - Sistema Protegido</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centrar el formulario de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("#### 🔑 Ingresa la contraseña de acceso")
            password = st.text_input(
                "Contraseña:",
                type="password",
                placeholder="Introduce tu contraseña...",
                help="Contacta al administrador si no tienes acceso"
            )
            
            col1_btn, col2_btn, col3_btn = st.columns([1, 2, 1])
            with col2_btn:
                login_button = st.form_submit_button(
                    "🚀 Acceder", 
                    type="primary",
                    use_container_width=True
                )
            
            if login_button:
                if password == get_admin_password():
                    st.session_state.authenticated = True
                    st.success("✅ ¡Acceso concedido! Redirigiendo...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ Contraseña incorrecta. Intenta nuevamente.
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Información adicional
    st.markdown("---")
    st.info("🔒 **Seguridad:** Esta aplicación procesa datos sensibles de negocios y requiere autenticación.")

def show_logout_option():
    """Muestra opción de logout en el sidebar"""
    with st.sidebar:
        st.markdown("### 👤 Sesión Activa")
        st.success("✅ Autenticado correctamente")
        
        if st.button("🚪 Cerrar Sesión", type="secondary"):
            st.session_state.authenticated = False
            st.success("👋 Sesión cerrada correctamente")
            time.sleep(1)
            st.rerun()

def main_app():
    """Función principal de la aplicación"""
    initialize_session_state()
    
    # Verificar autenticación
    if not st.session_state.authenticated:
        show_login_screen()
        return
    
    # Mostrar opción de logout
    show_logout_option()
    
    create_header()
    
    # Crear tabs
    tab1, tab2 = st.tabs(["🚀 Generador", "❓ Ayuda"])
    
    with tab1:
        # Dashboard histórico
        show_dashboard()
        
        # Mini instructivo
        show_instructivo()
        
        # Sección de configuración mejorada
        st.markdown("""
        <div class="config-section">
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Configuración de Búsqueda")
        
        # Campos principales alineados
        col1, col2 = st.columns(2)
        
        with col1:
            query = st.text_input(
                "🔍 Tipo de negocio",
                value="restaurant",
                help="Especifica qué tipo de negocio buscas (ej: restaurantes, cafeterías, gimnasios, dentistas)",
                placeholder="Ejemplo: restaurante italiano"
            )
        
        with col2:
            location = st.text_input(
                "📍 Ubicación",
                value="Buenos Aires, Argentina",
                help="Ciudad, barrio o dirección específica donde realizar la búsqueda",
                placeholder="Ejemplo: Palermo, Buenos Aires"
            )
        
        # Configurar opciones siempre activadas (no mostrar en UI)
        include_scraping = True  # Siempre hacer web scraping
        save_to_sheets = True    # Siempre guardar en Google Sheets
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Botón de búsqueda centrado y mejorado
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_button = st.button(
                "🚀 Iniciar Búsqueda Completa",
                type="primary",
                use_container_width=True,
                disabled=not query or not location
            )
        
        # Validación de entrada
        if not query or not location:
            st.warning("⚠️ Por favor completa el tipo de negocio y la ubicación para continuar")
        
        # Ejecutar búsqueda
        if search_button:
            with st.spinner("🔄 Preparando búsqueda..."):
                result_df, message = execute_search(
                    query, location,
                    include_scraping, save_to_sheets
                )
                
                if result_df is not None:
                    st.session_state.results_df = result_df
                    st.session_state.search_completed = True
        
        # Mostrar resultados si existen
        if st.session_state.search_completed and st.session_state.results_df is not None:
            st.markdown("---")
            show_results_section(st.session_state.results_df, "Búsqueda completada exitosamente")
    
    with tab2:
        show_help_section()

if __name__ == "__main__":
    main_app() 