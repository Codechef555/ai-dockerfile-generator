from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Python API Demo",
    description="A sample API for testing generated Dockerfiles.",
    version="1.0.0",
)

# Sample data for API testing.
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Keyboard", "price": 2500},
    {"id": 3, "name": "Mouse", "price": 1200},
    {"id": 4, "name": "Monitor", "price": 18000},
]

@app.get("/")
def home() -> dict:
    """Return a welcome message."""
    return {
        "message": "Python API is running!",
        "application": "Python API Demo",
        "version": "1.0.0",
        "docs": "/docs",
    }

@app.get("/health")
def health_check() -> dict:
    """Return the application health status."""
    return {"status": "healthy"}