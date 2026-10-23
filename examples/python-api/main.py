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

@app.get("/products")
def get_products() -> dict:
    """Return all available products."""
    return {
        "count": len(PRODUCTS),
        "products": PRODUCTS,
    }

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    """Return a product by its ID."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail=f"Product with ID {product_id} was not found.",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )