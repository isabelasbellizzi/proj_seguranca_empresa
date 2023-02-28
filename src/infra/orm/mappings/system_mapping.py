from sqlalchemy import Table, Column, Integer, VARCHAR, BigInteger
from sqlalchemy.dialects.postgresql import UUID as pg_uuid
from src.domain.entities.system import System

def system_mapping(mapper) -> None:
    schema = Table(
        'tb_system',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('token_id', pg_uuid(as_uuid=True), nullable=False),
        Column('name', VARCHAR(100), nullable=False),
        Column('status', Integer, nullable=False)
    )

    mapper.map_imperatively(System, schema,
                            properties={
                                "system_id": schema.c.id,
                                "system_name": schema.c.name
                            }
                            )
