from fastapi import FastAPI
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schema import Settings
import uvicorn

app = FastAPI()

app.include_router(auth_router)
@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/hello')
async def hello():
    return {"hello":"world"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)