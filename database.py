import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
    
    def criar_tabelas(self):
        # Tabela de livros
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            status TEXT NOT NULL,
            data_cadastro TEXT NOT NULL
        )
        ''')
        
        # Tabela de empréstimos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            amigo TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            FOREIGN KEY (livro_id) REFERENCES livros (id)
        )
        ''')
        
        self.conn.commit()
    
    def adicionar_livro(self, titulo, autor, genero, status):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
        INSERT INTO livros (titulo, autor, genero, status, data_cadastro)
        VALUES (?, ?, ?, ?, ?)
        ''', (titulo, autor, genero, status, data_atual))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def buscar_livros(self, criterio=None, valor=None):
        if criterio and valor:
            consulta = f"SELECT * FROM livros WHERE {criterio} LIKE ?"
            self.cursor.execute(consulta, (f'%{valor}%',))
        else:
            self.cursor.execute("SELECT * FROM livros ORDER BY titulo")
        return self.cursor.fetchall()
    
    def atualizar_livro(self, id, titulo, autor, genero, status):
        self.cursor.execute('''
        UPDATE livros SET titulo=?, autor=?, genero=?, status=?
        WHERE id=?
        ''', (titulo, autor, genero, status, id))
        self.conn.commit()
    
    def deletar_livro(self, id):
        # Primeiro, verificar se há empréstimos ativos
        self.cursor.execute('''
        SELECT COUNT(*) FROM emprestimos 
        WHERE livro_id=? AND data_devolucao IS NULL
        ''', (id,))
        
        emprestimos_ativos = self.cursor.fetchone()[0]
        if emprestimos_ativos > 0:
            return False
        
        # Excluir empréstimos relacionados ao livro (histórico)
        self.cursor.execute("DELETE FROM emprestimos WHERE livro_id=?", (id,))
        
        # Excluir o livro
        self.cursor.execute("DELETE FROM livros WHERE id=?", (id,))
        self.conn.commit()
        return True
    
    def registrar_emprestimo(self, livro_id, amigo):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
        INSERT INTO emprestimos (livro_id, amigo, data_emprestimo, data_devolucao)
        VALUES (?, ?, ?, NULL)
        ''', (livro_id, amigo, data_atual))
        self.conn.commit()
        
        # Atualizar status do livro para "Emprestado"
        self.cursor.execute("UPDATE livros SET status='Emprestado' WHERE id=?", (livro_id,))
        self.conn.commit()
    
    def registrar_devolucao(self, emprestimo_id):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        
        # Obter o livro_id associado a este empréstimo antes de atualizar
        self.cursor.execute("SELECT livro_id FROM emprestimos WHERE id=?", (emprestimo_id,))
        resultado = self.cursor.fetchone()
        
        if not resultado:
            return False
            
        livro_id = resultado[0]
        
        # Atualizar a data de devolução do empréstimo
        self.cursor.execute('''
        UPDATE emprestimos SET data_devolucao=?
        WHERE id=?
        ''', (data_atual, emprestimo_id))
        
        # Atualizar status do livro para "Disponível"
        self.cursor.execute("UPDATE livros SET status='Disponível' WHERE id=?", (livro_id,))
        self.conn.commit()
        return True
    
    def listar_emprestimos(self, apenas_ativos=True):
        if apenas_ativos:
            consulta = '''
            SELECT e.id, l.titulo, l.autor, e.amigo, e.data_emprestimo
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            WHERE e.data_devolucao IS NULL
            ORDER BY e.data_emprestimo DESC
            '''
        else:
            consulta = '''
            SELECT e.id, l.titulo, l.autor, e.amigo, e.data_emprestimo, e.data_devolucao
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            ORDER BY e.data_emprestimo DESC
            '''
        
        self.cursor.execute(consulta)
        return self.cursor.fetchall()
    
    def fechar_conexao(self):
        self.conn.close()