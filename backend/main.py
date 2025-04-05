import os
import sys
from fastapi import FastAPI

# Add the parent directory to the system path (if needed for imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the router from routes.py
from backend.api.routes import router

# Initialize FastAPI app
app = FastAPI()

# Include the router (which contains all the endpoints)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
