#%%
import pandas as pd
import numpy as np

from pathlib import Path
import sys
sys.path.append('../..')

DATA_FOLDER = Path.cwd().joinpath('data')
read_data_path = Path.joinpath(DATA_FOLDER, 'despesas56.pkl')
df = pd.read_pickle(read_data_path)

#%%
mapped_remaining_info = df["ultimoStatus"].apply(lambda x: (x['siglaPartido'], 
                                                            x['siglaUf'],
                                                            x["condicaoEleitoral"], 
                                                            x['situacao'], 
                                                            x['descricaoStatus'], 
                                                            x['nomeEleitoral'])).values


mapped_remaining_info_stacked = np.vstack(mapped_remaining_info)

df["partido"], df['ufPartido'], df["condicao"], df["situacao"], df["status"], df["nomeEleitoral"] = np.hsplit(mapped_remaining_info_stacked, 6)

features = ['id', 
            'nomeEleitoral', 
            'partido', 
            'ufPartido',
            'sexo', 
            'dataNascimento', 
            'ufNascimento', 
            'municipioNascimento', 
            'escolaridade', 
            'codDocumento',
            'numDocumento',
            'valorDocumento',
            'valorLiquido',
            'valorGlosa',
            'tipoDespesa', 
            'nomeFornecedor', 
            'dataDocumento',
            'mes',
            'parcela', 
            'condicao', 
            'situacao', 
            'status']

df_clean = df[features].copy()

df_clean.rename({'nomeEleitoral':'nome',
                'dataNascimento': 'nascimento',
                'municipioNascimento': 'munNascimento',
                'valorDocumento': 'valor',
                'tipoDespesa': 'tipo',
                'nomeFornecedor': 'fornecedor',
                'dataDocumento': 'dataGasto',
                }, 
                axis=1, inplace=True)

df_clean['nascimento'] = pd.to_datetime(df_clean['nascimento'], format='%Y-%m-%d')
df_clean['dataGasto'] = pd.to_datetime(df_clean['dataGasto'], format='%Y-%m-%d')
df_clean['idade'] = 2020 - df_clean['nascimento'].dt.year

save_data_path = Path.joinpath(DATA_FOLDER, 'despesas56_clean.pkl')
df_clean.to_pickle(save_data_path)

# %%
