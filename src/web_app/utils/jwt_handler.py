from dataclasses import dataclass
import os
from typing import Any
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from src.web_app.utils.jwt_data import JWTData

@dataclass
class JWTHandler:
    @staticmethod
    def create_token(jwt_data: JWTData) -> Any:
        secret = os.environ.get('JWT_SECRET_KEY', "")
        algorithm = os.environ.get('JWT_ALGORITHM', "")
        payload = {
            "data": jwt_data.__dict__,
            "expires": None
        }

        token = jwt.encode(payload, key=secret, algorithm=algorithm)

        return token

    @staticmethod
    def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> JWTData:
        secret = os.environ.get('JWT_SECRET_KEY', "")
        algorithm = os.environ.get('JWT_ALGORITHM', "")
        try:
            decoded_token = jwt.decode(auth.credentials, secret, algorithms=[algorithm])
            return JWTData(**decoded_token['data'])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
        except Exception as error:
            raise HTTPException(status_code=401, detail=f'Generating token: {str(error)}')
