from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Table, Boolean
from sqlalchemy.orm import relationship
from src.domain.entities import Feature,Paper,Function


def feature_mapping(mapper) -> None:
    schema = Table(
        'tb_features',
        mapper.metadata,
        Column('id', BigInteger, nullable=False, primary_key=True),
        Column('paper_id', ForeignKey("tb_paper.id"), nullable=False),
        Column('function_id', ForeignKey("tb_function.id"), nullable=False),
        Column('allow_get', Boolean, nullable=False),
        Column('allow_insert', Boolean, nullable=False),
        Column('allow_update', Boolean, nullable=False),
        Column('allow_delete', Boolean, nullable=False),
        Column('status', Integer, nullable=False)
    )
    mapper.map_imperatively(Feature, schema,
                            properties={
                                "feature_id": schema.c.id,
                                "read": schema.c.allow_get,
                                "create": schema.c.allow_insert,
                                "update": schema.c.allow_update,
                                "delete": schema.c.allow_delete,
                                "paper": relationship(Paper, lazy="joined", innerjoin=True),
                                "function": relationship(Function, lazy="joined", innerjoin=True)
                            }
                            )
