from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This microservice is for our library catalog."}
