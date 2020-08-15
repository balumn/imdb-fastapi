from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/fruits/get")
async def get_fruits(apple:float,orange):
    print(apple,orange)
    return {apple,orange}