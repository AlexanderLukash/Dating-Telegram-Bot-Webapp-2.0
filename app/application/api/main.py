from fastapi import FastAPI


def create_app():
    app = FastAPI(
        title="Dating Telegram Bot API",
        description="API for creating, updating, and deleting dating profiles",
        version="1.0.0",
        docs_url="/api/docs",
        debug=True,
    )
    return app
