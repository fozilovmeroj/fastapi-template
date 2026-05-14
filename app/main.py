from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from fastapi.middleware.cors import CORSMiddleware

from app.core import config
from app.core.plugins.i18n import init_i18n
from app.core.utils.router import load_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_i18n()
    yield


app = FastAPIOffline(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
)

# Load router from app.api package
api_dir = Path(__file__).parent / "api"
load_routers(app, api_dir)
