from fastapi import FastAPI

app = FastAPI(title="Transport Service API")

@app.get("/")
def read_root():
    return {"message": "Transport Service API is running"}
# API endpoint check