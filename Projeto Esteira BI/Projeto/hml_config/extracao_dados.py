# ==================================================================================================================
# Import de bibliotecas
import credenciais
import psycopg2
from psycopg2 import sql, extras
import pandas as pd
import gdown
import tempfile
import os

# ==================================================================================================================
# Extração diaria dos dados postgres
def extract_postgres_data(table_name):
    # URL de conexão ao PostgreSQL
    postgres_url = os.environ['DATABASE_URL'] # URL configurada no arquivo credenciais
    conn = psycopg2.connect(postgres_url)
    
    query = f"SELECT * FROM {table_name};"

    # Lendo query no dataframe
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ==================================================================================================================
# Extração diaria dos dados CSV via link web
def extract_csv_data_from_drive(drive_url):
    file_id = drive_url.split('/')[-2]
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

    # Caminho temporário adequado para o sistema operacional
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        output = temp_file.name

    # Download do arquivo
    gdown.download(download_url, output, quiet=False)

    # Lendo arquivo no dataframe
    df = pd.read_csv(output)
    return df


# ==================================================================================================================
# Tratamento dos dados dos Dataframe
def transform_data(df, date_column_names):
    df = df.drop_duplicates() # Remover duplicados

    df.fillna(0, inplace=True) # Substituir valores nulos por 0

    for date_column in date_column_names: # Transformar campos de datas
        df[date_column] = pd.to_datetime(df[date_column])
    
    return df


# ==================================================================================================================
# Função para carregar DataFrame no PostgreSQL Data warehouse
def load_data_to_postgres(df, table_name, unique_keys=None, column_key=None):
    # URL de conexão ao PostgreSQL
    postgres_url = os.environ['DATAWAREHOUSE_URL']
    conn = psycopg2.connect(postgres_url)
    
    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()

    try:
        # Prepara a consulta de inserção com upsert
        columns = list(df.columns)
        insert_query_base = sql.SQL("""
            INSERT INTO {table} ({fields})
            VALUES %s
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns))
        )

        # Verificar se tem chave unica para upsert
        if unique_keys:
            conflict_action = sql.SQL("""
                ON CONFLICT ({keys})
                DO UPDATE SET {updates}
            """).format(
                keys=sql.SQL(', ').join(map(sql.Identifier, unique_keys)),
                updates=sql.SQL(', ').join([
                    sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(col), sql.Identifier(col))
                    for col in columns
                    if col not in unique_keys
                ])
            )
            insert_query = insert_query_base + conflict_action
        else:
            insert_query = insert_query_base

        # Converte o DataFrame em uma lista de tuplas
        data = [tuple(row) for row in df.itertuples(index=False, name=None)]

        if column_key is not None:
            # Verificar quais registros já existem no banco de dados usando column_key
            existing_records = set()
            select_query = sql.SQL("""
                SELECT {keys}
                FROM {table}
            """).format(
                keys=sql.SQL(', ').join(map(sql.Identifier, column_key)),
                table=sql.Identifier(table_name)
            )

            cursor.execute(select_query)
            existing_records = set(cursor.fetchall())

            # Filtrar os dados do DataFrame para inserir apenas registros novos
            data_to_insert = [row for row in data if tuple(row[:len(column_key)]) not in existing_records]

            if data_to_insert:
                # Executar a consulta de inserção com upsert para os registros novos
                extras.execute_values(cursor, insert_query, data_to_insert)
                conn.commit()
                print(f"Upsert realizado com sucesso na tabela {table_name}.")
            else:
                print(f"Nenhum dado novo para inserir na tabela {table_name}.")
        else:
            # Caso column_key seja None, executar a inserção para todos os registros
            if data:
                extras.execute_values(cursor, insert_query, data)
                conn.commit()
                print(f"Upsert realizado com sucesso na tabela {table_name}.")
            else:
                print(f"Nenhum dado novo para inserir na tabela {table_name}.")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao realizar upsert na tabela {table_name}: {str(e)}")
    finally:
        cursor.close()
        conn.close()


# ==================================================================================================================
# Extração diaria dos dados data warehouse para analise BI
def extract_postgres_datawarehouse(table_name):
    # URL de conexão ao PostgreSQL
    postgres_url = os.environ['DATAWAREHOUSE_URL']
    conn = psycopg2.connect(postgres_url)
    
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df