from requests import get
import pandas as pd

import os
import sys
sys.path.append(os.path.realpath('..'))

# APi info https://dadosabertos.camara.leg.br/swagger/api.html

API_ROOT = 'https://dadosabertos.camara.leg.br/api/v2'

def page_json(dado, params = {}):
    if type(dado) == list:
        return get(os.path.join(API_ROOT, *dado), params=params).json()
    else:
        return get(os.path.join(API_ROOT, dado), params=params).json()

def deputado_info_pessoal(deputado_id):
    return page_json(['deputados', deputado_id])

def deputado_despesas(deputado_id, anos):

    pagina = 1
    deputados_info = []

    while True:
        params = {'itens':100, 'pagina': pagina, 'ano': anos}
        deputado_json = page_json(['deputados', deputado_id, 'despesas'], params)
        deputado_dados = deputado_json['dados']
        deputado_links = deputado_json['links']

        deputados_info.extend(deputado_dados)

        if not 'next' in [dp['rel'] for dp in deputado_links]:
            return deputados_info

        pagina += 1

if __name__ == '__main__':


    deputados_data =  page_json('deputados',{'itens':600,
                                            'dataInicio':'2019-01-01'
                                            })

    deputados_minimal_info = []
    for cell in deputados_data['dados']:
        deputado_info = deputado_info_pessoal(str(cell['id']))['dados']
        deputados_minimal_info.append(deputado_info)

    anos = (2019, 2020)
    deputados_info = []

    for deputado_minimal_info in deputados_minimal_info:
        deputado_id = str(deputado_minimal_info['id'])
        deputado_nome =  deputado_minimal_info['nomeCivil']

        print('{} - {}\n------------------'.format(deputado_id, deputado_nome))
        deputado_despesas_list = deputado_despesas(deputado_id, anos)

        for deputado_despesa in deputado_despesas_list:
            deputados_info.append({**deputado_minimal_info, **deputado_despesa})

    pd.DataFrame(deputados_info).to_pickle('data/despesas56.pkl')
