from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from src.domain.entities import System, User, Owner


def owner_mapping(mapper) -> None:
    schema = Table(
        'tb_owner',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('user_id', ForeignKey('tb_user.id'), nullable=False),
        Column('system_id', ForeignKey("tb_system.id"), nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(Owner, schema,
                            properties={
                                'owner_id': schema.c.id,
                                'system': relationship(System, lazy='joined', innerjoin=True),
                                'user': relationship(User, lazy='joined', innerjoin=True)
                            }
                            )
