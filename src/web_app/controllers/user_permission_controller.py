from typing import List, Optional

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations import (PaperRepository,
                                                    UserPermissionRepository,
                                                    UserRepository)
from src.services.DTOs.user_permission import (
    CreateUserPermissionRequestServiceDto, UserPermissionResponseServiceDto,ListUserPermissionServiceRequestDTO)
from src.services.exceptions import ServiceLayerNotFoundError,ServiceLayerDuplicatedObjectError
from src.services.implementations.user_permission import (
    DeleteUserPermissionService, GetUserPermissionService,
    InsertUserPermissionService, ListUserPermissionService)
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs import MessageResponseDTO


user_permission_route = APIRouter()
user_permission_router = InferringRouter()


@cbv(user_permission_router)
class UserPermissionRoute(BaseRoute):
    def create_user_permission_repository(self):
        return UserPermissionRepository(self.db_handler)

    def create_user_repository(self):
        return UserRepository(self.db_handler)

    def create_paper_repository(self):
        return PaperRepository(self.db_handler)

    @user_permission_router.get('/{user_permission_id}', status_code=status.HTTP_200_OK, response_model=UserPermissionResponseServiceDto,
                                responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, user_permission_id: int):
        try:
            user_permission = GetUserPermissionService.execute(repo=self.create_user_permission_repository(), user_permission_id=user_permission_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return user_permission

    @user_permission_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserPermissionResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records: int = 0, user_id: Optional[int] = None, paper_id: Optional[int] = None):

        data = ListUserPermissionServiceRequestDTO(max_records=max_records, user_id=user_id, paper_id=paper_id)

        try:
            lista = ListUserPermissionService.execute(repo=self.create_user_permission_repository(), data=data)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista


    @user_permission_router.delete('/{user_permission_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, user_permission_id: int):
        try:
            DeleteUserPermissionService.execute(db=self.db_handler, repo=self.create_user_permission_repository(), user_permission_id=user_permission_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return None

    @user_permission_router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[UserPermissionResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, user_id: int = Body(), paper_id: List[int] = Body()):
        try:
            data = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=paper_id)

            new_user_permission = InsertUserPermissionService.execute(db=self.db_handler,
                                                                      repo=self.create_user_permission_repository(),
                                                                      paper_repo=self.create_paper_repository(),
                                                                      user_repo=self.create_user_repository(),
                                                                      data=data)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except ServiceLayerDuplicatedObjectError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_user_permission


user_permission_route.include_router(user_permission_router)
