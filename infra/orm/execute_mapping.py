from sqlalchemy import MetaData
from sqlalchemy.orm import registry
from src.infra.orm.mappings import system_mapping, function_mapping, paper_mapping, user_mapping, user_permission_mapping, feature_mapping,owner_mapping


metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def execute_mapping():
    paper_mapping(mapper_registry)
    function_mapping(mapper_registry)
    system_mapping(mapper_registry)
    user_mapping(mapper_registry)
    user_permission_mapping(mapper_registry)
    feature_mapping(mapper_registry)
    owner_mapping(mapper_registry)
