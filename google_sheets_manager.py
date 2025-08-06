#!/usr/bin/env python3
"""
Google Sheets Manager - Módulo de Carga

Responsabilidad: Conectar y subir datos a una hoja de cálculo de Google Sheets,
manejando la deduplicación de registros.
"""

import pandas as pd
from datetime import datetime
import logging
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    """Maneja la conexión y escritura a Google Sheets"""
    
    def __init__(self, credentials_file=None, spreadsheet_id=None):
        # Intentar obtener configuración desde st.secrets primero
        try:
            self.spreadsheet_id = spreadsheet_id or st.secrets["google_sheets"]["spreadsheet_id"]
            self.credentials_file = credentials_file or st.secrets["google_sheets"]["credentials_file"]
            self.use_secrets_auth = True
        except (KeyError, AttributeError):
            # Fallback a valores por defecto
            self.spreadsheet_id = spreadsheet_id or '1KjQMeQQ_3EO0MtfrSO7waTHtiZdTb7futHIA4yk6Xf8'
            self.credentials_file = credentials_file or 'google_credentials_coti.json'
            self.use_secrets_auth = False
            logger.warning("⚠️ Usando configuración hardcodeada - configura st.secrets para producción")
        
        self.service = None
        self.sheet_name = 'Leads Data'
        
        self.column_mapping = {
            'place_id': 'Place ID',
            'displayName.text': 'Nombre del Negocio',
            'formattedAddress': 'Dirección',
            'rating': 'Calificación (Google)',
            'userRatingCount': 'N° de Opiniones (Google)',
            'websiteUri': 'Sitio Web',
            'nationalPhoneNumber': 'Teléfono Principal',
            'scraped_emails': 'Emails Encontrados',
            'facebook_url': 'Facebook',
            'instagram_url': 'Instagram',
            'search_query': 'Búsqueda Realizada',
            'extraction_date': 'Fecha Extracción'
        }
        
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.connect()

    def connect(self):
        """Conecta a Google Sheets API usando st.secrets o archivo de credenciales"""
        try:
            if self.use_secrets_auth:
                # Usar credenciales desde st.secrets
                creds_info = dict(st.secrets["google_service_account"])
                creds = Credentials.from_service_account_info(creds_info, scopes=self.scopes)
            else:
                # Usar archivo de credenciales
                creds = Credentials.from_service_account_file(self.credentials_file, scopes=self.scopes)
            
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("✅ Conexión exitosa a Google Sheets API")
            self.ensure_sheet_exists()
        except Exception as e:
            logger.error(f"❌ Error conectando a Google Sheets: {e}")
            raise

    def ensure_sheet_exists(self):
        """Verifica que la hoja existe y configura los headers"""
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            sheet_titles = [s['properties']['title'] for s in sheets]
            if self.sheet_name not in sheet_titles:
                self.create_sheet()
            self.setup_headers()
        except HttpError as e:
            logger.error(f"❌ Error verificando/creando la hoja: {e}")

    def create_sheet(self):
        """Crea una nueva hoja en el spreadsheet"""
        try:
            body = {'requests': [{'addSheet': {'properties': {'title': self.sheet_name}}}]}
            self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
            logger.info(f"✅ Hoja '{self.sheet_name}' creada.")
        except HttpError as e:
            logger.error(f"❌ Error creando la hoja: {e}")
            raise

    def setup_headers(self):
        """Configura los headers de la hoja"""
        try:
            clean_headers = list(self.column_mapping.values())
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, 
                range=f"'{self.sheet_name}'!A1:Z1"
            ).execute()
            current_headers = result.get('values', [[]])[0]
            if current_headers != clean_headers:
                body = {'values': [clean_headers]}
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id, 
                    range=f"'{self.sheet_name}'!A1:Z1", 
                    valueInputOption='USER_ENTERED', 
                    body=body
                ).execute()
                logger.info("✅ Headers configurados/actualizados en Google Sheets.")
        except HttpError as e:
            logger.error(f"❌ Error configurando headers: {e}")

    def get_existing_data(self):
        """Obtiene todos los datos existentes de la hoja"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, 
                range=f"'{self.sheet_name}'!A:Z"
            ).execute()
            values = result.get('values', [])
            if len(values) <= 1: 
                return pd.DataFrame()
            
            headers = values[0]
            data = values[1:]
            
            # Asegurar que todas las filas tengan el mismo número de columnas que los encabezados
            data = [row + [''] * (len(headers) - len(row)) for row in data]

            df = pd.DataFrame(data, columns=headers)
            # Mapear de vuelta a nombres programáticos
            reverse_mapping = {v: k for k, v in self.column_mapping.items()}
            df.rename(columns=reverse_mapping, inplace=True)
            
            logger.info(f"📊 Datos existentes obtenidos: {len(df)} registros")
            return df
        except HttpError as e:
            logger.error(f"❌ Error obteniendo datos existentes: {e}")
            return pd.DataFrame()

    def check_for_duplicates(self, new_df, existing_df):
        """
        Verifica duplicados de manera más robusta usando múltiples criterios
        """
        if existing_df.empty:
            return new_df, 0
        
        logger.info("🔍 Verificando duplicados...")
        
        # Criterio 1: place_id (más confiable)
        existing_place_ids = set(existing_df['place_id'].dropna().tolist())
        mask_place_id = ~new_df['place_id'].isin(existing_place_ids)
        
        # Criterio 2: combinación de nombre + dirección (backup)
        existing_combinations = set()
        for _, row in existing_df.iterrows():
            name = str(row.get('displayName.text', '')).strip().lower()
            address = str(row.get('formattedAddress', '')).strip().lower()
            if name and address:
                existing_combinations.add(f"{name}|{address}")
        
        mask_combination = pd.Series([True] * len(new_df), index=new_df.index)
        for idx, row in new_df.iterrows():
            name = str(row.get('displayName.text', '')).strip().lower()
            address = str(row.get('formattedAddress', '')).strip().lower()
            if name and address:
                combination = f"{name}|{address}"
                if combination in existing_combinations:
                    mask_combination.loc[idx] = False
        
        # Combinar ambos criterios
        final_mask = mask_place_id & mask_combination
        unique_df = new_df[final_mask].copy()
        duplicates_count = len(new_df) - len(unique_df)
        
        logger.info(f"🔍 Análisis de duplicados:")
        logger.info(f"   - Registros nuevos: {len(new_df)}")
        logger.info(f"   - Duplicados encontrados: {duplicates_count}")
        logger.info(f"   - Registros únicos a insertar: {len(unique_df)}")
        
        return unique_df, duplicates_count

    def upload_data(self, df):
        """Sube datos a Google Sheets con detección mejorada de duplicados"""
        if df.empty:
            logger.warning("⚠️ No hay datos para subir a Google Sheets.")
            return False
        
        try:
            logger.info("--- INICIANDO PROCESO DE CARGA A GOOGLE SHEETS ---")
            
            # 1. Añadir metadatos
            df_with_meta = df.copy()
            df_with_meta['extraction_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 2. Obtener datos existentes y verificar duplicados
            existing_data = self.get_existing_data()
            unique_df, duplicates_count = self.check_for_duplicates(df_with_meta, existing_data)
            
            if duplicates_count > 0:
                logger.info(f"🔍 Se encontraron y omitieron {duplicates_count} duplicados.")
            
            if unique_df.empty:
                logger.info("✅ No hay registros nuevos para subir.")
                return True
            
            # 3. Preparar datos para subida
            start_row = len(existing_data) + 2
            programmatic_headers = list(self.column_mapping.keys())
            final_df = unique_df.reindex(columns=programmatic_headers, fill_value='')
            
            # 4. Convertir a valores y limpiar
            values = final_df.fillna('').astype(str).values.tolist()
            
            # 5. Subir a Google Sheets
            body = {'values': values}
            range_name = f"'{self.sheet_name}'!A{start_row}"
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, 
                range=range_name, 
                valueInputOption='USER_ENTERED', 
                body=body
            ).execute()
            
            logger.info(f"✅ Datos subidos exitosamente. {len(values)} filas nuevas agregadas.")
            logger.info(f"📊 Total de registros en la hoja: {len(existing_data) + len(values)}")
            return True
            
        except HttpError as e:
            logger.error(f"❌ Error de API subiendo datos: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado durante la carga: {e}")
            return False

    def print_stats(self):
        """Imprime estadísticas de la hoja"""
        stats = self.get_stats()
        print("\n📊 ESTADÍSTICAS FINALES DE GOOGLE SHEETS:")
        print("=" * 50)
        print(f"📋 Total de registros en la hoja: {stats.get('total_records', 0)}")
        print(f"🔗 URL de la Hoja: {self.get_sheet_url()}")

    def get_stats(self):
        """Obtiene estadísticas completas de la hoja"""
        try:
            existing_data = self.get_existing_data()
            
            if existing_data.empty:
                return {
                    'total_records': 0,
                    'emails_found': 0,
                    'websites_found': 0,
                    'unique_searches': 0,
                    'last_searches': [],
                    'search_distribution': {},
                    'recent_activity': []
                }
            
            # Estadísticas básicas
            total_records = len(existing_data)
            
            # Contar emails extraídos
            emails_found = 0
            if 'scraped_emails' in existing_data.columns:
                emails_found = sum(1 for x in existing_data['scraped_emails'] 
                                 if x and str(x).strip() and str(x) != 'nan' and '@' in str(x))
            
            # Contar sitios web
            websites_found = 0
            if 'websiteUri' in existing_data.columns:
                websites_found = sum(1 for x in existing_data['websiteUri'] 
                                   if x and str(x).strip() and str(x) != 'nan' and 'http' in str(x))
            
            # Búsquedas únicas realizadas
            unique_searches = 0
            search_distribution = {}
            if 'search_query' in existing_data.columns:
                search_queries = existing_data['search_query'].dropna()
                unique_searches = len(search_queries.unique())
                search_distribution = search_queries.value_counts().head(10).to_dict()
            
            # Últimas búsquedas (basado en fecha de extracción)
            last_searches = []
            recent_activity = []
            if 'extraction_date' in existing_data.columns:
                # Obtener las 5 fechas más recientes
                recent_data = existing_data.sort_values('extraction_date', ascending=False).head(50)
                
                # Últimas búsquedas únicas
                if 'search_query' in recent_data.columns:
                    last_searches = recent_data['search_query'].dropna().unique()[:5].tolist()
                
                # Actividad reciente (últimas 5 entradas con fecha y búsqueda)
                for _, row in recent_data.head(5).iterrows():
                    date = row.get('extraction_date', '')
                    query = row.get('search_query', '')
                    if date and query:
                        recent_activity.append({'date': date, 'query': query})
            
            return {
                'total_records': total_records,
                'emails_found': emails_found,
                'websites_found': websites_found,
                'unique_searches': unique_searches,
                'last_searches': last_searches,
                'search_distribution': search_distribution,
                'recent_activity': recent_activity
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {
                'total_records': 0,
                'emails_found': 0,
                'websites_found': 0,
                'unique_searches': 0,
                'last_searches': [],
                'search_distribution': {},
                'recent_activity': []
            }
            
    def get_sheet_url(self):
        """Obtiene la URL de la hoja de cálculo"""
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid=0"
    
    def cleanup_historical_urls(self):
        """
        FUNCIÓN OPCIONAL: Limpia URLs mal clasificadas en datos históricos
        Esta función reclasifica todas las URLs existentes en la hoja
        """
        try:
            from main_orchestrator import classify_url
            
            logger.info("🧹 Iniciando limpieza de URLs históricas...")
            
            # Obtener todos los datos existentes
            existing_data = self.get_existing_data()
            if existing_data.empty:
                logger.info("No hay datos para limpiar")
                return True
            
            # Contadores para reporte
            websites_moved = 0
            facebooks_added = 0
            instagrams_added = 0
            
            # Procesar cada fila
            for idx, row in existing_data.iterrows():
                website_url = row.get('websiteUri', '')
                current_facebook = row.get('facebook_url', '')
                current_instagram = row.get('instagram_url', '')
                
                if website_url and str(website_url) != 'nan':
                    url_type, clean_url = classify_url(website_url)
                    
                    # Si la URL del sitio web es realmente una red social
                    if url_type in ['facebook', 'instagram']:
                        # Limpiar el campo websiteUri
                        existing_data.at[idx, 'websiteUri'] = ''
                        websites_moved += 1
                        
                        # Mover a la columna correcta (solo si no hay una ya)
                        if url_type == 'facebook' and not current_facebook:
                            existing_data.at[idx, 'facebook_url'] = clean_url
                            facebooks_added += 1
                        elif url_type == 'instagram' and not current_instagram:
                            existing_data.at[idx, 'instagram_url'] = clean_url
                            instagrams_added += 1
            
            # Solo actualizar si hay cambios
            if websites_moved > 0:
                # Aquí se podría implementar la actualización completa del sheet
                # Por ahora solo reportamos los cambios que se harían
                logger.info(f"🔄 Cambios detectados en datos históricos:")
                logger.info(f"   - URLs movidas de Sitio Web: {websites_moved}")
                logger.info(f"   - Facebook URLs agregadas: {facebooks_added}")
                logger.info(f"   - Instagram URLs agregadas: {instagrams_added}")
                logger.info("💡 Para aplicar cambios, implementar actualización del sheet completo")
            else:
                logger.info("✅ No se encontraron URLs mal clasificadas en datos históricos")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error limpiando URLs históricas: {e}")
            return False 