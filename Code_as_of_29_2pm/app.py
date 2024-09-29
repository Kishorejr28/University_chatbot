from fastapi import FastAPI
import uvicorn
from routes import router as chat_router

app = FastAPI()

app.include_router(chat_router,prefix="/chat_bot")

if __name__ =="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8080,reload=True)#,reload=True,loop="asyncio"
