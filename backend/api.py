from fastapi import FastAPI
import random
import uvicorn

app = FastAPI()

@app.get("/random-number")
def get_random_number():
    return {"number": random.randint(1, 100)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
