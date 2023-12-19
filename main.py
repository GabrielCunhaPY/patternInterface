import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

sequencia_atual = []
sequencia_display = None

# Função chamada quando um caractere é digitado
def on_key_press(event):
    global sequencia_atual, sequencia_display  # Adicionamos estas linhas para indicar que queremos usar as variáveis globais
    char = event.char
    if char:
        sequencia_atual.append(char)
        if len(sequencia_atual) > 10:
            sequencia_atual.pop(0)
        sequencia_display.config(text=''.join(sequencia_atual))
        id_padrao = verificar_sequencia(''.join(sequencia_atual))
        if id_padrao:
            messagebox.showinfo("Padrão Encontrado", f"Padrão ID: {id_padrao[0]} encontrado")

# Criar a tabela se não existir
def criar_tabela():
    conn = conectar()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS padroes (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          sequencia TEXT)''')
        conn.commit()
        conn.close()

# Conectar ao banco de dados MariaDB
def conectar():
    try:
        return mysql.connector.connect(
            host='localhost',       # ou o IP do seu servidor MariaDB
            user='root',           # seu usuário do MariaDB
            password='',           # sua senha do MariaDB
            database='padroes'     # nome do seu banco de dados
        )
    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        return None

# Adicionar uma nova sequência ao banco de dados
def adicionar_sequencia(sequencia):
    conn = conectar()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO padroes (sequencia) VALUES (%s)', (sequencia,))
        conn.commit()
        conn.close()

# Verificar a sequência digitada
def verificar_sequencia(sequencia):
    conn = conectar()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM padroes WHERE sequencia = %s', (sequencia,))
        data = cursor.fetchone()
        conn.close()
        return data

# Configurar a janela principal
root = tk.Tk()
root.title("Detector de Padrões")

# Campo para mostrar a sequência atual
sequencia_display = tk.Label(root, text='', font=('Helvetica', 16))
sequencia_display.pack()

# Entrada de texto para adicionar novos padrões
nova_sequencia_entry = tk.Entry(root)
nova_sequencia_entry.pack()

# Botão para adicionar novos padrões
adicionar_botao = tk.Button(root, text="Adicionar Padrão", command=lambda: adicionar_sequencia(nova_sequencia_entry.get()))
adicionar_botao.pack()

# Configurar evento de teclado
root.bind('<KeyPress>', on_key_press)

# Criar a tabela no banco de dados
criar_tabela()

# Iniciar o loop da interface gráfica
root.mainloop()
