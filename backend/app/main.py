from fastapi import FastAPI

app = FastAPI(title="JobPilot")


@app.get("/")
def root():
    return {
        "message": "JobPilot is running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
