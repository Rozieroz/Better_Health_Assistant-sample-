from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from reactpy.backend.fastapi import configure
from dotenv import load_dotenv
import os

"""# directory of the current file (e.g., backend/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory of the current script's directory (e.g., health-ai-app/)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Add the parent directory to sys.path
sys.path.append(PROJECT_ROOT)"""


# Import internal modules
from backend.database import init_db
from . import auth, ai_model

# Import the ReactPy frontend component
from frontend.app import frontend_app

# Load environment variables
load_dotenv()

# ==========================================
# Create main FastAPI application
# ==========================================
app = FastAPI(
    title="Health AI Assistant",
    description="AI-powered healthcare companion with secure authentication",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Initialize database
init_db()

# ==========================================
# Middleware (CORS)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Include Routers (APIs)
# ==========================================
app.include_router(auth.router)
app.include_router(ai_model.router)

# ==========================================
# Backend API Routes
# ==========================================
@app.get("/api/")
async def root():
    return {"message": "Health AI Assistant API", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Health AI Backend",
        "version": "1.0.0"
    }

@app.get("/api/home")
async def home():
    return {
        "message": "Welcome to Health AI 👋", 
        "features": [
            "AI Health Assistant",
            "Secure Authentication", 
            "Conversation History",
            "Medical Context Awareness"
        ]
    }

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "error": str(exc)}
    )

# ==========================================
# Mount ReactPy Frontend (after routers!)
# ==========================================
configure(app, frontend_app)

# ==========================================
# Development Server
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )