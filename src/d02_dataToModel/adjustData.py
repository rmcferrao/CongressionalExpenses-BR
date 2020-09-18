import pandas as pd

from pathlib import Path
import sys

regiao_estado = {'S':  ['RS', 'SC', 'PR'],
                 'SE': ['SP', 'MG', 'RJ', 'ES'],
                 'CO': ['MS', 'GO', 'DF', 'MT'],
                 'NE': ['BA', 'SE', 'AL', 'PE', 'PB', 'RN', 'CE', 'PI', 'MA'],
                 'N' : ['TO', 'PA', 'AP', 'RO', 'AC', 'AM', 'RR']}

update_escolaridade =  {'pos-graduacao':  ['Doutorado Incompleto', 'Doutorado', 'Mestrado', 'Pós-Graduação'],
                        'superior': ['Mestrado Incompleto', 'Superior'],
                        'ensino-medio': ['Ensino Técnico', 'Secundário', 'Ensino Médio', 'Superior Incompleto'],
                        'fundamental2': ['Ensino Médio Incompleto', 'Secundário Incompleto', 'Ensino Fundamental'],
                        'fundamental1': ['Ensino Médio Incompleto', 'Primário Completo'],
                        'sem-escolaridade': ['Primário Incompleto']}

def content_to_key(estado_input, dictionary):
    for regiao, estado in dictionary.items():
        if estado_input in estado:
            return regiao
    return None

if __name__ == '__main__':
    sys.path.append('../..')
    DATA_FOLDER = Path.cwd().joinpath('data')

    read_data_path = Path.joinpath(DATA_FOLDER, 'despesas56_clean.pkl')
    df = pd.read_pickle(read_data_path)
    df_model = df.copy()

    #select year period
    df = df.loc()[(df.dataGasto > '2019-06') & (df.dataGasto <= '2020-06')]
    # Only show positive values
    df = df[df.valor > 0]
    # Rodrigo Maia was born at santiago (Exile) but family is from RJ
    df['ufNascimento'].loc()[df['id'] == 74693] = 'RJ'
    # Camilo Capiberibe was born at santiago  (Exile) but family is from AP
    df['ufNascimento'].loc()[df['id'] == 204352] = 'AP'
    # Remove people who didnts presented escolaride and situacao
    df = df[~df['escolaridade'].isnull()]

    #set to numeric
    df[["valor", "mes", "idade"]] = df[["valor", "mes", "idade"]].apply(pd.to_numeric)

    # change estados to regions
    df['regiaoPartido'] = df['ufPartido'].apply(content_to_key, dictionary=regiao_estado)
    df['regiaoNascimento'] = df['ufNascimento'].apply(content_to_key, dictionary=regiao_estado)

    # change esclaridade to more a broad description
    df['escolaridade'] = df['escolaridade'].apply(content_to_key, dictionary=update_escolaridade)
    features = ['nome', 'partido', 'sexo', 'escolaridade', 'tipoDocumento', 'valor', 'tipo', 'mes', 'idade']

    df = df[features].reset_index(drop=True)

    save_data_path = Path.joinpath(DATA_FOLDER, 'despesas56_model.pkl')
    df.to_pickle(save_data_path)