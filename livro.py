class Livro:
    def __init__(self, id=None, titulo="", autor="", genero="", status="Disponível", data_cadastro=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.status = status
        self.data_cadastro = data_cadastro
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.status})"
    
    def esta_disponivel(self):
        return self.status == "Disponível"
    
    def esta_lido(self):
        return self.status == "Lido"
    
    def marcar_como_lido(self):
        self.status = "Lido"
    
    def marcar_como_disponivel(self):
        self.status = "Disponível"
    
    def marcar_como_emprestado(self):
        self.status = "Emprestado"