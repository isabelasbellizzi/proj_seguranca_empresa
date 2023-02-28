from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from src.domain.entities import Paper, User, UserPermission


def user_permission_mapping(mapper) -> None:
    schema = Table(
        'tb_user_permissions',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('user_id', ForeignKey('tb_user.id'), nullable=False),
        Column('paper_id', ForeignKey('tb_paper.id'), nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(UserPermission, schema,
                            properties={
                                'user_permission_id': schema.c.id,
                                'paper': relationship(Paper, lazy='joined', innerjoin=True),
                                'user': relationship(User, lazy='joined', innerjoin=True)
                            }
                            )
