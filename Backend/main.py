from fastapi import FastAPI
from auth_routes import auth_router
from session_routes import session_router
from fastapi_jwt_auth import AuthJWT
from schema import Settings
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),  # must match your Settings.SECRET_KEY
    https_only=False                     # set True in production w/ HTTPS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(session_router)
@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/hello')
async def hello():
    return {"hello":"world"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)