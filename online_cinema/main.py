from fastapi import FastAPI

app = FastAPI(title="Online Cinema")

@app.get("/")
def read_root():
    return {"message": "Welcome to Online Cinema!"}
