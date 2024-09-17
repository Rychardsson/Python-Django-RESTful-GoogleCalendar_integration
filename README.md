# Task Management with Google Calendar

API Restful para criação de tarefas e integração com o Google Calendar

## Pré-requisitos
Certifique-se de ter os seguintes itens instalados em seu sistema:
- Python 3.11 ou superior
- pip (gerenciador de pacotes do Python)
- virtualenv (opcional, mas recomendado para criar ambientes virtuais)
- Django (a versão usada no projeto)
- Configurado Google Calendar API (credenciais necessárias)
- Bibliotecas Externas: Django Rest Framework (DRF), Google API Client

## Configurando as Credenciais do Google Calendar
1. Crie um projeto no [Console de Desenvolvedores do Google](https://developers.google.com/calendar/api/quickstart/python?hl=pt-br).
2. Habilite a Google Calendar API.
3. Crie credenciais para "Desktop App" e faça o download do arquivo `credentials.json`.
4. Coloque o arquivo `credentials.json` na raiz do projeto.

É importante deixar mais claro que o processo de autenticação com o Google Calendar e como o arquivo token.pickle será gerado após o meu primeiro login. Por exemplo, detalho que ao executar o aplicativo pela primeira vez, o navegador será aberto para eu autenticar minha conta do Google.

## Criando um Ambiente Virtual
```bash
python -m venv tarefa
```

### Ativando o ambiente virtual:
#### Windows:
```bash
tarefa\Scripts\activate
```
#### Linux/Mac:
```bash
source tarefa/bin/activate
```

### Instalando o Django e o Django Rest Framework:
```bash
pip install django djangorestframework google-auth google-auth-oauthlib google-auth-http
```

## Configuração do Banco de Dados
Acesse o diretório: gestor_de_tarefas

```bash
python cd gestor_de_tarefas
```
### 1. Criar Migrações
Primeiro, você precisa criar as migrações, que geram arquivos indicando as alterações na estrutura do banco de dados:
```bash
python manage.py makemigrations
```
Esse comando verifica os modelos definidos no arquivo `models.py` e cria as migrações com base nas alterações feitas.

### 2. Aplicar Migrações
Agora, aplique as migrações criadas ao banco de dados:
```bash
python manage.py migrate
```
Esse comando cria as tabelas no banco de dados com base nas migrações.

## Executando o Servidor
```bash
python manage.py runserver
```

## Testando a API com o Insomnia
Agora que o servidor está em execução, você pode testar a API com o Insomnia.

### Passos para Testar a API Usando o Insomnia
1. Instale o Insomnia: Se você ainda não tem o Insomnia instalado, você pode baixá-lo e instalá-lo no site oficial: [Insomnia Download](https://insomnia.rest/download).
2. Abra o Insomnia e crie um novo workspace:
    - Abra o Insomnia.
    - Clique em "Create" e selecione "Workspace".
    - Dê um nome ao workspace, como "Task API", e escolha o tipo de requisições de API.
3. Configure a URL Base:
    - Como sua API está sendo executada localmente, a URL base para todas as requisições será: `http://127.0.0.1:8000/api/tasks/`.
4. Crie uma Requisição POST (Criar Tarefa):
    - No Insomnia, clique em "New Request" e nomeie a requisição como "Create Task".
    - Selecione o método POST.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/`.
    - Na aba "Body", selecione o tipo JSON.
    - Insira o corpo da requisição com os dados da nova tarefa, por exemplo:
      ```json
      {
          "title": "Test Task",
          "description": "This is a test task",
          "date": "2024-09-15",
          "time": "14:00:00"
      }
      ```
    - Clique em Send.
5. Crie uma Requisição GET (Listar Tarefas):
    - Crie uma nova requisição chamada "List Tasks".
    - Selecione o método GET.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/`.
    - Clique em Send.
    - Essa requisição retornará uma lista de todas as tarefas criadas até o momento.
6. Crie uma Requisição GET para Recuperar uma Tarefa por ID:
    - Crie uma nova requisição chamada "Get Task by ID".
    - Selecione o método GET.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/{id}/`.
    - Substitua `{id}` pelo ID da tarefa que você deseja recuperar. Por exemplo: `http://127.0.0.1:8000/api/tasks/1/`.
    - Clique em Send.
7. Crie uma Requisição GET para Pesquisar por Título:
    - Selecione o método GET.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/?search=task_title`.
    - Substitua `task_title` pelo título da tarefa que você deseja pesquisar.
8. Crie uma Requisição GET para Pesquisar por Intervalo de Datas:
    - Selecione o método GET.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/?date_range_after=2024-09-10&date_range_before=2024-09-20`.
    - Substitua `2024-09-10` e `2024-09-20` pelo intervalo de datas desejado.
9. Crie uma Requisição PUT (Atualizar Tarefa):
    - Crie uma nova requisição chamada "Update Task".
    - Selecione o método PUT.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/{id}/`.
    - Substitua `{id}` pelo ID da tarefa que você deseja atualizar.
    - Na aba "Body", selecione JSON.
    - Insira os dados atualizados da tarefa, por exemplo:
      ```json
      {
          "title": "Updated Task",
          "description": "This task was updated",
          "date": "2024-09-16",
          "time": "16:00:00"
      }
      ```
    - Clique em Send.
10. Crie uma Requisição DELETE (Excluir Tarefa):
    - Crie uma nova requisição chamada "Delete Task".
    - Selecione o método DELETE.
    - Utilize a URL: `http://127.0.0.1:8000/api/tasks/{id}/`.
    - Substitua `{id}` pelo ID da tarefa que você deseja excluir.
    - Clique em Send.


## Licença
MIT License

```
Copyright (c) 2024 [Rychardsson]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
```

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
