from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, projects, tasks, admin

app = FastAPI(title="Orbit API")

# Allow the React frontends (running on these ports) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # user app
        "http://localhost:5174",   # admin app
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "orbit"}