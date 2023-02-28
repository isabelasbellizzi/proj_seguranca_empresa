import json
from pydantic import BaseModel
from fastapi import APIRouter, status, Response

from src.web_app.utils.jwt_data import JWTData
from src.web_app.utils.jwt_handler import JWTHandler
from src.infra.adaptors.auth_handler.auth_handler import AuthHandler as SsoAdapter

class LoginRequest(BaseModel):
    email: str
    senha: str


class LoginResponse(BaseModel):
    token: str
    usuarioGuid: str
    primeiroAcesso: bool
    senhaExpirada: bool
    bloqueado: bool


login_route = APIRouter()


@login_route.put('', status_code=status.HTTP_201_CREATED, response_model=LoginResponse)
def login(login_request: LoginRequest):
    auth = login_request

    if not auth:
        return Response('Email/Senha não informados', status_code=status.HTTP_401_UNAUTHORIZED)

    if (not auth.email):
        return Response('Email required', status_code=status.HTTP_401_UNAUTHORIZED)
    email = auth.email

    if (not auth.senha):
        return Response('Password required', status_code=status.HTTP_401_UNAUTHORIZED)
    senha = auth.senha

    str_response = SsoAdapter.authenticate(chave=email, senha=senha)
    if not (str_response):
        return Response('Could not authenticate', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = json.loads(str_response)
    if (data.get("erros") is not None):
        primeiro_erro = data["erros"][0]["mensagem"]
        return Response(str(primeiro_erro), status_code=status.HTTP_400_BAD_REQUEST)

    jwt_data = JWTData(user_id=data["usuarioGuid"], email=email)
    access_token = JWTHandler.create_token(jwt_data=jwt_data)
    retorno = LoginResponse(token=access_token, usuarioGuid=data["usuarioGuid"], primeiroAcesso=data["primeiroAcesso"], senhaExpirada=data["senhaExpirada"], bloqueado=data["bloqueado"])
    return retorno


@login_route.get('/listaConfiguracao', status_code=status.HTTP_200_OK)
def lista_configuracao():
    response: Response = SsoAdapter.lista_configuracao()
    if (response.status_code != 200):
        return Response(response.text, response.status_code)

    return Response(response.text, status_code=status.HTTP_200_OK)
