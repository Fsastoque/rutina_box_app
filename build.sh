#!/usr/bin/env bash
# Instalar dependencias Python
pip install -r requirements.txt

# Instalar navegadores de Playwright
python -m playwright install chromium

# (Opcional) Si usas Firefox o WebKit, añade también:
# python -m playwright install firefox
# python -m playwright install webkit
