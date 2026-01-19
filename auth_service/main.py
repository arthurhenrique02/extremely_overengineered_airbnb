from fastapi import FastAPI

app = FastAPI()


@app.get("/health/live")
async def health_check():
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness_check():
    return {"status": "ready"}


@app.get("/health/startup")
async def startup_check():
    return {"status": "startup"}
