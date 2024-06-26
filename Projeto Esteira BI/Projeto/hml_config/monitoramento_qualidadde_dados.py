# ==================================================================================================================
# Import de bibliotaca 
from datetime import datetime, timedelta
import pandas as pd

# ==================================================================================================================
# Verificar se todos os campos obrigatórios possuem dados relatorio de completude
def generate_completeness_report(df, table_name):
    completeness_report = df.isnull().mean().reset_index()
    completeness_report.columns = ['column', 'missing_percentage']
    completeness_report['table'] = table_name
    return completeness_report


# ==================================================================================================================
# Verificar se não há registros duplicados onde não deveria haver relatorio de unicidade
def generate_uniqueness_report(df, table_name, unique_keys):
    if not unique_keys:
        print(f"No unique keys provided for table {table_name}")
        return pd.DataFrame(columns=['table', 'column', 'unique_percentage'])
    
    uniqueness_report_data = []
    
    for column in unique_keys:
        if column in df.columns:
            unique_count = df[column].nunique()
            total_count = len(df)
            if total_count == 0:
                unique_percentage = 0
                print(f"Warning: DataFrame for table '{table_name}' is empty.")
            else:
                unique_percentage = (unique_count / total_count) * 100
            uniqueness_report_data.append({
                'table': table_name,
                'column': column,
                'unique_percentage': unique_percentage
            })
        else:
            print(f"Warning: Column '{column}' not found in table '{table_name}'")
    
    uniqueness_report = pd.DataFrame(uniqueness_report_data)
    return uniqueness_report


# ==================================================================================================================
# Gera um relatorio de resumo com o nome da tabela, quantidade de linhas e a data atual
def generate_summary_report(df, table_name):
    # Quantidade de linhas
    quantity = len(df)

    # Data atual
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Dataframe pandas do relatorio
    summary_report = pd.DataFrame({
        'table_name': [table_name],
        'quantity': [quantity],
        'date': [current_date]
    })
    
    return summary_report