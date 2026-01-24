from fastapi import FastAPI

from auth_service.src.application.config import configure_cors, configure_routes


def create_application() -> FastAPI:
    application = FastAPI(title="Auth Service", version="1.0.0")
    configure_cors(application)
    configure_routes(application)
    return application


app = create_application()
