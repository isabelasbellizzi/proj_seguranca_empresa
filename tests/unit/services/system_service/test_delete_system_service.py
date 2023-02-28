import pytest
from src.infra.repositories.implementations import SystemRepository, FunctionRepository, PaperRepository, OwnerRepository
from src.services.implementations.system.delete_system_service import DeleteSystemService
from src.services.DTOs.function import ListFunctionServiceRequestDTO
from src.services.DTOs.paper import ListPaperServiceRequestDTO
from src.services.DTOs.owner import ListOwnerServiceRequestDTO
from tests.unit.services.teste_service_base import TestServiceBase,DbHandlerFake


class TestDeleteSystem(TestServiceBase):

    def test_execute_has_owners_error(self, mocker):
        #Arrange
        system_id = 1234
        db = self.db_handler
        repo = SystemRepository(db)
        function_repo = FunctionRepository(db)
        paper_repo = PaperRepository(db)
        owner_repo = OwnerRepository(db)

        mocker.patch.object(OwnerRepository, 'get_all', return_value=[1])

        #Act
        with pytest.raises(Exception) as error:
            DeleteSystemService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, owner_repo=owner_repo, system_id=system_id)

        #Assert
        assert str(error.value) == f"System has owners. [system_id={system_id}]"
    
    def test_delete_has_functions_error(self, mocker):
        #Arrange
        system_id = 1234
        db = self.db_handler
        repo = SystemRepository(db)
        function_repo = FunctionRepository(db)
        paper_repo = PaperRepository(db)
        owner_repo = OwnerRepository(db)

        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(FunctionRepository, 'get_all', return_value=[1])

        #Act
        with pytest.raises(Exception) as error:
            DeleteSystemService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, owner_repo=owner_repo, system_id=system_id)

        #Assert
        assert str(error.value) == f"System has functions. [id={system_id}]"

    def test_delete_system_has_papers_error(self, mocker):
        #Arrange
        system_id = 1234
        db = self.db_handler
        repo = SystemRepository(db)
        function_repo = FunctionRepository(db)
        paper_repo = PaperRepository(db)
        owner_repo = OwnerRepository(db)

        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(FunctionRepository, 'get_all', return_value=[])
        mocker.patch.object(PaperRepository, 'get_all', return_value=[1])

        #Act
        with pytest.raises(Exception) as error:
            DeleteSystemService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, owner_repo=owner_repo, system_id=system_id)

        #Assert
        assert str(error.value) == f"System has papers. [id={system_id}]"

    def test_delete_system_not_found_error(self, mocker):
        #Arrange
        system_id = 1234
        db = self.db_handler
        repo = SystemRepository(db)
        function_repo = FunctionRepository(db)
        paper_repo = PaperRepository(db)
        owner_repo = OwnerRepository(db)

        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(FunctionRepository, 'get_all', return_value=[])
        mocker.patch.object(PaperRepository, 'get_all', return_value=[])
        mocker.patch.object(SystemRepository, 'get', return_value=None)

        #Act
        with pytest.raises(Exception) as error:
            DeleteSystemService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, owner_repo=owner_repo, system_id=system_id)

        #Assert
        assert str(error.value) == f"System not found. [id={system_id}]"

    def test_delete_system_execute_ok(self, mocker):
        #Arrange
        system_id = 1234
        db = self.db_handler
        repo = SystemRepository(db)
        function_repo = FunctionRepository(db)
        paper_repo = PaperRepository(db)
        list_function_request_dto = ListFunctionServiceRequestDTO(system_id=system_id)
        list_paper_request_dto = ListPaperServiceRequestDTO(system_id=system_id)
        list_owner_request_dto = ListOwnerServiceRequestDTO(system_id=system_id)
        owner_repo = OwnerRepository(db)

        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(FunctionRepository, 'get_all', return_value=[])
        mocker.patch.object(PaperRepository, 'get_all', return_value=[])
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(SystemRepository, 'delete', return_value=True)
        mocker.patch.object(DbHandlerFake, 'commit')

        #Act
        DeleteSystemService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, owner_repo=owner_repo, system_id=system_id)

        #Assert
        OwnerRepository.get_all.assert_called_once_with(data=list_owner_request_dto)
        FunctionRepository.get_all.assert_called_once_with(data=list_function_request_dto)
        PaperRepository.get_all.assert_called_once_with(data=list_paper_request_dto)
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        SystemRepository.delete.assert_called_once_with(system_id=system_id)
        DbHandlerFake.commit.assert_called_once()
