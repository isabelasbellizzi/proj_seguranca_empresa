from sqlalchemy import Table, Column, Integer, VARCHAR, BigInteger
from sqlalchemy.dialects.postgresql import UUID as pg_uuid
from src.domain.entities import User

def user_mapping(mapper) -> None:
    schema = Table(
        'tb_user',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('user_email', VARCHAR(100), nullable=False),
        Column('azure_id', pg_uuid(as_uuid=True), nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(User, schema,
                            properties={
                                "user_id": schema.c.id
                            }
                            )
