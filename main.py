from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.controller import router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bellogoperador.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 conecta os controllers
app.include_router(router)