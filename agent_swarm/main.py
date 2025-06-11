from fastapi import FastAPI
import os
from agent_swarm.api.chat import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    yield

fastapi = FastAPI(lifespan=lifespan)
fastapi.include_router(router)