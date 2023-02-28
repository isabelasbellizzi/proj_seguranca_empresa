from typing import List, Optional
from src.domain.entities import User
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get_by_email(self, user_email: str) -> Optional[User]:
        query = self.session.query(User).filter(User.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(User.user_email == user_email)
        return query.first()

    def get_by_user_id(self, user_id: int) -> Optional[User]:
        query = self.session.query(User).filter(User.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(User.user_id == user_id)
        return query.first()

    def get_all(self, max_records=0) -> List[User]:
        query = self.session.query(User).filter(User.status != StatusEnum.LOGICALLYDELETED)

        if max_records > 0:
            query = query.limit(max_records)

        return query.all()

    def add(self, new: User) -> None:
        new.validate()
        new.user_id = None # type: ignore
        new.status = StatusEnum.ACTIVE
        self.session.add(new)
        self.session.flush()

    def delete(self, user_id: int) -> None:
        obj = self.get_by_user_id(user_id=user_id)

        if not obj:
            raise Exception(f"User not found. [user_id={user_id}]")

        obj.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, obj: User) -> None:
        obj.validate()
        self.session.flush()
