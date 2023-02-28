from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.infra.repositories.implementations import SystemPermissionRepository, SystemRepository
from src.services.implementations.system_permission import ListSystemPermissionService
from src.services.DTOs.system_permission import SystemPermissionResponseServiceDTO
from src.web_app.DTOs.message_response_dto import MessageResponseDTO
from src.web_app.controllers.base_controller import BaseRoute
from src.services.exceptions import ServiceLayerNotFoundError


system_permission_route = APIRouter()
system_permission_router = InferringRouter()


@cbv(system_permission_router)
class SystemPermissionRoute(BaseRoute):
    def create_system_permission_repository(self):
        return SystemPermissionRepository(self.db_handler)

    def create_system_repository(self):
        return SystemRepository(self.db_handler)

    @system_permission_router.get('/{system_id}', status_code=status.HTTP_200_OK, response_model=List[SystemPermissionResponseServiceDTO],
                                responses={400: {"model": MessageResponseDTO},500: {"model": MessageResponseDTO}})
    def get_all(self, system_id: int):
        try:
            system_permissions = ListSystemPermissionService.execute(repo=self.create_system_permission_repository(), system_repo=self.create_system_repository(), system_id=system_id)
        except ServiceLayerNotFoundError as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return JSONResponse(content={'msg': str(error)}, status_code=status.HTTP_400_BAD_REQUEST)

        return system_permissions

system_permission_route.include_router(system_permission_router)
