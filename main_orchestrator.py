#!/usr/bin/env python3
"""
Main Orchestrator - Flujo Principal de Generación de Leads

Orquesta el proceso completo:
1. Llama a GooglePlacesFetcher para obtener datos de negocios.
2. Llama a WebsiteScraper para enriquecer los datos con información de contacto.
3. Llama a GoogleSheetsManager para subir los datos finales a la nube.
"""

import pandas as pd
import logging
import re
import streamlit as st
from google_places_fetcher import GooglePlacesFetcher
from website_scraper import WebsiteScraper
from google_sheets_manager import GoogleSheetsManager

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_api_keys():
    """
    Obtiene las API keys desde Streamlit secrets o variables de entorno
    """
    try:
        # Intentar obtener desde Streamlit secrets primero
        google_api_key = st.secrets["google"]["places_api_key"]
        return google_api_key
    except (KeyError, AttributeError):
        # Fallback a valores hardcodeados para desarrollo
        logger.warning("⚠️ Usando API key hardcodeada - configura st.secrets para producción")
        google_api_key = "YOUR_GOOGLE_PLACES_API_KEY_HERE"
        return google_api_key

def clean_phone_number(phone):
    """
    Limpia y formatea un número de teléfono para WhatsApp Argentina (+54 9 código área número)
    """
    if not phone or pd.isna(phone):
        return ""
    
    # Convertir a string y limpiar
    phone = str(phone).strip()
    
    # Remover caracteres no numéricos excepto el +
    phone_clean = re.sub(r'[^\d+]', '', phone)
    
    # Si ya está en formato WhatsApp correcto (+54 9), mantenerlo
    if phone_clean.startswith('+549'):
        return phone_clean
    
    # Si tiene +54 pero no el 9, agregarlo
    if phone_clean.startswith('+54') and not phone_clean.startswith('+549'):
        # Extraer el número después del +54
        number_part = phone_clean[3:]
        return f"+549{number_part}"
    
    # Si empieza con 54 (sin +), agregar + y 9
    if phone_clean.startswith('54') and not phone_clean.startswith('549'):
        number_part = phone_clean[2:]
        return f"+549{number_part}"
    
    # Si empieza con 549, solo agregar +
    if phone_clean.startswith('549'):
        return f"+{phone_clean}"
    
    # Números de Buenos Aires (011 o 11)
    if phone_clean.startswith('011'):
        number_part = phone_clean[3:]  # Remover 011
        return f"+54911{number_part}"
    elif phone_clean.startswith('11'):
        number_part = phone_clean[2:]  # Remover 11
        return f"+54911{number_part}"
    
    # Otros códigos de área argentinos con 0 inicial (ej: 0341, 0351, etc.)
    if phone_clean.startswith('0') and len(phone_clean) >= 11:
        # Remover el 0 inicial y agregar +549
        number_part = phone_clean[1:]
        return f"+549{number_part}"
    
    # Para otros números argentinos (códigos de área), asumir que necesitan +54 9
    # Si el número tiene 10 dígitos o más, probablemente ya incluye código de área
    if len(phone_clean) >= 10:
        return f"+549{phone_clean}"
    
    # Para números más cortos, asumir Buenos Aires
    return f"+54911{phone_clean}"

def classify_url(url):
    """
    Clasifica una URL como sitio web real o red social
    Retorna: ('website', url) o ('facebook', url) o ('instagram', url) o ('other_social', url)
    """
    if not url or pd.isna(url):
        return 'empty', ''
    
    url_str = str(url).lower().strip()
    
    # Verificar redes sociales específicas
    if 'facebook.com' in url_str or 'fb.com' in url_str:
        return 'facebook', url
    elif 'instagram.com' in url_str or 'instagr.am' in url_str:
        return 'instagram', url
    elif any(domain in url_str for domain in ['twitter.com', 'linkedin.com', 'youtube.com', 'tiktok.com']):
        return 'other_social', url
    else:
        # Es un sitio web real
        return 'website', url

def separate_social_media_data(social_media_string):
    """
    Separa las redes sociales en Facebook e Instagram
    """
    if not social_media_string or pd.isna(social_media_string):
        return "", ""
    
    facebook_url = ""
    instagram_url = ""
    
    social_links = str(social_media_string).split(';')
    
    for link in social_links:
        link = link.strip()
        if link.startswith('facebook:'):
            facebook_url = link.replace('facebook:', '').strip()
        elif link.startswith('instagram:'):
            instagram_url = link.replace('instagram:', '').strip()
    
    return facebook_url, instagram_url

def clean_dataframe_for_sheets(df, search_query="", search_location=""):
    """
    Limpia el DataFrame eliminando valores NaN y preparándolo para Google Sheets
    """
    logger.info("🧹 Limpiando datos para Google Sheets...")
    
    # Reemplazar NaN con strings vacíos
    df_clean = df.fillna('')
    
    # Agregar información de la búsqueda realizada
    if search_query:
        df_clean['search_query'] = search_query
        logger.info(f"🔍 Tipo de negocio agregado: {search_query}")
    
    if search_location:
        df_clean['search_location'] = search_location
        logger.info(f"📍 Lugar buscado agregado: {search_location}")
    
    # Limpiar formato de teléfonos
    if 'nationalPhoneNumber' in df_clean.columns:
        df_clean['nationalPhoneNumber'] = df_clean['nationalPhoneNumber'].apply(clean_phone_number)
        logger.info("📱 Teléfonos limpiados y formateados")
    
    # Separar y consolidar redes sociales de múltiples fuentes
    facebook_urls = []
    instagram_urls = []
    
    # Fuente 1: Redes sociales extraídas por web scraping
    if 'social_media_links' in df_clean.columns:
        social_media_split = df_clean['social_media_links'].apply(separate_social_media_data)
        scraped_facebook = [x[0] for x in social_media_split]
        scraped_instagram = [x[1] for x in social_media_split]
    else:
        scraped_facebook = [''] * len(df_clean)
        scraped_instagram = [''] * len(df_clean)
    
    # Fuente 2: Redes sociales de Google Places (clasificadas en transform_places_data)
    places_facebook = df_clean.get('places_facebook_url', [''] * len(df_clean))
    places_instagram = df_clean.get('places_instagram_url', [''] * len(df_clean))
    
    # Consolidar: priorizar web scraping, luego Google Places
    for i in range(len(df_clean)):
        # Facebook: usar scraped si existe, sino usar places
        fb_final = scraped_facebook[i] if scraped_facebook[i] else str(places_facebook.iloc[i] if hasattr(places_facebook, 'iloc') else places_facebook[i] if i < len(places_facebook) else '')
        facebook_urls.append(fb_final)
        
        # Instagram: usar scraped si existe, sino usar places  
        ig_final = scraped_instagram[i] if scraped_instagram[i] else str(places_instagram.iloc[i] if hasattr(places_instagram, 'iloc') else places_instagram[i] if i < len(places_instagram) else '')
        instagram_urls.append(ig_final)
    
    df_clean['facebook_url'] = facebook_urls
    df_clean['instagram_url'] = instagram_urls
    
    # Eliminar columnas temporales
    if 'places_facebook_url' in df_clean.columns:
        df_clean = df_clean.drop(['places_facebook_url', 'places_instagram_url'], axis=1)
    
    logger.info("📱 Redes sociales consolidadas desde múltiples fuentes")
    
    # Convertir listas a strings si existen
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str)
            # Limpiar representaciones de listas como "['item1', 'item2']"
            df_clean[col] = df_clean[col].str.replace(r"^\['|'\]$", "", regex=True)
            df_clean[col] = df_clean[col].str.replace(r"', '", "; ", regex=True)
    
    # Asegurar que no hay valores None
    df_clean = df_clean.replace('None', '')
    df_clean = df_clean.replace('nan', '')
    df_clean = df_clean.replace('NaN', '')
    
    logger.info(f"✅ Datos limpios: {len(df_clean)} filas, {len(df_clean.columns)} columnas")
    return df_clean

def transform_places_data(places_results):
    """
    Transforma la estructura de datos de GooglePlacesFetcher al formato esperado por el sistema
    """
    logger.info("🔄 Transformando estructura de datos de Google Places...")
    
    transformed_data = []
    for place in places_results:
        # Clasificar la URL del sitio web
        website_url = place.get('website', '')
        url_type, clean_url = classify_url(website_url)
        
        # Inicializar campos
        final_website = ''
        places_facebook = ''
        places_instagram = ''
        
        # Asignar según el tipo de URL
        if url_type == 'website':
            final_website = clean_url
        elif url_type == 'facebook':
            places_facebook = clean_url
        elif url_type == 'instagram':
            places_instagram = clean_url
        # Si es 'other_social' o 'empty', no asignamos nada
        
        transformed_place = {
            'place_id': place.get('place_id', ''),
            'displayName.text': place.get('name', ''),
            'formattedAddress': place.get('address', ''),
            'rating': place.get('rating', ''),
            'userRatingCount': place.get('user_ratings_total', ''),
            'websiteUri': final_website,  # Solo sitios web reales
            'nationalPhoneNumber': place.get('phone', ''),
            'latitude': place.get('latitude', ''),
            'longitude': place.get('longitude', ''),
            'types': str(place.get('types', [])),  # Convertir lista a string
            # Campos temporales para redes sociales de Google Places
            'places_facebook_url': places_facebook,
            'places_instagram_url': places_instagram
        }
        transformed_data.append(transformed_place)
    
    logger.info(f"✅ Transformados {len(transformed_data)} registros al formato correcto")
    return transformed_data

def main(query="cotillones", location="Once, Buenos Aires, Argentina", max_results=None, progress_callback=None):
    """
    Función principal que orquesta todo el flujo de trabajo.
    
    Args:
        query (str): Tipo de negocio a buscar
        location (str): Ubicación geográfica
        max_results (int): Límite máximo de resultados (None = sin límite)
        progress_callback (function): Callback para reportar progreso en tiempo real
    """
    print("=" * 60)
    print("🚀 INICIANDO ORQUESTADOR DE GENERACIÓN DE LEADS 🚀")
    print("=" * 60)

    # --- Configuración del Proceso ---
    GOOGLE_API_KEY = get_api_keys()

    try:
        # --- PASO 1: OBTENER DATOS DE GOOGLE PLACES ---
        logger.info("--- INICIANDO PASO 1: Google Places Fetcher ---")
        if progress_callback:
            progress_callback("places_searching", f"Inicializando búsqueda de '{query}' en '{location}'...", 0)
        
        # Crear un callback anidado para el fetcher
        def places_fetcher_progress(current, total, found_count, phase="grid"):
            if progress_callback:
                if phase == "grid":
                    # Estimación de tiempo
                    # (Esto es una heurística y puede necesitar ajuste)
                    time_per_point = 10 # segundos por punto de grilla (promedio)
                    time_remaining = (total - current) * time_per_point
                    
                    progress_callback(
                        "places_progress", 
                        f"Procesando grilla: Punto {current}/{total}. "
                        f"Lugares únicos encontrados: {found_count}. "
                        f"Tiempo estimado restante: ~{time_remaining // 60} min {time_remaining % 60} seg.",
                        (current, total, found_count)
                    )
                elif phase == "details":
                    progress_callback(
                        "places_details_progress",
                        f"Obteniendo detalles: {current}/{total}...",
                        (current, total)
                    )

        places_fetcher = GooglePlacesFetcher(api_key=GOOGLE_API_KEY, progress_callback=places_fetcher_progress)
        places_results_raw = places_fetcher.search_places_grid(query, location)
        
        if not places_results_raw:
            logger.error("El Paso 1 (Google Places) no devolvió resultados. Abortando.")
            return None, "No se encontraron resultados en Google Places"
        
        # Informar progreso detallado durante la búsqueda
        if progress_callback:
            progress_callback("places_searching", f"Procesando {len(places_results_raw)} lugares encontrados...", len(places_results_raw))
        
        # Transformar la estructura de datos al formato esperado
        places_results = transform_places_data(places_results_raw)
        
        # Aplicar límite si se especifica
        if max_results and len(places_results) > max_results:
            places_results = places_results[:max_results]
            logger.info(f"🔬 Limitando resultados a {max_results} para procesamiento")
        
        # Convertir a DataFrame
        places_df = pd.DataFrame(places_results)
        logger.info(f"✅ Datos de Google Places procesados: {len(places_df)} registros")
        
        if progress_callback:
            progress_callback("places_found", f"Encontrados {len(places_df)} lugares en {location}", len(places_df))
        
        # --- PASO 2: SCRAPEAR SITIOS WEB ---
        logger.info("\n--- INICIANDO PASO 2: Website Scraper ---")
        
        # Contar sitios web disponibles
        sites_with_url = places_df['websiteUri'].notna().sum()
        if progress_callback:
            progress_callback("scraping_start", f"Iniciando scraping de {sites_with_url} sitios web...", sites_with_url)
        
        try:
            website_scraper = WebsiteScraper()
            
            # Configurar callback para el web scraper
            def scraping_progress_callback(processed, total, current_site=""):
                if progress_callback:
                    progress_percentage = int((processed / total) * 100) if total > 0 else 0
                    progress_callback("scraping_progress", f"Procesando sitio web {processed}/{total}: {current_site[:50]}...", progress_percentage)
            
            # Ejecutar scraping con progreso
            scraped_df = website_scraper.run_scraping_process_from_dataframe(
                places_df, 
                progress_callback=scraping_progress_callback
            )
            logger.info("✅ Paso 2 (Website Scraper) completado.")
            if progress_callback:
                # Calcular emails encontrados
                emails_found = scraped_df['scraped_emails'].str.count('@').sum()
                progress_callback("scraping_complete", "Scraping de sitios web finalizado.", emails_found)

        except Exception as e:
            logger.error(f"🚨 OCURRIÓ UN ERROR EN EL PASO 2 (Website Scraper): {e}")
            scraped_df = places_df # Continuar con los datos originales
            if progress_callback:
                progress_callback("error", f"Error en scraping: {e}", 0)

        # --- LIMPIEZA FINAL DE DATOS ---
        logger.info("\n--- LIMPIEZA FINAL DE DATOS ---")
        
        final_df = clean_dataframe_for_sheets(scraped_df, search_query=query, search_location=location)

        # --- PASO 3: SUBIR DATOS A GOOGLE SHEETS ---
        logger.info("\n--- INICIANDO PASO 3: Google Sheets Manager ---")
        if progress_callback:
            progress_callback("sheets_start", f"Subiendo {len(final_df)} registros a Google Sheets...", len(final_df))
        
        sheets_manager = GoogleSheetsManager()
        success = sheets_manager.upload_data(final_df)

        if success:
            logger.info("\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE! 🎉")
            stats = sheets_manager.get_stats()
            total_records = stats.get('total_records', 0)
            
            # Crear mensaje de resumen detallado
            summary_message = f"""
            ✅ Proceso completado exitosamente para '{query}' en '{location}'
            📊 Resumen final:
            • {len(final_df)} lugares procesados
            • {scraped_df['scraped_emails'].str.count('@').sum()} emails extraídos
            • {total_records} registros totales en Google Sheets
            """
            
            if progress_callback:
                progress_callback("sheets_complete", f"Datos subidos exitosamente: {total_records} registros totales", total_records)
                
            return final_df, summary_message.strip()
        else:
            logger.error("\n❌ HUBO UN ERROR DURANTE LA CARGA A GOOGLE SHEETS.")
            error_message = f"""
            ⚠️ Datos procesados correctamente pero error al subir a Google Sheets
            📊 Resumen:
            • {len(final_df)} lugares procesados
            • {scraped_df['scraped_emails'].str.count('@').sum()} emails extraídos
            • Error en subida a Google Sheets
            """
            
            if progress_callback:
                progress_callback("sheets_complete", "Error al subir a Google Sheets", 0)
                
            return final_df, error_message.strip()

    except Exception as e:
        logger.error(f"\n🚨 OCURRIÓ UN ERROR INESPERADO EN EL ORQUESTADOR: {e}", exc_info=True)
        error_message = f"Error inesperado durante el proceso: {str(e)}"
        return None, error_message

if __name__ == "__main__":
    result_df, message = main()
    print(f"\n📊 Resultado: {message}")
    if result_df is not None:
        print(f"📈 Procesados: {len(result_df)} registros") 