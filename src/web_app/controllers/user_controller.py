
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.DTOs.user import (CreateUserRequestServiceDto,
                                    UpdateUserRequestServiceDto,
                                    UserResponseServiceDto)
from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.user import DeleteUserService, InsertUserService, GetUserByEmailService, GetUserByIdService, ListUserService, UpdateUserService
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs.message_response_dto import MessageResponseDTO
from src.infra.repositories.implementations.user_permission_repository import UserPermissionRepository
from src.infra.repositories.implementations.owner_repository import OwnerRepository
from src.services.exceptions.service_layer_foreign_key_error import ServiceLayerForeignKeyError

user_route = APIRouter()
user_router = InferringRouter()


@cbv(user_router)
class UserRoute(BaseRoute):
    def create_user_repository(self):
        return UserRepository(self.db_handler)

    def create_user_permission_repository(self):
        return UserPermissionRepository(self.db_handler)
    
    def create_owner_repository(self):
        return OwnerRepository(self.db_handler)

    def create_user_dto(self, azure_id, user_email) -> CreateUserRequestServiceDto:
        return CreateUserRequestServiceDto(azure_id=azure_id, user_email=user_email)

    def update_user_dto(self, azure_id, user_email) -> UpdateUserRequestServiceDto:
        return UpdateUserRequestServiceDto(azure_id=azure_id, user_email=user_email)



    @user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, azure_id: UUID = Body(), user_email: str = Body()):
        try:
            create_user_dto = self.create_user_dto(azure_id=azure_id, user_email=user_email)

            new_user = InsertUserService.execute(db=self.db_handler, repo=self.create_user_repository(), data=create_user_dto)
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_user


###READ###


    @user_router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, user_id: int):
        try:
            user = GetUserByIdService.execute(repo=self.create_user_repository(), user_id=user_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return user

    @user_router.get('/email/{user_email}', status_code=status.HTTP_200_OK, response_model=UserResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_by_email(self, user_email: str):
        try:
            user = GetUserByEmailService.execute(repo=self.create_user_repository(), user_email=user_email)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return user

    @user_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records=0):
        if max_records != 0:
            max_records = int(max_records)
        try:
            lista = ListUserService.execute(repo=self.create_user_repository(), max_records=max_records)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista



###UPDATE###


    @user_router.put('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def update(self, user_id: int, azure_id: Optional[UUID] = Body(), user_email: Optional[str] = Body()):
        try:
            update_user_dto = self.update_user_dto(azure_id=azure_id, user_email=user_email)

            UpdateUserService.execute(db=self.db_handler, repo=self.create_user_repository(), user_id=user_id, data=update_user_dto)
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)


###DELETE###


    @user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, user_id: int):
        try:
            DeleteUserService.execute(db=self.db_handler, repo=self.create_user_repository(), up_repo=self.create_user_permission_repository(), owner_repo=self.create_owner_repository(), user_id=user_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except ServiceLayerForeignKeyError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)


user_route.include_router(user_router)
