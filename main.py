from fastapi import FastAPI
from api import news_report_router
app = FastAPI()
app.include_router(news_report_router)
