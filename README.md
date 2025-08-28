# Sistema de Login e Cadastro de Itens

## Visão Geral

Este projeto é uma aplicação de desktop desenvolvida em Python com a biblioteca **CustomTkinter**. Ele oferece uma interface gráfica moderna para autenticação de usuários (login e cadastro) e um sistema principal para o gerenciamento de itens, incluindo funcionalidades de cadastro, visualização, busca e exclusão.

## Funcionalidades

  - **Tela de Login**: Autenticação de usuários para acesso ao sistema principal.
  - **Tela de Cadastro**: Permite que novos usuários criem uma conta.
  - **Sistema Principal**:
      - **Cadastro de Itens**: Formulário para adicionar novos itens com nome, tipo, qualidade e quantidade.
      - **Visualização em Tabela**: Exibe todos os itens cadastrados em uma tabela organizada (`Treeview`).
      - **Busca de Itens**: Funcionalidade para pesquisar itens específicos na tabela.
      - **Exclusão de Itens**: Permite remover itens selecionados da lista.
  - **Interface Gráfica Moderna**: Utiliza o tema escuro e componentes estilizados do CustomTkinter para uma melhor experiência de usuário.


## Tecnologias e Dependências

  - **Python 3**
  - **CustomTkinter**: Biblioteca utilizada para criar a interface gráfica moderna.
  - **Tkinter**: Biblioteca padrão do Python para GUI, base para o CustomTkinter.

-----

## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em sua máquina local.

### 1\. Pré-requisitos

  - **Python 3.x** instalado.
  - **pip** (gerenciador de pacotes do Python).

### 2\. Instalação

**a. Clone o repositório:**

```bash
git clone https://github.com/lemosjr/sistema-de-estoque-ctk
cd sistema-de-estoque-ctk
```

**b. Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv
```

  - Para ativar no Windows:
    ```bash
    .\venv\Scripts\activate
    ```
  - Para ativar no macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

**c. Instale as dependências:**
A única dependência externa é o `customtkinter`. Instale-a com o pip:

```bash
pip install customtkinter
```

### 3\. Executando a Aplicação

Com as dependências instaladas, execute o arquivo principal para iniciar o sistema:

```bash
python main.py
```

A tela de login será exibida. Para acessar o sistema principal, utilize as credenciais padrão:

  - **Usuário**: `admin`
  - **Senha**: `123`

-----

## Estrutura dos Arquivos

O projeto está modularizado da seguinte forma para facilitar a manutenção:

  - `main.py`: Ponto de entrada da aplicação. Inicia o fluxo chamando a tela de login.
  - `login.py`: Contém a lógica e a interface gráfica da tela de login. Após um login bem-sucedido, ele chama o sistema principal.
  - `cadastro.py`: Responsável pela interface e funcionalidade da tela de cadastro de novos usuários.
  - `sistema.py`: Contém a janela principal da aplicação, onde o gerenciamento de itens é realizado.