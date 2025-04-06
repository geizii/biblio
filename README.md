# Sistema de Gestão de Biblioteca Pessoal

Um aplicativo desktop desenvolvido em Python para gerenciar sua coleção pessoal de livros e acompanhar empréstimos.

## Funcionalidades

- **Gerenciamento de Livros**

  - Adicionar novos livros com título, autor, gênero e status
  - Pesquisar livros por título, autor, gênero ou status
  - Editar informações de livros existentes
  - Excluir livros da biblioteca

- **Controle de Empréstimos**
  - Registrar empréstimos de livros para amigos
  - Visualizar todos os empréstimos ativos
  - Registrar devoluções de livros
  - Acompanhamento automático do status dos livros (Disponível, Lido, Emprestado)

## Requisitos

- Python 3.6 ou superior
- SQLite3 (incluído na biblioteca padrão do Python)
- Tkinter (incluído na maioria das instalações padrão do Python)

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto
2. Certifique-se de que Python 3.6+ está instalado em seu sistema
3. Nenhuma instalação adicional é necessária, pois o projeto utiliza apenas bibliotecas padrão do Python

## Como Executar

Execute o arquivo `main.py` para iniciar o aplicativo:

```bash
python main.py
```

Na primeira execução, o banco de dados será criado automaticamente.

## Estrutura do Projeto

- `main.py` - Ponto de entrada do aplicativo
- `interface.py` - Interface gráfica usando Tkinter
- `database.py` - Gerenciamento de banco de dados SQLite
- `livro.py` - Classe para representar um livro
- `emprestimo.py` - Classe para representar um empréstimo

## Utilizando o Sistema

### Gerenciando Livros

1. **Adicionar um livro**

   - Preencha os campos de título, autor, gênero e selecione o status
   - Clique em "Adicionar Livro"
   - Se o status for "Emprestado", será solicitado o nome da pessoa que está com o livro

2. **Pesquisar livros**

   - Selecione o critério de pesquisa (título, autor, gênero ou status)
   - Digite o valor de pesquisa
   - Clique em "Pesquisar"
   - Use "Mostrar Todos" para ver todos os livros

3. **Editar um livro**

   - Dê um duplo clique em um livro na lista ou clique com o botão direito e selecione "Editar"
   - Modifique as informações e salve

4. **Excluir um livro**
   - Clique com o botão direito sobre um livro na lista e selecione "Excluir"
   - Confirme a exclusão

### Gerenciando Empréstimos

1. **Emprestar um livro**

   - Selecione um livro com status "Disponível"
   - Clique com o botão direito e selecione "Emprestar"
   - Insira o nome da pessoa e confirme

2. **Visualizar empréstimos ativos**

   - Selecione a aba "Empréstimos" para ver todos os empréstimos em aberto

3. **Registrar uma devolução**
   - Na aba "Empréstimos", dê um duplo clique no empréstimo ou clique com o botão direito e selecione "Registrar Devolução"
   - Confirme a devolução

## Banco de Dados

O sistema utiliza SQLite para armazenar os dados, criando um arquivo chamado `biblioteca.db` no diretório do projeto. O banco contém duas tabelas principais:

- `livros`: Armazena informações sobre os livros
- `emprestimos`: Registra empréstimos e devoluções
