from typing import List, Optional

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations import (SystemRepository,
                                                    OwnerRepository,
                                                    UserRepository)
from src.services.DTOs.owner import (
    CreateOwnerRequestServiceDto, OwnerResponseServiceDto, ListOwnerServiceRequestDTO)
from src.services.DTOs.system import SystemResponseServiceDto
from src.services.exceptions import ServiceLayerNotFoundError,ServiceLayerDuplicatedObjectError
from src.services.implementations.owner import (
    DeleteOwnerService, GetOwnerService,
    InsertOwnerService, ListOwnerService,
    GetSystemsOwnedService)
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs import MessageResponseDTO


owner_route = APIRouter()
owner_router = InferringRouter()


@cbv(owner_router)
class OwnerRoute(BaseRoute):
    def create_owner_repository(self):
        return OwnerRepository(self.db_handler)

    def create_user_repository(self):
        return UserRepository(self.db_handler)

    def create_system_repository(self):
        return SystemRepository(self.db_handler)
    
    
    ####CREATE###
    
    @owner_router.post('/', status_code=status.HTTP_201_CREATED, response_model=OwnerResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, user_id: int = Body(), system_id: int = Body()):
        try:
            data = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

            new_owner = InsertOwnerService.execute(db=self.db_handler, repo=self.create_owner_repository(), user_repo=self.create_user_repository(), system_repo=self.create_system_repository(), data=data)

        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except ServiceLayerDuplicatedObjectError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_owner
    
    ###READ###

    @owner_router.get('/{owner_id}', status_code=status.HTTP_200_OK, response_model=OwnerResponseServiceDto,
                                responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, owner_id: int):
        try:
            owner = GetOwnerService.execute(repo=self.create_owner_repository(), owner_id=owner_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return owner

    @owner_router.get('/', status_code=status.HTTP_200_OK, response_model=List[OwnerResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records: int = 0, system_id: Optional[int] = None, user_id: Optional[int] = None):

        data = ListOwnerServiceRequestDTO(max_records=max_records, system_id=system_id, user_id=user_id)

        try:
            owner_list = ListOwnerService.execute(repo=self.create_owner_repository(), data=data)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return owner_list
    
    
    @owner_router.get('/systems/{user_email}', status_code=status.HTTP_200_OK, response_model=List[SystemResponseServiceDto],
                                responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_systems_owned(self, user_email: str):
        try:
            system_list = GetSystemsOwnedService.execute(repo=self.create_owner_repository(), system_repo=self.create_system_repository(),user_repo=self.create_user_repository(), user_email=user_email)  # nao entendi por que está dando esse erro de tipo
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return system_list
    
    
    ###DELETE###

    @owner_router.delete('/{owner_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, owner_id: int):
        try:
            DeleteOwnerService.execute(db=self.db_handler, repo=self.create_owner_repository(), owner_id=owner_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return None

owner_route.include_router(owner_router)
