from typing import List, Optional
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


from src.infra.repositories.implementations.features_repository import FeatureRepository
from src.infra.repositories.implementations.function_repository import FunctionRepository
from src.infra.repositories.implementations.paper_repository import PaperRepository
from src.services.DTOs.feature import (CreateFeatureRequestServiceDto,
                               FeatureResponseServiceDto,
                               UpdateFeatureRequestServiceDto,
                               ListFeatureServiceRequestDTO)
from src.services.exceptions import ServiceLayerNotFoundError, ServiceLayerDuplicatedNameError, ServiceLayerDuplicatedObjectError
from src.services.implementations.feature import (DeleteFeatureService,
                                                  GetFeatureService,
                                                  InsertFeatureService,
                                                  ListFeatureService,
                                                  UpdateFeatureService)
from src.web_app.controllers.base_controller import BaseRoute
from src.web_app.DTOs import MessageResponseDTO
from src.web_app.controllers.models import FeatureCreateRequest, FeatureUpdateRequest

feature_route = APIRouter()
feature_router = InferringRouter()


@cbv(feature_router)
class FeatureRoute(BaseRoute):

    def create_feature_repository(self):
        return FeatureRepository(self.db_handler)

    def create_paper_repository(self):
        return PaperRepository(self.db_handler)

    def create_function_repository(self):
        return FunctionRepository(self.db_handler)

    def create_feature_dto(self, paper_id: int, function_id: int, create: bool, read: bool, update: bool, delete: bool) -> CreateFeatureRequestServiceDto:
        return CreateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete, paper_id=paper_id, function_id=function_id)

    def update_feature_dto(self, create: bool, read: bool, update: bool, delete: bool) -> UpdateFeatureRequestServiceDto:
        return UpdateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete)


    ###CREATE###


    @feature_router.post('/', status_code=status.HTTP_201_CREATED, response_model=FeatureResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def insert(self, data: FeatureCreateRequest = Body()):
        new_feature_dto = self.create_feature_dto(paper_id=data.paper_id, function_id=data.function_id, create=data.create, read=data.read, update=data.update, delete=data.delete)

        try:
            new_feature = InsertFeatureService.execute(db=self.db_handler,
                                                       repo=self.create_feature_repository(),
                                                       function_repo=self.create_function_repository(),
                                                       paper_repo=self.create_paper_repository(),
                                                       data=new_feature_dto)
        except ServiceLayerDuplicatedObjectError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return new_feature


    ###READ###


    @feature_router.get('/{feature_id}', status_code=status.HTTP_200_OK, response_model=FeatureResponseServiceDto, responses={400: {"model": MessageResponseDTO}, 404: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_by_feature_id(self, feature_id: int):
        try:
            feature = GetFeatureService.execute(repo=self.create_feature_repository(), id=feature_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return feature


    @feature_router.get('/', status_code=status.HTTP_200_OK, response_model=List[FeatureResponseServiceDto], responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def get_all(self, max_records=0, paper_id: Optional[int] = None, function_id: Optional[int] = None):
        if max_records != 0:
            max_records = int(max_records)
        if paper_id is not None:
            paper_id = int(paper_id)
        if function_id is not None:
            function_id = int(function_id)

        list_feature_request_dto = ListFeatureServiceRequestDTO(max_records=max_records, paper_id=paper_id, function_id=function_id)

        try:
            lista = ListFeatureService.execute(repo=self.create_feature_repository(), data=list_feature_request_dto)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return lista

    @feature_router.put('/{feature_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def update(self, feature_id: int, data: FeatureUpdateRequest = Body()):
        update_feature_dto = self.update_feature_dto(create=data.create, read=data.read, update=data.update, delete=data.delete)
        try:
            UpdateFeatureService.execute(
                db=self.db_handler,
                repo=self.create_feature_repository(),
                feature_id=feature_id,
                data=update_feature_dto
            )
        except ServiceLayerNotFoundError as error:
            return JSONResponse(
                content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return JSONResponse(
                content={'msg': str(error)},
                status_code=status.HTTP_400_BAD_REQUEST
            )


    ###DELETE###


    @feature_router.delete('/{feature_id}', status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": MessageResponseDTO}, 500: {"model": MessageResponseDTO}})
    def delete(self, feature_id: int):
        try:
            DeleteFeatureService.execute(
                db=self.db_handler,
                repo=self.create_feature_repository(),
                feature_id=feature_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return None


feature_route.include_router(feature_router)
