from fastapi import FastAPI , Request
from fastapi.middleware.cors import CORSMiddleware
from router import usuarios

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados en las solicitudes
)

app.include_router(usuarios.router)