import subprocess
from fastapi import FastAPI
from prisma import Client as PrismaClient
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from api import auth, friends, statuses, users
from db import prisma

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Routers from other modules
app.include_router(auth.router)
app.include_router(friends.router)
app.include_router(statuses.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
