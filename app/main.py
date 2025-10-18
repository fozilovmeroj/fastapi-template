from contextlib import asynccontextmanager
from pathlib import Path

import i18n
from fastapi import FastAPI

from app.core.plugins.i18n import init_i18n
from app.core.utils.router import load_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_i18n()
    yield


app = FastAPI(lifespan=lifespan)

# Load router from app.api package
api_dir = Path(__file__).parent / "api"
load_routers(app, api_dir)
