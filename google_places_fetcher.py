#!/usr/bin/env python3
"""
Google Places Fetcher - Búsqueda por Grillas Geográficas

Responsabilidad:
  Realizar búsquedas exhaustivas en la Google Places API Web Service
  superando las limitaciones de paginación mediante subdivisión lógica.
"""

import os
import math
import time
import logging
import requests
import pandas as pd
from typing import List, Dict, Optional, Set, Tuple
from dotenv import load_dotenv

# --- Configuración de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- Carga de variables de entorno ---
load_dotenv()

class GooglePlacesFetcher:
    TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    DETAILS_URL     = "https://maps.googleapis.com/maps/api/place/details/json"

    def __init__(self, api_key: str, delay: float = 1.0, progress_callback=None):
        if not api_key:
            raise ValueError("La clave de API de Google Places no está configurada.")
        self.api_key = api_key
        self.delay_between_requests = delay
        self._seen_place_ids: Set[str] = set()
        self.progress_callback = progress_callback

    def get_location_bounds(self, location_query: str) -> Optional[Dict]:
        logger.info(f"📍 Geocoding para '{location_query}'...")
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {'address': location_query, 'key': self.api_key}
        try:
            resp = requests.get(geocode_url, params=params)
            resp.raise_for_status()
            data = resp.json()
            if data.get('status') == 'OK':
                geom = data['results'][0]['geometry']
                sw = geom['viewport']['southwest']
                ne = geom['viewport']['northeast']
                loc = geom['location']
                bounds = {
                    'low': {'latitude': sw['lat'], 'longitude': sw['lng']},
                    'high': {'latitude': ne['lat'], 'longitude': ne['lng']},
                    'center': {'latitude': loc['lat'], 'longitude': loc['lng']}
                }
                logger.info(f"✅ Bounds obtenidos: centro=({loc['lat']:.4f},{loc['lng']:.4f})")
                return bounds
            else:
                logger.error(f"❌ Geocoding error: {data.get('status')} - {data.get('error_message')}")
                return None
        except requests.RequestException as e:
            logger.error(f"❌ Error red Geocoding: {e}")
            return None

    def calculate_grid_points(self, bounds: Dict, grid_size: int) -> List[Dict]:
        lat_min, lat_max = bounds['low']['latitude'], bounds['high']['latitude']
        lng_min, lng_max = bounds['low']['longitude'], bounds['high']['longitude']
        lat_step = (lat_max - lat_min) / (grid_size - 1)
        lng_step = (lng_max - lng_min) / (grid_size - 1)
        points = []
        for i in range(grid_size):
            for j in range(grid_size):
                points.append({
                    'latitude': lat_min + i * lat_step,
                    'longitude': lng_min + j * lng_step,
                    'grid_pos': f"{i+1}x{j+1}"
                })
        logger.info(f"🗺️ Grilla {grid_size}x{grid_size} -> {len(points)} puntos generados")
        return points

    def search_places_from_point(self,
                                 query: str,
                                 lat: float,
                                 lng: float,
                                 radius: int = 2000,
                                 max_unique: int = 60
                                ) -> Tuple[List[Dict], int, bool]:
        """
        Búsqueda Text Search con paginación completa desde un punto.
        Retorna:
          - Lista de resultados únicos
          - Conteo bruto de items revisados
          - Flag limit_reached: True si alcanzamos max_unique (hay más resultados)
        """
        unique_places = []
        raw_count = 0
        limit_reached = False
        next_token = None

        while True:
            params = {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': min(radius, 50000),
                'key': self.api_key,
                'pagetoken': next_token
            } if next_token else {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': min(radius, 50000),
                'key': self.api_key
            }
            if next_token:
                time.sleep(2)  # wait for token activation

            try:
                time.sleep(self.delay_between_requests)
                resp = requests.get(self.TEXT_SEARCH_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                status = data.get('status')
                if status not in ('OK', 'ZERO_RESULTS'):
                    logger.warning(f"⚠️ Text search status {status}")
                    break
                results = data.get('results', [])
                raw_count += len(results)

                for item in results:
                    pid = item.get('place_id')
                    if not pid or pid in self._seen_place_ids:
                        continue
                    
                    # Se elimina el filtro estricto por nombre para aceptar
                    # todos los resultados relevantes de la API
                    self._seen_place_ids.add(pid)
                    unique_places.append({'id': pid})

                    if len(unique_places) >= max_unique:
                        limit_reached = True
                        break
                if limit_reached:
                    break
                next_token = data.get('next_page_token')
                if not next_token:
                    break
            except requests.RequestException as e:
                logger.error(f"❌ Text Search error at ({lat:.4f},{lng:.4f}): {e}")
                break

        return unique_places, raw_count, limit_reached

    def get_place_details(self, place_id: str) -> Optional[Dict]:
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,international_phone_number,website,geometry,rating,user_ratings_total,types',
            'key': self.api_key
        }
        try:
            time.sleep(self.delay_between_requests * 0.5)
            resp = requests.get(self.DETAILS_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            if data.get('status') == 'OK':
                return data['result']
            else:
                logger.warning(f"⚠️ Details {data.get('status')} for {place_id}")
                return None
        except requests.RequestException as e:
            logger.error(f"❌ Details API error for {place_id}: {e}")
            return None

    def _calculate_point_bounds(self, point: Dict, radius: int) -> Dict:
        lat, lng = point['latitude'], point['longitude']
        dlat = radius / 111000
        dlng = radius / (111000 * abs(math.cos(math.radians(lat))))
        return {
            'low': {'latitude': lat - dlat, 'longitude': lng - dlng},
            'high': {'latitude': lat + dlat, 'longitude': lng + dlng},
            'center': {'latitude': lat, 'longitude': lng}
        }

    def _search_grid_recursive(self,
                               query: str,
                               bounds: Dict,
                               grid_size: int,
                               radius: int,
                               recursion: int,
                               max_recursion: int) -> List[Dict]:
        if recursion >= max_recursion:
            logger.info(f"🛑 Nivel máximo de recursión alcanzado ({recursion}) - retornando solo resultados locales")
            # Simple grid search sin más subdivisiones
            return self._search_grid_simple(query, bounds, grid_size, radius)

        logger.info(f"🔄 Recursión nivel {recursion}/{max_recursion}")
        points = self.calculate_grid_points(bounds, grid_size)
        total_points = len(points)
        found = []
        subs = []

        for idx, p in enumerate(points, start=1):
            if self.progress_callback:
                # Notificar progreso: punto actual, total de puntos, lugares encontrados hasta ahora
                self.progress_callback(idx, total_points, len(self._seen_place_ids))
            
            logger.info(f"🔍 Punto {idx}/{len(points)} {p['grid_pos']}...")
            places, count, limited = self.search_places_from_point(
                query, p['latitude'], p['longitude'], radius
            )
            found.extend(places)
            logger.info(f"   → {len(places)} únicos de {count} revisados")
            # Subdividir solo si alcanzamos límite real de resultados
            if limited:
                subs.append({'bounds': self._calculate_point_bounds(p, radius)})

        # Procesar subgrillas solo si detectamos limitaciones
        for sub in subs:
            logger.info(f"   ↪ Subgrilla por límite detectado")
            found.extend(self._search_grid_recursive(
                query,
                sub['bounds'],
                max(2, grid_size // 2),
                max(100, radius // 2),
                recursion + 1,
                max_recursion
            ))

        return found

    def _search_grid_simple(self, query: str, bounds: Dict, grid_size: int, radius: int) -> List[Dict]:
        logger.info("🔄 Búsqueda simple por grilla (sin subdivisión)")
        points = self.calculate_grid_points(bounds, grid_size)
        found = []
        total_points = len(points)
        for i, p in enumerate(points, start=1):
            if self.progress_callback:
                self.progress_callback(i, total_points, len(self._seen_place_ids))
                
            logger.info(f"🔍 Simple Punto {i}/{len(points)} {p['grid_pos']}...")
            places, _, _ = self.search_places_from_point(query, p['latitude'], p['longitude'], radius)
            found.extend(places)
        return found

    def search_places_grid(self,
                            query: str,
                            location_query: str,
                            grid_size: int = 6,
                            radius: int = 3000,
                            max_recursion: int = 2) -> List[Dict]:
        self._seen_place_ids.clear()
        bounds = self.get_location_bounds(location_query)
        if not bounds:
            return []
        
        raw = self._search_grid_recursive(query, bounds, grid_size, radius, 0, max_recursion)

        detailed = []
        logger.info("👷 Obteniendo detalles para cada lugar...")
        total_raw = len(raw)
        for i, p in enumerate(raw, start=1):
            if self.progress_callback:
                # Notificar progreso de la fase de obtención de detalles
                self.progress_callback(i, total_raw, len(detailed), phase="details")
                
            det = self.get_place_details(p['id'])
            if det:
                detailed.append({
                    'place_id': p['id'],
                    'name': det.get('name'),
                    'address': det.get('formatted_address'),
                    'phone': det.get('international_phone_number'),
                    'website': det.get('website'),
                    'latitude': det.get('geometry', {}).get('location', {}).get('lat'),
                    'longitude': det.get('geometry', {}).get('location', {}).get('lng'),
                    'rating': det.get('rating'),
                    'user_ratings_total': det.get('user_ratings_total'),
                    'types': det.get('types')
                })
        logger.info(f"🎉 Total final: {len(detailed)} lugares con detalles")
        return detailed

    def save_to_csv(self, places: List[Dict], filename: str = "places_results.csv"):
        if not places:
            logger.warning("⚠️ No hay datos para guardar.")
            return
        df = pd.DataFrame(places)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"✅ Resultados exportados a {filename}")

if __name__ == '__main__':
    key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not key:
        logger.error("❌ Define GOOGLE_PLACES_API_KEY en .env o en tu entorno.")
        exit(1)
    fetcher = GooglePlacesFetcher(key)
    results = fetcher.search_places_grid(
        query='cotillones',
        location_query='Recoleta, Buenos Aires, Argentina',
        grid_size=6,
        radius=3000,
        max_recursion=2
    )
    fetcher.save_to_csv(results)
