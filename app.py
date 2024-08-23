import streamlit as st
import datetime
import mysql.connector

# Configurações iniciais
st.set_page_config(layout="wide", page_title="Confirmação de Presença")
deadline = datetime.datetime(2024, 9, 15)
current_date = datetime.datetime.now()

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


# Função para salvar os dados no MySQL
def save_to_mysql(nomes_lista):
    db = connect_to_db()
    cursor = db.cursor()
    insert_query = "INSERT INTO confirmacoes (Nome, Idade, Pagante) VALUES (%s, %s, %s)"
    data_to_insert = [
        (item['nome'], item['idade'], 1 if item['idade'] >= 5 else 0)
        for item in nomes_lista
    ]
    cursor.executemany(insert_query, data_to_insert)
    db.commit()
    cursor.close()
    db.close()

# Função para remover um nome da lista pelo índice
def remover_nome(index):
    if 'nomes_lista' in st.session_state:
        del st.session_state['nomes_lista'][index]

# Função para adicionar nome e limpar o campo
def adicionar_nome():
    if st.session_state['input_nome']:
        st.session_state['nomes_lista'].append(st.session_state['input_nome'])
        st.session_state['input_nome'] = ""  # Limpa o campo de texto

# Tela principal para confirmação de presença
def confirmacao_presenca():
    st.title("Confirmação de Presença")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        convite_img = "images/CONVITE_DANTE_5_ANOS_2024.png"  # Substitua pelo caminho da imagem do convite
        st.image(convite_img, use_column_width=True)
    
    with col2:
        # Verifica se a lista de nomes está no session_state
        if 'nomes_lista' not in st.session_state:
            st.session_state['nomes_lista'] = []
        
        # Inputs para Nome e Idade
        nome = st.text_input("Nome", key="nome_input")
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1, key="idade_input")

        if st.button("Adicionar à Lista"):
            if not nome.strip():
                st.warning("O campo Nome é obrigatório.")
            elif idade == 0:
                st.warning("Por favor, insira uma idade válida.")
            else:
                # Adiciona o nome e a idade à lista de sessão
                if 'nomes_lista' not in st.session_state:
                    st.session_state['nomes_lista'] = []
                st.session_state['nomes_lista'].append({'nome': nome.strip(), 'idade': idade})
    
        # Exibe a lista de nomes adicionados
        if 'nomes_lista' in st.session_state and st.session_state['nomes_lista']:
            st.subheader("Lista de Confirmados:")
            for i, item in enumerate(st.session_state['nomes_lista']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{item['nome']} ({item['idade']} anos)")
                with col2:
                    if st.button("Remover", key=f"remove_{i}"):
                        remover_nome(i)

        # Botão para confirmar a lista
        if st.button("Confirmar Lista"):
                # Verificação se a lista não está vazia
            if len(st.session_state['nomes_lista']) > 0:
                if not any(item['nome'] == 'admin.corni' for item in st.session_state['nomes_lista']):
                    save_to_mysql(st.session_state['nomes_lista'])
                    st.session_state['page'] = 'agradecimento'
                    st.switch_page('pages/agradecimento.py')
                if any(item['nome'] == 'admin.corni' for item in st.session_state['nomes_lista']):
                    st.switch_page('pages/confirmacoes.py')
            else:
                st.warning("Adicione ao menos um nome à lista.")

# Controle de página
if current_date > deadline:
    st.title("O prazo para confirmar a presença já passou.")
    st.switch_page('pages/agradecimento_final.py')
else:
    confirmacao_presenca()
