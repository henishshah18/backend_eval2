#main fastapi app

import re
from fastapi import FastAPI
import uvicorn

# from api.endpoints.v1 import router  # Importing the router

app = FastAPI(title="Financial Transactions API", version="1.0.0")
# app.include_router(router, prefix="/api/v1")  # Including the router with the specified prefix

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Transactions API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)