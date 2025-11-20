from fastapi import FastAPI

from source.api.routes import router

app = FastAPI()
app.include_router(router)
