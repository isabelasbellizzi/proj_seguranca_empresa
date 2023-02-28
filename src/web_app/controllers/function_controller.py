from typing import List, Optional
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations import (FunctionRepository,
                                                    SystemRepository,
                                                    FeatureRepository)
from src.services.DTOs.function import (CreateFunctionRequestServiceDto,
                                        FunctionResponseServiceDto,
                                        UpdateFunctionRequestServiceDto,
                                        ListFunctionServiceRequestDTO)
from src.services.exceptions import (ServiceLayerDuplicatedNameError,
                                     ServiceLayerNotFoundError,
                                     ServiceLayerForeignKeyError)
from src.services.implementations.function import (DeleteFunctionService,
                                                   GetFunctionService,
                                                   InsertFunctionService,
                                                   ListFunctionService,
                                                   UpdateFunctionService)
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs.message_response_dto import MessageResponseDTO
from src.web_app.controllers.models import FunctionCreateRequest

from src.domain.enums import FunctionTypeEnum


function_route = APIRouter()
function_router = InferringRouter()


@cbv(function_router)
class FunctionRoute(BaseRoute):
    def create_function_repository(self):
        return FunctionRepository(self.db_handler)

    def create_system_repository(self):
        return SystemRepository(self.db_handler)

    def create_feature_repository(self):
        return FeatureRepository(self.db_handler)

    @function_router.get('/{function_id}', status_code=status.HTTP_200_OK, response_model=FunctionResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, function_id: int):
        try:
            function = GetFunctionService.execute(repo=self.create_function_repository(), id=function_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return function

    @function_router.get('/', status_code=status.HTTP_200_OK, response_model=List[FunctionResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records: int = 0, system_id: Optional[int] = None, function_name: Optional[str] = None, function_type: Optional[FunctionTypeEnum] = None):

        data = ListFunctionServiceRequestDTO(max_records=max_records, system_id=system_id, function_name=function_name, function_type=function_type)

        try:
            lista = ListFunctionService.execute(repo=self.create_function_repository(), data=data)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista


    @function_router.delete('/{function_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, function_id: int):
        try:
            DeleteFunctionService.execute(db=self.db_handler, repo=self.create_function_repository(), feature_repo=self.create_feature_repository(), id=function_id)
        except ServiceLayerForeignKeyError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return None

    @function_router.post('/', status_code=status.HTTP_201_CREATED, response_model=FunctionResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, data: FunctionCreateRequest = Body()):
        try:
            create_function_dto = CreateFunctionRequestServiceDto(name=data.name, function_type=data.function_type, system_id=data.system_id)

            new_function = InsertFunctionService.execute(db=self.db_handler,
                                                         repo=self.create_function_repository(),
                                                         system_repo=self.create_system_repository(),
                                                         data=create_function_dto)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_function

    @function_router.put('/{function_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def update(self, function_id: int, function_name: str = Body(min_length=10), function_type: FunctionTypeEnum = Body()):
        update_function_dto = UpdateFunctionRequestServiceDto(name=function_name, function_type=function_type)

        try:
            UpdateFunctionService.execute(db=self.db_handler, repo=self.create_function_repository(), id=function_id, data=update_function_dto)
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return None


function_route.include_router(function_router)
