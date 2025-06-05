from fastapi import FastAPI
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    yield

fastapi = FastAPI(lifespan=lifespan)
