from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from online_cinema.middlewares import LoggingMiddleware
from online_cinema.api import auth, profile, password_reset, tokens

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # змінити на whitelist для production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(password_reset.router)
app.include_router(tokens.router)
