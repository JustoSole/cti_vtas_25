#!/usr/bin/env python3
"""
🚀 API Health Checker - Verifica el estado de las APIs necesarias

Este script verifica que todas las APIs estén funcionando correctamente:
1. Google Places API
2. Google Sheets API

Ejecuta este script antes de usar la aplicación para detectar problemas.
"""

import requests
import json
import logging
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURACIÓN ---
# 1. Google Places API Key
GOOGLE_API_KEY = "AIzaSyDZ4RCI-w0MkxkdYbdFjiT1wkLh9H-BqCk"

# Test data
TEST_QUERY = "restaurant"
TEST_LOCATION = "Buenos Aires, Argentina"

# 2. Google Sheets Configuration
GOOGLE_SHEET_ID = "1KjQMeQQ_3EO0MtfrSO7waTHtiZdTb7futHIA4yk6Xf8"
GOOGLE_SHEETS_CREDENTIALS_FILE = "google_credentials_coti.json"

class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{TColors.HEADER}{TColors.BOLD}{'='*60}{TColors.ENDC}")
    print(f"{TColors.HEADER}{TColors.BOLD}{text.center(60)}{TColors.ENDC}")
    print(f"{TColors.HEADER}{TColors.BOLD}{'='*60}{TColors.ENDC}\n")

def test_google_places_api():
    print(f"{TColors.OKBLUE}▶️ Probando Google Places & Geocoding API...{TColors.ENDC}")
    if not GOOGLE_API_KEY or "TU_GOOGLE" in GOOGLE_API_KEY:
        print(f"  {TColors.WARNING}⚠️  SKIPPED: No se proporcionó una Google API Key.{TColors.ENDC}")
        return

    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={TEST_LOCATION}&key={GOOGLE_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                print(f"  {TColors.OKGREEN}✅ SUCCESS:{TColors.ENDC} La API de Google Places/Geocoding funciona correctamente.")
            else:
                error = data.get('error_message', 'Error desconocido.')
                print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} La API respondió con estado '{data['status']}'. Causa probable: {error}")
        elif response.status_code in [401, 403]:
            print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Error de autenticación ({response.status_code}). Verifica que tu API Key sea correcta y esté habilitada.")
        else:
            print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Error inesperado. Código de estado: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Error de conexión: {e}")

def test_google_sheets_api():
    print(f"{TColors.OKBLUE}▶️ Probando Google Sheets API...{TColors.ENDC}")
    if not GOOGLE_SHEET_ID or "TU_SPREADSHEET" in GOOGLE_SHEET_ID:
        print(f"  {TColors.WARNING}⚠️  SKIPPED: No se proporcionó un Spreadsheet ID.{TColors.ENDC}")
        return
        
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)
        
        # Realizar una llamada de solo lectura a una celda para verificar
        service.spreadsheets().values().get(
            spreadsheetId=GOOGLE_SHEET_ID,
            range="'Leads Data'!A1"
        ).execute()
        
        print(f"  {TColors.OKGREEN}✅ SUCCESS:{TColors.ENDC} La API de Google Sheets funciona y se puede acceder a la hoja.")
        
    except FileNotFoundError:
        print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} No se encontró el archivo de credenciales '{GOOGLE_SHEETS_CREDENTIALS_FILE}'.")
    except HttpError as e:
        if e.resp.status == 404:
            print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} No se encontró el Spreadsheet con ID '{GOOGLE_SHEET_ID}'. Verifica el ID.")
        elif e.resp.status == 403:
            print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Permiso denegado. Asegúrate de que:")
            print("     - La API de Google Sheets esté habilitada en tu proyecto de GCP.")
            print("     - La cuenta de servicio (el email en el .json) tenga permisos de 'Editor' en tu Google Sheet.")
        else:
            print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Error de API: {e}")
    except Exception as e:
        print(f"  {TColors.FAIL}❌ FAILED:{TColors.ENDC} Error inesperado: {e}")

if __name__ == "__main__":
    print_header("API HEALTH CHECKER")
    test_google_places_api()
    test_google_sheets_api()
    print_header("CHECK COMPLETO") 