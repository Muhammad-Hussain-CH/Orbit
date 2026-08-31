from fastapi import FastAPI
from app.api.routes import auth, projects
from app.api.routes import auth
from app.api.routes import auth, projects, tasks
from app.api.routes import auth, projects, tasks, admin


app = FastAPI(title="Orbit API")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "orbit"}