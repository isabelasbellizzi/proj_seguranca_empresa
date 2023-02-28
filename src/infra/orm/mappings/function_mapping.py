from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from src.domain.entities import Function, System


def function_mapping(mapper) -> None:
    schema = Table(
        'tb_function',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('system_id', ForeignKey("tb_system.id"), nullable=False),
        Column('name', VARCHAR(100), nullable=False),
        Column('function_type', Integer, nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(Function, schema,
                            properties={
                                "function_id": schema.c.id,
                                "system": relationship(System, lazy="joined", innerjoin=True)
                            }
                            )
