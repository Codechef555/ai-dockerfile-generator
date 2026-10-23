from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Python API Demo",
    description="A sample API for testing generated Dockerfiles.",
    version="1.0.0",
)