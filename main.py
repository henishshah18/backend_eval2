#main fastapi app

import re
from fastapi import FastAPI
import uvicorn
from api.endpoints.v1 import transaction, transfer, user, wallet  # Importing the router

# from api.endpoints.v1 import router  # Importing the router

app = FastAPI(title="Financial Transactions API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Transactions API"}

app.include_router(transaction.router)
app.include_router(transfer.router)
app.include_router(user.router)
app.include_router(wallet.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)