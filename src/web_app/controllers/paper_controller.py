from typing import List
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations import (PaperRepository,
                                                    SystemRepository,
                                                    UserPermissionRepository,
                                                    FeatureRepository)
from src.services.DTOs.paper import UpdatePaperRequestServiceDto,CreatePaperRequestServiceDto

from src.services.exceptions import \
    ServiceLayerDuplicatedNameError,ServiceLayerNotFoundError,ServiceLayerForeignKeyError
from src.services.implementations.paper import (DeletePaperService,
                                                GetPaperService,
                                                InsertPaperService,
                                                ListPaperService,
                                                UpdatePaperService)
from src.web_app.controllers.base_controller import BaseRoute
from src.services.DTOs.paper.paper_response_service_dto import PaperResponseServiceDto
from src.web_app.DTOs.message_response_dto import MessageResponseDTO
from src.services.DTOs.paper.list_paper_service_request_dto import \
    ListPaperServiceRequestDTO

paper_route = APIRouter()
paper_router = InferringRouter()


@cbv(paper_router)
class PaperRoute(BaseRoute):
    def create_paper_repository(self):
        return PaperRepository(self.db_handler)

    def create_system_repository(self):
        return SystemRepository(self.db_handler)

    def create_user_permission_repository(self):
        return UserPermissionRepository(self.db_handler)

    def create_feature_repository(self):
        return FeatureRepository(self.db_handler)

    def create_paper_dto(self, paper_name, system_id) -> CreatePaperRequestServiceDto:
        return CreatePaperRequestServiceDto(name=paper_name, system_id=system_id)

    @paper_router.get("/{paper_id}", status_code=status.HTTP_200_OK, response_model=PaperResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get(self, paper_id: int):
        try:
            paper = GetPaperService.execute(repo=self.create_paper_repository(), paper_id=paper_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return paper

    @paper_router.delete('/{paper_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, paper_id: int):
        try:
            DeletePaperService.execute(db=self.db_handler,
                                       repo=self.create_paper_repository(),
                                       user_per_repo=self.create_user_permission_repository(),
                                       feature_repo=self.create_feature_repository(),
                                       paper_id=paper_id)
        except ServiceLayerForeignKeyError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

    @paper_router.get('/', status_code=status.HTTP_200_OK, response_model=List[PaperResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records=0, system_id=None, paper_name=None, paper_status=None):
        if max_records != 0:
            max_records = int(max_records)
        if paper_status is not None:
            paper_status = int(paper_status)

        data = ListPaperServiceRequestDTO(max_records=max_records, system_id=system_id, paper_name=paper_name, paper_status=paper_status)

        try:
            lista = ListPaperService.execute(repo=self.create_paper_repository(), data=data)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista

    @paper_router.put('/{paper_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def update(self, paper_id: int, paper_name: str = Body(embed=True)):
        update_paper_dto = UpdatePaperRequestServiceDto(name=paper_name)

        try:
            UpdatePaperService.execute(
                db=self.db_handler,
                repo=self.create_paper_repository(),
                paper_id=paper_id,
                data=update_paper_dto
            )

        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return


    @paper_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PaperResponseServiceDto, responses={400: {"model": MessageResponseDTO}})
    def insert(self, system_id: int = Body(), paper_name: str = Body(min_length=5)):
        try:
            create_paper_dto = self.create_paper_dto(paper_name=paper_name, system_id=system_id)

            new_paper = InsertPaperService.execute(db=self.db_handler,
                                                   repo=self.create_paper_repository(),
                                                   system_repo=self.create_system_repository(),
                                                   data=create_paper_dto)
        except ServiceLayerDuplicatedNameError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_paper


paper_route.include_router(paper_router)
