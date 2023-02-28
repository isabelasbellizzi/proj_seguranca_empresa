import logging
import os
from uuid import uuid4
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from src.web_app.start_webapp import config_cors, config_routes, config_orm
from src.web_app.models.health_check_response import HealthCheckResponse
from src.web_app.webapp_settings import WebappSettings

def config_app(app_: FastAPI) -> None:
    config_orm()
    config_cors(app_)
    config_routes(app_)


app = FastAPI()
logging.basicConfig(filename='exceptions.log', encoding='utf-8', level=logging.ERROR)
logger = logging.getLogger(__name__)
webapp_settings = WebappSettings()

load_dotenv()
is_dev_environment = os.environ.get('ENVIRONMENT', '') != 'PROD'

@app.get("/")
async def health_check():
    return {
        "name": webapp_settings.project_name,
        "version": webapp_settings.version,
        "environment": webapp_settings.environment
    }

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    id = uuid4()
    friendly_msg = f'System error... Try again later [msg id={id}]'
    logger.exception(f'{id} Database Exception: {str(exc)}')

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"msg": friendly_msg}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"msg": exc.detail}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    new_msg = []
    # Replace 'msg' with 'message' for each error
    for error in details:
        field_name = error["loc"][1]
        msg = f'{error["msg"]}. [Field={field_name}]'
        new_msg.append(
            {
                "msg": msg,
                #"complete": error["msg"] + f'[Type={error["type"]}] [loc={error["loc"]}]',
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"erros": new_msg}),
    )




if __name__ == "__main__":
    config_app(app)
    uvicorn.run(app, host="127.0.0.1", port=5000, debug=True)
