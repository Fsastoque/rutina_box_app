#!/usr/bin/env bash
set -eux

# Asegura que Playwright use una ruta local válida
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/src/.playwright-browsers

# Instala navegadores si no existen
if [ ! -d "$PLAYWRIGHT_BROWSERS_PATH" ]; then
  echo "Instalando navegadores de Playwright..."
  python -m playwright install chromium --with-deps
else
  echo "Navegadores ya instalados, continuando..."
fi

# Inicia el servidor FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 10000
