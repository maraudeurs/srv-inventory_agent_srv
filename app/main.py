from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.models.database import SessionLocal, engine

from app.api.v1.routes import instance_route, auth_route, inventory_route
from app.models.database import init_db, purge_db

## Manage lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    ## at app start
    init_db(engine)
    yield
    ## at app shutdown
    # purge_db()

app = FastAPI(lifespan=lifespan)

## CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

## Include routers
app.include_router(instance_route.router, prefix="/v1", tags=["instances"])
app.include_router(inventory_route.router, prefix="/v1", tags=["inventory"])
app.include_router(auth_route.router, prefix="/v1", tags=["auth"])
