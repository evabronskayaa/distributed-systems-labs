from fastapi import FastAPI
from endpoints.link import router as links_router

app = FastAPI()

app.include_router(links_router, tags=['links'])

@app.get("/")
async def root():
    return {"message": "Hello World"}