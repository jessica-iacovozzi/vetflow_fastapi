from pathlib import Path
from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_babel import Babel, BabelConfigs, BabelMiddleware, _
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
logger = setup_logging()

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent

# Supported languages configuration
SUPPORTED_LANGUAGES = ["en", "fr"]

def get_locale(request: Request) -> str:
    """
    Determine the best language based on the Accept-Language header
    or fall back to the default language.
    """
    if not request.headers.get("Accept-Language"):
        return "en"
    # Parse Accept-Language header and match against supported languages
    header = request.headers["Accept-Language"].split(",")[0].strip()
    if header[:2] in SUPPORTED_LANGUAGES:
        return header[:2]
    return "en"

configs = BabelConfigs(
    ROOT_DIR=str(BASE_DIR),
    BABEL_DEFAULT_LOCALE="en",
    BABEL_TRANSLATION_DIRECTORY="translations",
    BABEL_SUPPORTED_LOCALES=SUPPORTED_LANGUAGES,
    # Function to determine which language to use for each request
    BABEL_LOCALE_SELECTOR=get_locale
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(BabelMiddleware, babel_configs=configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') 
                 else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept-Language"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root(request: Request):
    """
    Root endpoint that demonstrates internationalization.
    The message will be translated based on the Accept-Language header.
    """
    return {
        "message": _("Welcome to Vet Flow API"),
        "current_language": get_locale(request)
    }

# CLI commands for managing translations
if __name__ == "__main__":
    babel = Babel(configs=configs)
    babel.run_cli()