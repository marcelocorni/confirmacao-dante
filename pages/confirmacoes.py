import streamlit as st
import mysql.connector
import pandas as pd

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    mysql_config = {
        'user': st.secrets["db_username"],
        'password': st.secrets["db_password"],
        'host': 'mysql.desenvolvedor.net',
        'database': 'desenvolvedordb',
        'port': '3306'
    }
    return mysql.connector.connect(**mysql_config )
    # return mysql.connector.connect(
    #     host="mysql-3cdcc8f3-marcelo-eb41.b.aivencloud.com",   # Substitua pelo seu host MySQL
    #     user=st.secrets["db_username"],   # Substitua pelo seu usuário MySQL
    #     password=st.secrets["db_password"],   # Substitua pela sua senha MySQL
    #     database="dante",  # Substitua pelo nome do seu banco de dados
    #     port=13398
    # )

# Função para extrair dados do MySQL para um DataFrame
def export_confirmations_to_dataframe():
    db = connect_to_db()
    query = "SELECT Nome, Idade, Data, Pagante FROM confirmacoes ORDER BY Data, Nome"
    df = pd.read_sql(query, db)
    db.close()
    return df

# Tela de listagem das confirmações

st.title("Lista de Confirmações")

# Exportar os dados para um DataFrame
confirmations_df = export_confirmations_to_dataframe()

# Exibir o DataFrame
st.write(confirmations_df)