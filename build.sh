#!/usr/bin/env bash
set -eux  # Detiene si hay errores y muestra logs

# Actualiza e instala dependencias del sistema necesarias para Chromium
apt-get update && apt-get install -y \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 \
  libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
  libpango-1.0-0 libcairo2

# Instala las dependencias Python
pip install -r requirements.txt

# Instala Chromium (navegador para Playwright)
#python -m playwright install chromium
python -m playwright install chromium
