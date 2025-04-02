import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from livro import Livro
from emprestimo import Emprestimo

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Biblioteca Pessoal")
        self.root.geometry("800x600")
        self.db = Database()
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Criar abas
        self.tab_livros = ttk.Frame(self.notebook)
        self.tab_emprestimos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_livros, text="Livros")
        self.notebook.add(self.tab_emprestimos, text="Empréstimos")
        
        # Inicializar interfaces de cada aba
        self.inicializar_aba_livros()
        self.inicializar_aba_emprestimos()
        
        # Vincular evento de mudança de aba para atualizar os dados
        self.notebook.bind("<<NotebookTabChanged>>", self.atualizar_aba_selecionada)
    
    def atualizar_aba_selecionada(self, event=None):
        """Atualiza os dados da aba selecionada quando o usuário muda de aba"""
        tab_index = self.notebook.index(self.notebook.select())
        if tab_index == 0:  # Aba de livros
            self.mostrar_todos_livros()
        elif tab_index == 1:  # Aba de empréstimos
            self.carregar_emprestimos()
    
    def inicializar_aba_livros(self):
        # Frame para adicionar livros
        frame_add = ttk.LabelFrame(self.tab_livros, text="Adicionar Livro")
        frame_add.pack(fill="x", padx=10, pady=10)
        
        # Campos para adicionar livro
        ttk.Label(frame_add, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.titulo_entry = ttk.Entry(frame_add, width=30)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_add, text="Autor:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.autor_entry = ttk.Entry(frame_add, width=30)
        self.autor_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_add, text="Gênero:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.genero_entry = ttk.Entry(frame_add, width=30)
        self.genero_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_add, text="Status:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.status_var = tk.StringVar(value="Disponível")
        status_combo = ttk.Combobox(frame_add, textvariable=self.status_var, values=["Disponível", "Lido", "Emprestado"])
        status_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Botão para adicionar
        ttk.Button(frame_add, text="Adicionar Livro", command=self.adicionar_livro).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Frame para pesquisa
        frame_pesquisa = ttk.LabelFrame(self.tab_livros, text="Pesquisar Livros")
        frame_pesquisa.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(frame_pesquisa, text="Critério:").grid(row=0, column=0, padx=5, pady=5)
        self.criterio_var = tk.StringVar(value="titulo")
        criterio_combo = ttk.Combobox(frame_pesquisa, textvariable=self.criterio_var, 
                                    values=["titulo", "autor", "genero", "status"])
        criterio_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_pesquisa, text="Valor:").grid(row=0, column=2, padx=5, pady=5)
        self.valor_pesquisa = ttk.Entry(frame_pesquisa, width=30)
        self.valor_pesquisa.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_pesquisa, text="Pesquisar", command=self.pesquisar_livros).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frame_pesquisa, text="Mostrar Todos", command=self.mostrar_todos_livros).grid(row=0, column=5, padx=5, pady=5)
        
        # Treeview para mostrar livros
        frame_lista = ttk.LabelFrame(self.tab_livros, text="Lista de Livros")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_livros = ttk.Treeview(frame_lista, columns=("ID", "Título", "Autor", "Gênero", "Status", "Data"), show="headings")
        self.tree_livros.heading("ID", text="ID")
        self.tree_livros.heading("Título", text="Título")
        self.tree_livros.heading("Autor", text="Autor")
        self.tree_livros.heading("Gênero", text="Gênero")
        self.tree_livros.heading("Status", text="Status")
        self.tree_livros.heading("Data", text="Data Cadastro")
        
        self.tree_livros.column("ID", width=50)
        self.tree_livros.column("Título", width=200)
        self.tree_livros.column("Autor", width=150)
        self.tree_livros.column("Gênero", width=100)
        self.tree_livros.column("Status", width=100)
        self.tree_livros.column("Data", width=100)
        
        self.tree_livros.pack(fill="both", expand=True)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_livros.yview)
        self.tree_livros.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Menu de contexto para a árvore
        self.menu_contexto = tk.Menu(self.tree_livros, tearoff=0)
        self.menu_contexto.add_command(label="Editar", command=self.abrir_editor_livro)
        self.menu_contexto.add_command(label="Excluir", command=self.excluir_livro)
        self.menu_contexto.add_separator()
        self.menu_contexto.add_command(label="Emprestar", command=self.abrir_dialog_emprestimo)
        
        self.tree_livros.bind("<Button-3>", self.mostrar_menu_contexto)
        self.tree_livros.bind("<Double-1>", lambda e: self.abrir_editor_livro())
        
        # Carregar dados iniciais
        self.mostrar_todos_livros()
    
    def inicializar_aba_emprestimos(self):
        # Frame para gerenciar empréstimos
        frame_emprestimos = ttk.LabelFrame(self.tab_emprestimos, text="Empréstimos Ativos")
        frame_emprestimos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview para mostrar empréstimos
        self.tree_emprestimos = ttk.Treeview(frame_emprestimos, 
                                            columns=("ID", "Livro", "Autor", "Amigo", "Data Empréstimo"),
                                            show="headings")
        self.tree_emprestimos.heading("ID", text="ID")
        self.tree_emprestimos.heading("Livro", text="Livro")
        self.tree_emprestimos.heading("Autor", text="Autor")
        self.tree_emprestimos.heading("Amigo", text="Emprestado para")
        self.tree_emprestimos.heading("Data Empréstimo", text="Data Empréstimo")
        
        self.tree_emprestimos.column("ID", width=50)
        self.tree_emprestimos.column("Livro", width=200)
        self.tree_emprestimos.column("Autor", width=150)
        self.tree_emprestimos.column("Amigo", width=150)
        self.tree_emprestimos.column("Data Empréstimo", width=150)
        
        self.tree_emprestimos.pack(fill="both", expand=True)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(frame_emprestimos, orient="vertical", command=self.tree_emprestimos.yview)
        self.tree_emprestimos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Botão para registrar devolução
        ttk.Button(self.tab_emprestimos, text="Registrar Devolução", 
                 command=self.registrar_devolucao).pack(pady=10)
        
        # Menu de contexto para empréstimos
        self.menu_emprestimos = tk.Menu(self.tree_emprestimos, tearoff=0)
        self.menu_emprestimos.add_command(label="Registrar Devolução", command=self.registrar_devolucao)
        
        self.tree_emprestimos.bind("<Button-3>", self.mostrar_menu_emprestimos)
        self.tree_emprestimos.bind("<Double-1>", lambda e: self.registrar_devolucao())
        
        # Carregar empréstimos ativos
        self.carregar_emprestimos()
    
    def adicionar_livro(self):
        titulo = self.titulo_entry.get().strip()
        autor = self.autor_entry.get().strip()
        genero = self.genero_entry.get().strip()
        status = self.status_var.get()
        
        if not titulo or not autor:
            messagebox.showerror("Erro", "Título e autor são obrigatórios!")
            return
        
        livro_id = self.db.adicionar_livro(titulo, autor, genero, status)
        
        # Se o status inicial for "Emprestado", abrir diálogo para pedir informações do empréstimo
        if status == "Emprestado":
            self.abrir_dialog_emprestimo_para_livro(livro_id, titulo, autor)
        else:
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado com sucesso!")
        
        # Limpar campos
        self.titulo_entry.delete(0, tk.END)
        self.autor_entry.delete(0, tk.END)
        self.genero_entry.delete(0, tk.END)
        self.status_var.set("Disponível")
        
        # Atualizar lista
        self.mostrar_todos_livros()
    
    def abrir_dialog_emprestimo_para_livro(self, livro_id, titulo, autor):
        """Abre diálogo de empréstimo para um livro recém-adicionado com status 'Emprestado'"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Informações do Empréstimo: {titulo}")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text=f"Livro: {titulo} - {autor}").pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Emprestado para:").pack(padx=10, pady=5)
        amigo_entry = ttk.Entry(dialog, width=30)
        amigo_entry.pack(padx=10, pady=5)
        amigo_entry.focus()
        
        def registrar():
            amigo = amigo_entry.get().strip()
            if not amigo:
                messagebox.showerror("Erro", "Informe o nome do amigo!")
                return
            
            self.db.registrar_emprestimo(livro_id, amigo)
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado e emprestado para {amigo}!")
            dialog.destroy()
            self.mostrar_todos_livros()
            self.carregar_emprestimos()
        
        ttk.Button(dialog, text="Registrar Empréstimo", command=registrar).pack(pady=10)
    
    def pesquisar_livros(self):
        criterio = self.criterio_var.get()
        valor = self.valor_pesquisa.get().strip()
        
        if not valor:
            messagebox.showinfo("Atenção", "Digite um valor para pesquisar.")
            return
        
        resultados = self.db.buscar_livros(criterio, valor)
        self.atualizar_tree_livros(resultados)
    
    def mostrar_todos_livros(self):
        livros = self.db.buscar_livros()
        self.atualizar_tree_livros(livros)
    
    def atualizar_tree_livros(self, livros):
        # Limpar treeview
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        # Adicionar livros à treeview
        for livro in livros:
            self.tree_livros.insert("", "end", values=livro)
    
    def mostrar_menu_contexto(self, event):
        # Selecionar item sob o cursor
        iid = self.tree_livros.identify_row(event.y)
        if iid:
            self.tree_livros.selection_set(iid)
            self.menu_contexto.post(event.x_root, event.y_root)
    
    def mostrar_menu_emprestimos(self, event):
        iid = self.tree_emprestimos.identify_row(event.y)
        if iid:
            self.tree_emprestimos.selection_set(iid)
            self.menu_emprestimos.post(event.x_root, event.y_root)
    
    def abrir_editor_livro(self):
        selecao = self.tree_livros.selection()
        if not selecao:
            return
        
        # Obter dados do livro selecionado
        item = self.tree_livros.item(selecao)
        livro_id, titulo, autor, genero, status, _ = item['values']
        
        # Criar janela de edição
        editor = tk.Toplevel(self.root)
        editor.title(f"Editar Livro: {titulo}")
        editor.geometry("400x200")
        editor.resizable(False, False)
        
        ttk.Label(editor, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        titulo_entry = ttk.Entry(editor, width=30)
        titulo_entry.insert(0, titulo)
        titulo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(editor, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        autor_entry = ttk.Entry(editor, width=30)
        autor_entry.insert(0, autor)
        autor_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(editor, text="Gênero:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        genero_entry = ttk.Entry(editor, width=30)
        genero_entry.insert(0, genero)
        genero_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(editor, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        status_var = tk.StringVar(value=status)
        status_combo = ttk.Combobox(editor, textvariable=status_var, values=["Disponível", "Lido", "Emprestado"])
        status_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Salvar status original para comparação posterior
        status_original = status
        
        def salvar_edicao():
            novo_titulo = titulo_entry.get().strip()
            novo_autor = autor_entry.get().strip()
            novo_genero = genero_entry.get().strip()
            novo_status = status_var.get()
            
            if not novo_titulo or not novo_autor:
                messagebox.showerror("Erro", "Título e autor são obrigatórios!")
                return
            
            # Verificar se houve mudança de status para "Emprestado"
            if status_original != "Emprestado" and novo_status == "Emprestado":
                editor.destroy()
                # Se status mudou para "Emprestado", abrir diálogo para emprestar
                self.abrir_dialog_emprestimo_para_livro(livro_id, novo_titulo, novo_autor)
            # Verificar se livro estava emprestado e agora está "Disponível"
            elif status_original == "Emprestado" and novo_status != "Emprestado":
                # Atualizar o empréstimo atual como devolvido
                self.db.cursor.execute("""
                    UPDATE emprestimos 
                    SET data_devolucao=datetime('now') 
                    WHERE livro_id=? AND data_devolucao IS NULL
                """, (livro_id,))
                self.db.conn.commit()
            
            self.db.atualizar_livro(livro_id, novo_titulo, novo_autor, novo_genero, novo_status)
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            editor.destroy()
            self.mostrar_todos_livros()
            self.carregar_emprestimos()
        
        ttk.Button(editor, text="Salvar", command=salvar_edicao).grid(row=4, column=0, columnspan=2, pady=10)
    
    def excluir_livro(self):
        selecao = self.tree_livros.selection()
        if not selecao:
            return
        
        # Obter dados do livro selecionado
        item = self.tree_livros.item(selecao)
        livro_id, titulo, autor, _, status, _ = item['values']
        
        # Verificar se o livro está emprestado
        if status == "Emprestado":
            messagebox.showwarning("Atenção", 
                                 f"O livro '{titulo}' está emprestado. Registre a devolução antes de excluí-lo.")
            return
        
        # Confirmar exclusão
        confirmacao = messagebox.askyesno("Confirmar Exclusão", 
                                         f"Deseja realmente excluir o livro '{titulo}' de {autor}?")
        if confirmacao:
            self.db.deletar_livro(livro_id)
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
            self.mostrar_todos_livros()
            self.carregar_emprestimos()
    
    def abrir_dialog_emprestimo(self):
        selecao = self.tree_livros.selection()
        if not selecao:
            return
        
        # Obter dados do livro selecionado
        item = self.tree_livros.item(selecao)
        livro_id, titulo, autor, _, status, _ = item['values']
        
        # Verificar se o livro está disponível
        if status != "Disponível":
            messagebox.showwarning("Indisponível", 
                                 f"O livro '{titulo}' não está disponível para empréstimo.")
            return
        
        # Criar janela de empréstimo
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Emprestar: {titulo}")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        
        ttk.Label(dialog, text=f"Livro: {titulo} - {autor}").pack(padx=10, pady=5)
        
        ttk.Label(dialog, text="Emprestar para:").pack(padx=10, pady=5)
        amigo_entry = ttk.Entry(dialog, width=30)
        amigo_entry.pack(padx=10, pady=5)
        amigo_entry.focus()
        
        def registrar():
            amigo = amigo_entry.get().strip()
            if not amigo:
                messagebox.showerror("Erro", "Informe o nome do amigo!")
                return
            
            self.db.registrar_emprestimo(livro_id, amigo)
            messagebox.showinfo("Sucesso", f"Livro emprestado com sucesso para {amigo}!")
            dialog.destroy()
            self.mostrar_todos_livros()
            self.carregar_emprestimos()
            
            # Mudar para a aba de empréstimos para mostrar o novo empréstimo
            self.notebook.select(1)  # Seleciona a segunda aba (empréstimos)
        
        ttk.Button(dialog, text="Registrar Empréstimo", command=registrar).pack(pady=10)
    
    def carregar_emprestimos(self):
        # Limpar treeview
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        # Buscar empréstimos ativos
        emprestimos = self.db.listar_emprestimos(apenas_ativos=True)
        
        # Adicionar à treeview
        for emp in emprestimos:
            self.tree_emprestimos.insert("", "end", values=emp)
    
    def registrar_devolucao(self):
        selecao = self.tree_emprestimos.selection()
        if not selecao:
            messagebox.showinfo("Selecione", "Selecione um empréstimo para registrar a devolução.")
            return
        
        # Obter ID do empréstimo selecionado
        item = self.tree_emprestimos.item(selecao)
        emprestimo_id = item['values'][0]
        livro_titulo = item['values'][1]
        amigo = item['values'][3]
        
        # Confirmar devolução
        confirmacao = messagebox.askyesno("Confirmar Devolução", 
                                        f"Confirmar a devolução do livro '{livro_titulo}' por {amigo}?")
        if confirmacao:
            self.db.registrar_devolucao(emprestimo_id)
            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
            self.carregar_emprestimos()
            self.mostrar_todos_livros()