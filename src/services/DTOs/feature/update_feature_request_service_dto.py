from dataclasses import dataclass


@dataclass
class UpdateFeatureRequestServiceDto():
    create: bool
    read: bool
    update: bool
    delete: bool
