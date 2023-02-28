from dataclasses import dataclass
import os

@dataclass
class WebappSettings():
    project_name = 'Seguranca'
    environment = 'Homolog'
    version = '1.04'
    debug = True

    def __init__(self):
        debug = os.environ.get('FASTAPI_DEBUG', "")
        self.debug = (debug.upper() == 'true')

    @property
    def title(self) -> str:
        if (self.environment):
            return f'{self.project_name} ({self.environment})'

        return self.project_name
