#!/usr/bin/env python3
"""
Website Scraper - Módulo 2 del Flujo de Leads

Responsabilidad: Tomar un CSV con datos de negocios, visitar sus sitios web
y extraer información de contacto (emails, teléfonos, redes sociales).
"""

import requests
import pandas as pd
import re
import time
import random
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebsiteScraper:
    """
    Clase dedicada a scrapear sitios web para encontrar información de contacto.
    """
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.session = requests.Session()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        self.contact_keywords = ['contacto', 'contact', 'about', 'info', 'telefono', 'email']
        self.social_media_patterns = {
            'facebook': 'facebook.com', 'instagram': 'instagram.com', 'twitter': 'twitter.com',
            'linkedin': 'linkedin.com', 'youtube': 'youtube.com', 'tiktok': 'tiktok.com'
        }

    def get_random_headers(self):
        return {'User-Agent': random.choice(self.user_agents), 'Accept': 'text/html,application/xhtml+xml', 'Accept-Language': 'es-ES,es;q=0.9'}

    def is_real_website(self, url):
        if not url or pd.isna(url): return False
        social_domains = ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com', 'youtube.com', 'tiktok.com']
        return not any(domain in str(url).lower() for domain in social_domains)

    def extract_emails(self, text, html=""):
        emails = set()
        for pattern in self.email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                email = match if isinstance(match, str) else match[0] if match else ''
                emails.add(email.strip().lower())
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                if link.get('href', '').startswith('mailto:'):
                    emails.add(link['href'][7:].split('?')[0].strip().lower())
        
        valid_emails = []
        invalid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
        fake_email_patterns = [
            'nombre@ejemplo.com',
            'email@ejemplo.com', 
            'correo@ejemplo.com',
            'user@example.com',
            'admin@example.com',
            'info@example.com',
            'contact@example.com',
            'test@test.com',
            'ejemplo@ejemplo.com',
            'sample@sample.com'
        ]
        
        for email in emails:
            if '@' in email and '.' in email.split('@')[1] and not any(email.lower().endswith(ext) for ext in invalid_extensions):
                # Filtrar emails falsos/de prueba
                if not any(fake_pattern in email.lower() for fake_pattern in fake_email_patterns):
                    # Filtrar dominios de ejemplo comunes
                    if not any(domain in email.lower() for domain in ['ejemplo.com', 'example.com', 'test.com', 'sample.com']):
                        valid_emails.append(email)
        return valid_emails

    def extract_social_media(self, soup, base_url):
        social_links = {}
        for a in soup.find_all('a', href=True):
            href = a.get('href', '').lower()
            if not href: continue
            for name, pattern in self.social_media_patterns.items():
                if pattern in href:
                    full_url = urljoin(base_url, a.get('href'))
                    if name not in social_links:
                        social_links[name] = full_url
                    break
        return [f"{name}:{url}" for name, url in social_links.items()]
    
    def find_contact_pages(self, soup, base_url):
        contact_urls = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            link_text = link.get_text().lower().strip()
            if any(kw in link_text or kw in href.lower() for kw in self.contact_keywords):
                full_url = urljoin(base_url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    contact_urls.add(full_url)
        return list(contact_urls)

    def scrape_single_website(self, url, name):
        try:
            if not url or pd.isna(url): return {'emails': [], 'social_media': []}
            
            url = str(url).strip()
            if not url.startswith(('http://', 'https://')): url = 'https://' + url
            
            self.session.headers.update(self.get_random_headers())
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            emails = self.extract_emails(html_content)
            social_media = self.extract_social_media(soup, url)
            
            contact_urls = self.find_contact_pages(soup, url)
            for contact_url in contact_urls[:2]:
                time.sleep(random.uniform(1, 2))
                contact_response = self.session.get(contact_url, timeout=10)
                contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                emails.extend(self.extract_emails(contact_response.text))
                social_media.extend(self.extract_social_media(contact_soup, contact_url))
            
            emails = list(set(emails))
            social_media = list(set(social_media))
            
            if emails or social_media:
                logger.info(f"✅ {name}: {len(emails)} emails, {len(social_media)} redes.")
            
            return {'emails': emails, 'social_media': social_media}
            
        except Exception as e:
            logger.error(f"❌ {name}: Error - {e}")
            return {'emails': [], 'social_media': []}

    def run_scraping_process(self, input_filename="places_output.csv"):
        logger.info("--- INICIANDO PROCESO DE WEB SCRAPING ---")
        try:
            df = pd.read_csv(input_filename)
        except FileNotFoundError:
            logger.error(f"El archivo de entrada '{input_filename}' no fue encontrado. Abortando.")
            return None

        return self.run_scraping_process_from_dataframe(df)

    def run_scraping_process_from_dataframe(self, df, progress_callback=None):
        """Procesa web scraping directamente desde un DataFrame"""
        logger.info("--- INICIANDO PROCESO DE WEB SCRAPING ---")
        
        if df is None or df.empty:
            logger.error("DataFrame vacío o nulo. Abortando.")
            return None

        # Determinar qué columnas están disponibles (flexibilidad entre formatos)
        website_col = 'websiteUri' if 'websiteUri' in df.columns else 'website'
        name_col = 'displayName.text' if 'displayName.text' in df.columns else 'name'
        
        if website_col not in df.columns:
            logger.error(f"No se encontró columna de sitio web (buscando: {website_col})")
            return df
        
        real_websites = df[df[website_col].apply(self.is_real_website)].copy()
        total_sites = len(real_websites)
        logger.info(f"Se encontraron {total_sites} sitios web reales para scrapear.")

        df['scraped_emails'] = ''
        df['social_media_links'] = ''

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_idx = {executor.submit(self.scrape_single_website, row[website_col], row[name_col]): idx for idx, row in real_websites.iterrows()}
            
            processed_count = 0
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    result = future.result()
                    df.at[idx, 'scraped_emails'] = '; '.join(result['emails'])
                    df.at[idx, 'social_media_links'] = '; '.join(result['social_media'])
                except Exception as e:
                    logger.error(f"Error procesando el futuro para el índice {idx}: {e}")
                
                processed_count += 1
                if progress_callback:
                    # Notificar progreso al orquestador
                    progress_callback(processed_count, total_sites, df.loc[idx, website_col])
        
        logger.info("🎯 Proceso de scraping finalizado.")
        return df

def save_to_csv(df, filename="scraped_output.csv"):
    if df is None:
        logger.warning("No hay DataFrame para guardar.")
        return
    df.to_csv(filename, index=False)
    logger.info(f"💾 Datos scrapeados guardados en: {filename}")

def main():
    """
    Función principal para ejecutar este módulo de forma independiente.
    """
    scraper = WebsiteScraper()
    enriched_df = scraper.run_scraping_process()
    save_to_csv(enriched_df)

if __name__ == "__main__":
    main() 