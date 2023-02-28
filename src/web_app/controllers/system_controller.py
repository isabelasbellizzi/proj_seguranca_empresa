from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from src.domain.enums.status_enum import StatusEnum

from src.infra.repositories.implementations import SystemRepository, FunctionRepository, PaperRepository, OwnerRepository
from src.services.DTOs.system import (CreateSystemRequestServiceDto,
                                      SystemResponseServiceDto,
                                      UpdateSystemRequestServiceDto,
                                      ListSystemServiceRequestDTO)
from src.services.exceptions import \
    ServiceLayerNotFoundError, ServiceLayerForeignKeyError, ServiceLayerDuplicatedNameError
from src.services.implementations.system import (DeleteSystemService,
                                                 GetSystemService,
                                                 InsertSystemService,
                                                 ListSystemService,
                                                 UpdateSystemService)
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs.message_response_dto import MessageResponseDTO

system_route = APIRouter()
system_router = InferringRouter()


@cbv(system_router)
class SystemRoute(BaseRoute):
    def create_system_repository(self):
        return SystemRepository(self.db_handler)

    def create_paper_repository(self):
        return PaperRepository(self.db_handler)

    def create_function_repository(self):
        return FunctionRepository(self.db_handler)

    def create_owner_repository(self):
        return OwnerRepository(self.db_handler)

    def create_system_dto(self, system_name, token_id) -> CreateSystemRequestServiceDto:
        return CreateSystemRequestServiceDto(system_name=system_name, token_id=token_id)

    @system_router.get('/{system_id}', status_code=status.HTTP_200_OK, response_model=SystemResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, system_id: int):
        try:
            system = GetSystemService.execute(
                repo=self.create_system_repository(),
                system_id=system_id
            )
        except ServiceLayerNotFoundError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return system


    @system_router.get('/', status_code=status.HTTP_200_OK, response_model=List[SystemResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records: int = 0, system_name: Optional[str] = None, system_status: Optional[StatusEnum] = None):
        if max_records != 0:
            max_records = int(max_records)

        list_system_request_dto = ListSystemServiceRequestDTO(max_records=max_records, system_name=system_name, system_status=system_status)

        try:
            lista = ListSystemService.execute(
            repo=self.create_system_repository(),
            data=list_system_request_dto
        )
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista


    @system_router.delete('/{system_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, system_id: int):  # pylint: disable = inconsistent-return-statements
        try:
            DeleteSystemService.execute(
                db=self.db_handler,
                repo=self.create_system_repository(),
                paper_repo=self.create_paper_repository(),
                owner_repo= self.create_owner_repository(),
                function_repo=self.create_function_repository(),
                system_id=system_id
            )
        except ServiceLayerForeignKeyError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except ServiceLayerNotFoundError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @system_router.put('/{system_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def update(self, system_id: int, token_id: UUID = Body(), system_name: str = Body()):  # pylint: disable = inconsistent-return-statements

        update_system_dto = UpdateSystemRequestServiceDto(
            token_id=token_id,
            system_name=system_name
        )

        try:
            UpdateSystemService.execute(
                repo=self.create_system_repository(),
                system_id=system_id,
                db=self.db_handler,
                data=update_system_dto
            )
        except ServiceLayerNotFoundError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_404_NOT_FOUND
            )
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )


    @system_router.post('/', status_code=status.HTTP_201_CREATED, response_model=SystemResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, system_name: str = Body(min_length=5), token_id: UUID = Body()):
        try:
            create_system_dto = self.create_system_dto(
                token_id=token_id,
                system_name=system_name
            )

            new_system = InsertSystemService.execute(
                repo=self.create_system_repository(),
                data=create_system_dto,
                db=self.db_handler
            )
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return new_system


system_route.include_router(system_router)
