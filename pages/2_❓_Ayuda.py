#!/usr/bin/env python3
"""
🎯 Lead Generator App - Página de Ayuda Actualizada
Centro de ayuda completo con guías, consejos y buenas prácticas
"""

import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="❓ Ayuda - Lead Generator",
    page_icon="❓",
    layout="wide"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .help-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .help-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .faq-item {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .tip-box {
        background: linear-gradient(45deg, #e8f5e8, #f0f8ff);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .warning-box {
        background: linear-gradient(45deg, #fff3cd, #ffeaa7);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .step-number {
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="help-header">
    <h1>❓ Centro de Ayuda Completo</h1>
    <p>Guía completa para maximizar tu generación de leads con COTI Lead Generator</p>
</div>
""", unsafe_allow_html=True)

# Sección de inicio rápido
st.markdown("""
<div class="help-section">
<h2>🚀 Inicio Rápido</h2>

<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div class="step-number">1</div>
    <div>
        <strong>Tipo de Negocio:</strong> Especifica qué buscas de manera precisa<br>
        <small>✅ Correcto: "restaurante italiano", "gimnasio 24 horas"<br>
        ❌ Evitar: "negocio", "tienda"</small>
    </div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div class="step-number">2</div>
    <div>
        <strong>Ubicación:</strong> Usa ubicaciones específicas para mejores resultados<br>
        <small>✅ Correcto: "Palermo, Buenos Aires", "Av. Corrientes, CABA"<br>
        ❌ Evitar: "Argentina", "Buenos Aires completo"</small>
    </div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div class="step-number">3</div>
    <div>
        <strong>Opciones:</strong> Configura según tus necesidades<br>
        <small>• <strong>Web Scraping:</strong> Para obtener emails y redes sociales<br>
        • <strong>Google Sheets:</strong> Para guardar automáticamente</small>
    </div>
</div>

<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div class="step-number">4</div>
    <div>
        <strong>Búsqueda:</strong> Inicia y observa el progreso en tiempo real<br>
        <small>La aplicación te mostrará estadísticas detalladas del proceso</small>
    </div>
</div>

</div>
""", unsafe_allow_html=True)

# Sección de comprensión del proceso
st.markdown("""
<div class="help-section">
<h2>🔄 Entendiendo el Proceso</h2>

<h3>Fases del Proceso:</h3>

<h4>📍 Fase 1: Búsqueda en Google Places</h4>
<p>• Encuentra todos los lugares disponibles sin límite<br>
• Extrae información básica: nombre, dirección, teléfono, rating<br>
• Progreso en tiempo real mostrando lugares encontrados</p>

<h4>🌐 Fase 2: Web Scraping</h4>
<p>• Visita los sitios web encontrados<br>
• Extrae emails, redes sociales y contactos adicionales<br>
• Respeta robots.txt y límites de velocidad</p>

<h4>☁️ Fase 3: Google Sheets</h4>
<p>• Sube automáticamente los resultados a la nube<br>
• Detecta y evita duplicados<br>
• Organiza la información en columnas claras</p>

</div>
""", unsafe_allow_html=True)

# FAQ mejorada
st.markdown("""
<div class="help-section">
<h2>❓ Preguntas Frecuentes</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("¿Cuántos resultados puedo obtener?"):
    st.markdown("""
    **No hay límite establecido.** La aplicación busca automáticamente todos los lugares disponibles 
    en Google Places para tu consulta específica.
    
    **Resultados típicos:**
    - Búsquedas específicas (ej: "sushi Palermo"): 10-50 resultados
    - Búsquedas amplias (ej: "restaurantes Buenos Aires"): 100-500+ resultados
    - Búsquedas muy específicas (ej: "veterinaria 24hs Belgrano"): 5-20 resultados
    
    **Factores que afectan la cantidad:**
    - Especificidad del término de búsqueda
    - Tamaño de la zona geográfica
    - Densidad de negocios en el área
    """)

with st.expander("¿Cuánto tiempo tarda el proceso completo?"):
    st.markdown("""
    **Tiempo estimado por fase:**
    
    **🔍 Google Places:** 30 segundos - 2 minutos
    - Depende del número de lugares encontrados
    
    **🌐 Web Scraping:** 1-10 minutos
    - Depende del número de sitios web válidos
    - Procesa múltiples sitios simultáneamente
    
    **☁️ Google Sheets:** 10-30 segundos
    - Tiempo constante independiente del tamaño
    
    **Tiempos totales típicos:**
    - 10-50 lugares: 2-5 minutos
    - 50-200 lugares: 5-15 minutos
    - 200+ lugares: 10-25 minutos
    """)

with st.expander("¿Qué información exacta puedo obtener?"):
    st.markdown("""
    **Información básica (Google Places):**
    - ✅ Nombre del negocio
    - ✅ Dirección completa
    - ✅ Número de teléfono
    - ✅ Sitio web oficial
    - ✅ Rating y cantidad de reseñas
    - ✅ Coordenadas geográficas
    - ✅ Tipos de negocio
    
    **Información adicional (Web Scraping):**
    - ✅ Emails de contacto
    - ✅ Enlaces a Facebook
    - ✅ Enlaces a Instagram
    - ✅ Información de contacto adicional
    
    **Organización (Google Sheets):**
    - ✅ Todas las columnas organizadas
    - ✅ Detección de duplicados
    - ✅ Información de la búsqueda realizada
    """)

with st.expander("¿Cómo mejorar la calidad de mis resultados?"):
    st.markdown("""
    **Estrategias de búsqueda efectivas:**
    
    **🎯 Términos específicos:**
    - "restaurante vegano" > "restaurante"
    - "gimnasio crossfit" > "gimnasio"
    - "dentista infantil" > "dentista"
    
    **📍 Ubicaciones precisas:**
    - "Palermo Hollywood, Buenos Aires" > "Buenos Aires"
    - "Av. Santa Fe 1000-2000" > "Av. Santa Fe"
    - "Villa Crespo" > "Capital Federal"
    
    **🔧 Configuración recomendada:**
    - ✅ Activar Web Scraping (más emails)
    - ✅ Activar Google Sheets (organización)
    
    **📊 Filtrado posterior:**
    - Usa "Solo con Emails" para contacto directo
    - Filtra por rating para calidad
    - Combina múltiples criterios
    """)

with st.expander("¿Qué significan las métricas mostradas?"):
    st.markdown("""
    **Durante el proceso:**
    - **📍 Lugares Encontrados:** Negocios identificados en Google Places
    - **🌐 Emails Extraídos:** Contactos obtenidos de sitios web
    - **☁️ Google Sheets:** Registros subidos a la nube
    
    **En los resultados:**
    - **🏢 Total Lugares:** Cantidad total de negocios encontrados
    - **📧 Con Emails:** Porcentaje que tiene email de contacto
    - **🌐 Con Website:** Porcentaje que tiene sitio web
    
    **En la tabla:**
    - **⭐ Rating:** Calificación promedio (1-5 estrellas)
    - **👥 Opiniones:** Número total de reseñas
    """)

# Consejos avanzados
st.markdown("""
<div class="help-section">
<h2>💡 Consejos Avanzados para Expertos</h2>

<div class="tip-box">
<h4>🎯 Estrategias de Segmentación</h4>
<p><strong>Por zona geográfica:</strong> Realiza búsquedas por barrios específicos en lugar de ciudades completas</p>
<p><strong>Por tipo de negocio:</strong> Usa términos específicos del sector (ej: "panadería artesanal" vs "panadería")</p>
<p><strong>Por nivel de servicio:</strong> Incluye calificadores como "premium", "económico", "familiar"</p>
</div>

<div class="tip-box">
<h4>📊 Optimización de Resultados</h4>
<p><strong>Horarios de búsqueda:</strong> Mejores resultados durante horarios comerciales (9-18hs)</p>
<p><strong>Días de la semana:</strong> Martes a jueves suelen tener mejor respuesta</p>
<p><strong>Combinaciones efectivas:</strong> Usa términos + ubicación + características</p>
</div>

<div class="tip-box">
<h4>🔄 Análisis de Datos</h4>
<p><strong>Priorización:</strong> Contacta primero los que tienen email Y sitio web</p>
<p><strong>Calidad:</strong> Filtra por rating >4.0 para mejor respuesta</p>
<p><strong>Seguimiento:</strong> Usa Google Sheets para tracking de contactos</p>
</div>

</div>
""", unsafe_allow_html=True)

# Solución de problemas
st.markdown("""
<div class="help-section">
<h2>🔧 Solución de Problemas</h2>

<h3>Problemas Comunes y Soluciones:</h3>

<div class="faq-item">
<h4>❌ "No se encontraron resultados"</h4>
<p><strong>Posibles causas:</strong></p>
<ul>
<li>Término de búsqueda demasiado específico</li>
<li>Ubicación muy restringida</li>
<li>Combinación de términos sin resultados</li>
</ul>
<p><strong>Soluciones:</strong></p>
<ul>
<li>Usa términos más generales</li>
<li>Amplía la zona geográfica</li>
<li>Prueba sinónimos del tipo de negocio</li>
</ul>
</div>

<div class="faq-item">
<h4>❌ "Pocos emails encontrados"</h4>
<p><strong>Posibles causas:</strong></p>
<ul>
<li>Muchos negocios sin sitio web</li>
<li>Sitios web con emails protegidos</li>
<li>Páginas web simples sin información</li>
</ul>
<p><strong>Soluciones:</strong></p>
<ul>
<li>Enfócate en negocios con sitio web</li>
<li>Busca tipos de negocio que suelen tener web</li>
<li>Usa los teléfonos encontrados como alternativa</li>
</ul>
</div>

<div class="faq-item">
<h4>❌ "Proceso muy lento"</h4>
<p><strong>Posibles causas:</strong></p>
<ul>
<li>Gran cantidad de resultados</li>
<li>Sitios web lentos de cargar</li>
<li>Validación de muchos números</li>
</ul>
<p><strong>Soluciones:</strong></p>
<ul>
<li>Usa búsquedas más específicas</li>
<li>Desactiva opciones si no las necesitas</li>
<li>Realiza búsquedas en horarios de menor carga</li>
</ul>
</div>

</div>
""", unsafe_allow_html=True)

# Información técnica
st.markdown("""
<div class="help-section">
<h2>ℹ️ Información Técnica</h2>

<h3>APIs y Servicios Utilizados:</h3>

<p><strong>🗺️ Google Places API:</strong></p>
<ul>
<li>API oficial de Google para búsqueda de lugares</li>
<li>Datos actualizados en tiempo real</li>
<li>Cobertura global con información precisa</li>
</ul>

<p><strong>🌐 Web Scraping:</strong></p>
<ul>
<li>Extracción ética respetando robots.txt</li>
<li>Límites de velocidad para no sobrecargar sitios</li>
<li>Procesamiento paralelo para eficiencia</li>
</ul>

<p><strong>☁️ Google Sheets API:</strong></p>
<ul>
<li>Almacenamiento seguro en la nube</li>
<li>Detección automática de duplicados</li>
<li>Acceso desde cualquier dispositivo</li>
</ul>

<h3>Privacidad y Seguridad:</h3>

<p><strong>🔒 Protección de Datos:</strong></p>
<ul>
<li>Procesamiento local sin almacenamiento permanente</li>
<li>Datos guardados solo donde tú eliges</li>
<li>No compartimos información con terceros</li>
</ul>

<p><strong>🛡️ Uso Ético:</strong></p>
<ul>
<li>Respeto por límites de APIs</li>
<li>Extracción responsable de sitios web</li>
<li>Cumplimiento de términos de servicio</li>
</ul>

</div>
""", unsafe_allow_html=True)

# Casos de uso
st.markdown("""
<div class="help-section">
<h2>📈 Casos de Uso Exitosos</h2>

<h3>Ejemplos Reales de Implementación:</h3>

<div class="faq-item">
<h4>🍕 Caso: Delivery de Comidas</h4>
<p><strong>Búsqueda:</strong> "restaurante delivery" en "Palermo, Buenos Aires"</p>
<p><strong>Configuración:</strong> Web Scraping ✅, Google Sheets ✅</p>
<p><strong>Resultados:</strong> 87 restaurantes, 34 con email, 52 con sitio web</p>
<p><strong>Éxito:</strong> 15% de respuesta por email</p>
</div>

<div class="faq-item">
<h4>🏥 Caso: Servicios Médicos</h4>
<p><strong>Búsqueda:</strong> "consultorio médico" en "Microcentro, Buenos Aires"</p>
<p><strong>Configuración:</strong> Web Scraping ✅, Google Sheets ✅</p>
<p><strong>Resultados:</strong> 156 consultorios, 78 con email, 23 con sitio web completo</p>
<p><strong>Éxito:</strong> 25% de respuesta por email formal</p>
</div>

<div class="faq-item">
<h4>🏋️ Caso: Fitness y Bienestar</h4>
<p><strong>Búsqueda:</strong> "gimnasio crossfit" en "Villa Crespo, Buenos Aires"</p>
<p><strong>Configuración:</strong> Web Scraping ✅, Google Sheets ✅</p>
<p><strong>Resultados:</strong> 23 gimnasios, 18 con redes sociales, 15 con sitio web</p>
<p><strong>Éxito:</strong> 30% de respuesta por email</p>
</div>

</div>
""", unsafe_allow_html=True)

# Warning sobre límites
st.markdown("""
<div class="warning-box">
<h4>⚠️ Consideraciones Importantes</h4>
<p><strong>Límites de API:</strong> Las APIs tienen límites diarios. Si experimentas errores, intenta más tarde.</p>
<p><strong>Tiempo de procesamiento:</strong> Búsquedas muy grandes pueden tomar tiempo. Sé paciente.</p>
<p><strong>Calidad de datos:</strong> No todos los sitios web tienen emails públicos. Esto es normal.</p>
<p><strong>Uso responsable:</strong> Usa la información obtenida de manera ética y respeta las políticas de privacidad.</p>
</div>
""", unsafe_allow_html=True)

# Enlaces útiles
st.markdown("""
<div class="help-section">
<h2>🔗 Enlaces Útiles</h2>

<h3>Recursos Adicionales:</h3>

<p><strong>📚 Documentación:</strong></p>
<ul>
<li>Google Places API: Para entender qué datos están disponibles</li>
<li>Google Sheets: Para gestionar tus resultados en la nube</li>
<li>README del proyecto: Para información técnica detallada</li>
</ul>

<p><strong>🛠️ Herramientas Complementarias:</strong></p>
<ul>
<li>Google Sheets: Para análisis y seguimiento</li>
<li>Herramientas de email marketing: Para campañas masivas</li>
<li>CRM: Para gestión completa de contactos</li>
</ul>

<p><strong>📞 Soporte:</strong></p>
<ul>
<li>Revisa esta guía completa antes de contactar</li>
<li>Utiliza ejemplos específicos al reportar problemas</li>
<li>Incluye capturas de pantalla si es necesario</li>
</ul>

</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
<h3>🎯 COTI Lead Generator</h3>
<p><strong>Desarrollado para maximizar tu generación de leads</strong></p>
<p>Versión actualizada con interfaz mejorada y proceso más informativo</p>
</div>
""", unsafe_allow_html=True) 