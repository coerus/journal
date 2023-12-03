import sqlite3 as sql
from datetime import datetime
import sys

# Função para criar a tabela do diário se ainda não existir
def create_table():
    with sql.connect("journal.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                entry_date TEXT
            )
        """)

# Função para adicionar uma nova entrada ao diário com a data
def add_entry():
    print("Digite a sua entry diária. Pressione Ctrl-D (ou Ctrl-Z no Windows) para finalizar:")
    content = sys.stdin.read().rstrip('\n')
    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sql.connect("journal.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO entries (content, entry_date) VALUES (?, ?)", (content, entry_date))
        connection.commit()
        print("Entry adicionada com sucesso!")

# Função para visualizar todas as entradas no diário
# Função para visualizar todas as entradas no diário
def view_entries():
    with sql.connect("journal.db") as connection:
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
                print(f"Conteúdo:\n{entry[1]}\n")
            print("===========================================")
        else:
            print("Nenhuma entry encontrada.")


# Função para apagar uma entrada do diário
def delete_entry():
    entry_id = input("Digite o ID da entry que deseja apagar:\n")
    with sql.connect("journal.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM entries WHERE id=?", (entry_id,))
        connection.commit()
        print("Entry apagada com sucesso!")
        reset_autoincrement()

# Função para redefinir a sequência de autoincremento
def reset_autoincrement():
    with sql.connect("journal.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='entries'")
        connection.commit()
        print("Sequência de autoincremento resetada.")

# Cria a tabela se ainda não existir
create_table()

# Exibe o menu para o usuário
while True:
    print("""
    ===============================
                JOURNAL            
    ===============================
    1. Escrever uma nova entry
    2. Ver todas as entries
    3. Apagar uma entry
    4. Sair
    """)
    
    choice = input("Escolha uma opção (1/2/3/4):\n")
    
    if choice == "1":
        add_entry()
    elif choice == "2":
        view_entries()
    elif choice == "3":
        delete_entry()
    elif choice == "4":
        print("Saindo do Journal. Até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")
