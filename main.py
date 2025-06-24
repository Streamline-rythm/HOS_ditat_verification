import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv

#load environment values
load_dotenv()

basic_url = os.getenv("basic_url")
if not basic_url:
    raise ValueError("API request url is not found")

app = FastAPI(
    title="driver loading ditat verification",
    description="this API will retrieve the substatus of driver on now",
    version="1.0.0",
)

@app.get("/test")
async def test():
    return {
        "result": "okay"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, proxy_headers=True,)
