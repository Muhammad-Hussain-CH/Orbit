from fastapi import FastAPI

app = FastAPI(title="Orbit API")


@app.get("/health")
def health():
    return {"status": "ok", "service": "orbit"}