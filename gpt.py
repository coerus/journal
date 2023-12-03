import sqlite3 as sql
from datetime import datetime
import sys

# Função para criar a tabela do diário se ainda não existir
def create_table():
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                entry_date TEXT,
                category TEXT
            )
        """)

# Função para criar a tabela de senhas se ainda não existir
def create_password_table():
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )
        """)

# Função para definir ou atualizar a senha
def set_password():
    password = input("Digite a nova senha para o diário:\n")
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM passwords")
        cursor.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
        connection.commit()
        print("Senha definida com sucesso!")

# Função para verificar a senha
def check_password(input_password):
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM passwords")
        saved_password = cursor.fetchone()
        if saved_password and input_password == saved_password[1]:
            return True
        else:
            return False

# Função para adicionar uma nova entrada ao diário com a data e categoria
def add_entry():
    print("Digite a sua entry diária. Pressione Ctrl-D (ou Ctrl-Z no Windows) para finalizar:")
    content = sys.stdin.read().rstrip('\n')
    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    category = input("Digite a categoria da entrada:\n")

    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO entries (content, entry_date, category) VALUES (?, ?, ?)", (content, entry_date, category))
        connection.commit()
        print("Entry adicionada com sucesso!")

# Função para visualizar todas as entradas no diário
def view_entries():
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM entries")
        entries = cursor.fetchall()
        if entries:
            print("\n===========================================")
            print("            ENTRADAS NO DIÁRIO              ")
            print("===========================================\n")
            for entry in entries:
                print(f"ID: {entry[0]}")
                print(f"Data: {entry[2]}")
                print(f"Categoria: {entry[3]}")
                print(f"Conteúdo:\n{entry[1]}\n")
            print("===========================================")
        else:
            print("Nenhuma entry encontrada.")

# Função para apagar uma entrada do diário
def delete_entry():
    entry_id = input("Digite o ID da entry que deseja apagar:\n")
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM entries WHERE id=?", (entry_id,))
        connection.commit()
        print("Entry apagada com sucesso!")

# Função para redefinir a sequência de autoincremento
def reset_autoincrement():
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='entries'")
        connection.commit()
        print("Sequência de autoincremento resetada.")

# Função para pesquisar entradas por palavras-chave
def search_entries_by_keyword(keyword):
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM entries WHERE content LIKE ?", ('%' + keyword + '%',))
        entries = cursor.fetchall()
        if entries:
            print("\n===========================================")
            print(f"    ENTRADAS CONTENDO A PALAVRA-CHAVE '{keyword}'")
            print("===========================================\n")
            for entry in entries:
                print(f"ID: {entry[0]}")
                print(f"Data: {entry[2]}")
                print(f"Categoria: {entry[3]}")
                print(f"Conteúdo:\n{entry[1]}\n")
            print("===========================================")
        else:
            print(f"Nenhuma entrada contendo a palavra-chave '{keyword}' encontrada.")

# Função para exportar entradas para um arquivo de texto
def export_entries_to_file():
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM entries")
        entries = cursor.fetchall()
        if entries:
            with open("chat_export.txt", "w", encoding="utf-8") as file:
                for entry in entries:
                    file.write(f"ID: {entry[0]}\n")
                    file.write(f"Data: {entry[2]}\n")
                    file.write(f"Categoria: {entry[3]}\n")
                    file.write(f"Conteúdo:\n{entry[1]}\n\n")
            print("Entradas exportadas para 'chat_export.txt' com sucesso.")
        else:
            print("Nenhuma entrada para exportar.")

# Função para editar uma entrada existente
def edit_entry():
    entry_id = input("Digite o ID da entry que deseja editar:\n")
    with sql.connect("chat.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM entries WHERE id=?", (entry_id,))
        entry = cursor.fetchone()
        if entry:
            print(f"Editando a entrada ID {entry[0]}:\n")
            new_content = input("Digite o novo conteúdo da entrada:\n")
            cursor.execute("UPDATE entries SET content=? WHERE id=?", (new_content, entry_id))
            connection.commit()
            print("Entrada editada com sucesso!")
        else:
            print(f"Entrada com ID {entry_id} não encontrada.")

# Cria a tabela se ainda não existir
create_table()
create_password_table()

# Exibe o menu para o usuário
while True:
    print("""
    ===============================
                JOURNAL            
    ===============================
    1. Escrever uma nova entry
    2. Ver todas as entries
    3. Apagar uma entry
    4. Pesquisar por palavra-chave
    5. Exportar entradas para arquivo
    6. Editar uma entry
    7. Definir ou atualizar senha
    8. Verificar senha
    9. Sair
    """)
    
    choice = input("Escolha uma opção: ")
    
    if choice == "1":
        add_entry()
    elif choice == "2":
        view_entries()
    elif choice == "3":
        delete_entry()
