import uvicorn
from fastapi import FastAPI
from .routes import router

server = FastAPI()
server.include_router(router)

if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8000)
