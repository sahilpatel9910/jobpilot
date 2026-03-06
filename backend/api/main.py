from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="JobPilot API",
    description="Automated job discovery and tracking API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "JobPilot API is running 🚀"}

# Routers will be added here as we build each phase
# from backend.api.routes import jobs, scraper, matcher
