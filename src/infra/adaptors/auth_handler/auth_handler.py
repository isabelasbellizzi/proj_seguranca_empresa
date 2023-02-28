from dataclasses import dataclass
import os
from typing import Any
import requests
from src.infra.adaptors.auth_handler.iauth_handler import IAuthHandler

@dataclass
class AuthHandler (IAuthHandler):
    @staticmethod
    def lista_configuracao() -> Any:
        sso_url = os.environ.get('SSO_SERVICE_URL', "")
        sso_token = os.environ.get('SSO_TOKEN_ID', "")

        url = sso_url + f"login/listaConfiguracao?tokenSistema={sso_token}"
        return requests.get(url, verify=False, timeout=3)

    @staticmethod
    def authenticate(chave: str, senha: str):
        sso_url = os.environ.get('SSO_SERVICE_URL', "")
        sso_token = os.environ.get('SSO_TOKEN_ID', "")

        url = sso_url + "login/autentica"
        params = {'tokenSistema': sso_token, 'chave': chave, 'senha': senha, 'comPermissoes': False}
        headers = {'content-type': 'application/json'}
        req = requests.put(url, json=params, headers=headers, verify=False, timeout=30)
        if req.status_code == 404:
            return '{"erros":[{"chave":"000.1000","mensagem":"Url do sso não encontrada"}]}'

        return req.text
