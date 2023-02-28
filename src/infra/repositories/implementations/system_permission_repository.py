from typing import List
from src.domain.entities import System, Paper, UserPermission, User
from src.domain.enums import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import ISystemPermissionRepository

class SystemPermissionRepository(ISystemPermissionRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get_all(self, system_id: int) -> List[dict]:
        query = self.session.query(System, Paper, UserPermission, User)
        query = query.where(System.status != StatusEnum.LOGICALLYDELETED, System.system_id == system_id)
        query = query.where(Paper.status != StatusEnum.LOGICALLYDELETED, Paper.system_id == System.system_id)
        query = query.where(UserPermission.status != StatusEnum.LOGICALLYDELETED, UserPermission.paper_id == Paper.paper_id)
        query = query.where(User.status != StatusEnum.LOGICALLYDELETED, User.user_id == UserPermission.user_id)

        query = query.with_entities(User.user_id.label("user_id"),
                                    User.user_email.label("user_email"),
                                    Paper.paper_id.label("paper_id"),
                                    Paper.name.label("paper_name"))

        return query.all()
