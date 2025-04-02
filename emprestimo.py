from datetime import datetime

class Emprestimo:
    def __init__(self, id=None, livro_id=None, livro_titulo="", amigo="", data_emprestimo=None, data_devolucao=None):
        self.id = id
        self.livro_id = livro_id
        self.livro_titulo = livro_titulo
        self.amigo = amigo
        self.data_emprestimo = data_emprestimo or datetime.now().strftime("%Y-%m-%d")
        self.data_devolucao = data_devolucao
    
    def __str__(self):
        status = "Devolvido" if self.data_devolucao else "Em aberto"
        return f"{self.livro_titulo} - emprestado para {self.amigo} em {self.data_emprestimo} ({status})"
    
    def esta_ativo(self):
        return self.data_devolucao is None
    
    def calcular_dias_emprestado(self):
        data_emp = datetime.strptime(self.data_emprestimo, "%Y-%m-%d")
        
        if self.data_devolucao:
            data_dev = datetime.strptime(self.data_devolucao, "%Y-%m-%d")
        else:
            data_dev = datetime.now()
            
        return (data_dev - data_emp).days