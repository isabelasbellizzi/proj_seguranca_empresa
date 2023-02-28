from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infra.orm.execute_mapping import execute_mapping
from src.web_app.controllers import (function_route, login_route, paper_route,
                                     system_route, user_permission_route,
                                     user_route,feature_route, system_permission_route,
                                     owner_route)
from src.web_app.utils.jwt_handler import JWTHandler

def config_orm() -> None:
    execute_mapping()


def config_cors(app: FastAPI) -> None:
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def config_routes(app: FastAPI) -> None:
    app.include_router(login_route, prefix="/login", tags=["Login"])

    app.include_router(system_route, prefix="/systems", tags=['SYSTEMS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(function_route, prefix="/functions", tags=['FUNCTIONS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(user_route, prefix="/users", tags=['USERS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(paper_route, prefix="/papers", tags=['PAPERS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(feature_route, prefix="/features", tags=['FEATURES'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(user_permission_route, prefix="/user_permissions", tags=['USER_PERMISSIONS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(system_permission_route, prefix="/system_permissions", tags=['SYSTEM_PERMISSIONS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    app.include_router(owner_route, prefix="/owners", tags=['OWNERS'], dependencies=[Depends(JWTHandler().auth_wrapper)])
    