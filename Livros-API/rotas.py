import json as js
import requests as r
from urllib.parse import urlencode

class API:

    def __init__(self):
        self.key = "AIzaSyCugkTxksVat-eQawRKcpO6CHWqY-yYeyc"

    def get_requisicao(self, url_base, dict_params):
        q = dict_params.pop("q", "")
        terms = dict_params.pop("terms", "")
        terms_value = dict_params.pop("terms_value", "")

        if terms and not terms_value :
           raise ValueError("erro: o termo foi seleconado sem um valor dado a ele")
        elif q:
            q_novo_valor = f"q={q}"
        elif not terms and not q :
            q_novo_valor = "q=Search"
        elif not q and terms:
            q_novo_valor = f"q={terms}:{terms_value}"
        else:
            q_novo_valor = f"q={q}+{terms}:{terms_value}"      

        url_api = lambda x : f"{url_base}{q_novo_valor}&{urlencode(dict_params)}&key={self.key}" if len(x) > 0 else f"{url_base}{q_novo_valor}&key={self.key}"

        url_final = url_api(dict_params)
        
        return r.get(url_final).json().get("items")

    def doc(self):
        with open("D:/Projetos python/Agente IA Livros/Livros_site/backend/doc.json", "r") as dados_json:
            doc_file = js.load(dados_json)
        return doc_file




