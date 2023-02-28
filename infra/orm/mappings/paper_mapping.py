from sqlalchemy import ForeignKey, Table, Column, BigInteger, Integer, VARCHAR
from sqlalchemy.orm import relationship

from src.domain.entities import Paper, System

def paper_mapping(mapper) -> None:
    schema = Table(
        'tb_paper',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('name', VARCHAR(100), nullable=False),
        Column('system_id', ForeignKey("tb_system.id"), nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(Paper, schema,
                            properties={
                                "paper_id": schema.c.id,
                                "system": relationship(System, lazy="joined", innerjoin=True)
                            }
                            )
