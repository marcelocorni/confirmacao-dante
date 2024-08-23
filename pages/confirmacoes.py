import streamlit as st
import mysql.connector

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="mysql-3cdcc8f3-marcelo-eb41.b.aivencloud.com",   # Substitua pelo seu host MySQL
        user="avnadmin",   # Substitua pelo seu usuário MySQL
        password="AVNS_f7wJl9lniRrPZYsailW",   # Substitua pela sua senha MySQL
        database="dante",  # Substitua pelo nome do seu banco de dados
        port=13398
    )

# Tela de listagem das confirmações

st.title("Lista de Confirmações")

db = connect_to_db()
cursor = db.cursor()
query = "SELECT Nome, Data FROM confirmacoes ORDER BY Data, Nome"
cursor.execute(query)
results = cursor.fetchall()
cursor.close()
db.close()

st.write("Confirmações:")
for row in results:
    st.write(f"{row[1]} - {row[0]}")