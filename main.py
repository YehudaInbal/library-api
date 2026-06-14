import uvicorn
from database import setup_db
from fastapi import FastAPI

from logger import get_logger
from routes import book_routes, member_routes, report_routes


logger = get_logger(__name__)
app = FastAPI()


app.include_router(router=book_routes.router, prefix="/books", tags=["Books"])
app.include_router(router=member_routes.router, prefix="/members", tags=["Members"])
app.include_router(router=report_routes.router, prefix="/reports", tags=["Reports"])

def main():
    setup_db.setup()
    try:
        uvicorn.run("main:app", reload=True)
    except Exception as e:
        logger.critical(e)
        raise






if __name__ == '__main__':
    main()