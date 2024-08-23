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
def save_to_mysql(data):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO confirmacoes (Nome) VALUES (%s)"
    cursor.executemany(query, [(nome,) for nome in data])
    db.commit()
    cursor.close()
    db.close()

# Função para remover um nome da lista
def remover_nome(nome):
    st.session_state['nomes_lista'].remove(nome)

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
        
        # Input para adicionar nome
        st.text_input("Digite o nome para e pressione ENTER para adicionar na lista:", key="input_nome", on_change=adicionar_nome)

        # Exibe a lista de nomes e botões de remoção
        st.write("Nomes na Lista (Caso esteja correta a sua lista de nomes clique em `Confirmar Lista`:")
        for i, nome in enumerate(st.session_state['nomes_lista']):
            col = st.columns([3, 1])
            col[0].write(nome)
            if col[1].button("Remover", key=f"remove_{i}"):
                remover_nome(nome)

        # Botão para confirmar a lista
        if st.button("Confirmar Lista"):
            if 'admin.corni' not in st.session_state['nomes_lista']:
                save_to_mysql(st.session_state['nomes_lista'])
                st.session_state['page'] = 'agradecimento'
                st.switch_page('pages/agradecimento.py')
            elif 'admin.corni' in st.session_state['nomes_lista']:
                st.switch_page('pages/confirmacoes.py')
            else:
                st.warning("Adicione ao menos um nome à lista.")

# Controle de página
if current_date > deadline:
    st.title("O prazo para confirmar a presença já passou.")
    st.switch_page('pages/agradecimento_final.py')
else:
    confirmacao_presenca()
