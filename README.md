# SGMon: Sistema de Gerenciamento de Monografias

**SGMon** é uma plataforma web desenvolvida como projeto para a disciplina de Sistemas Distribuídos da **Universidade Federal dos Vales do Jequitinhonha e Mucuri (UFVJM)**. O sistema tem como objetivo gerenciar o ciclo de vida de Trabalhos de Conclusão de Curso (TCCs), desde a submissão pelo aluno até a avaliação e gerenciamento por parte dos professores e administradores.

## Funcionalidades Principais

* **Autenticação Completa:** Sistema de cadastro, login, logout e redefinição de senha para usuários.
* **Perfis de Usuário:** Três níveis de acesso distintos:
    * **Aluno:** Pode submeter, visualizar, editar e excluir suas próprias monografias.
    * **Professor:** Pode visualizar e editar as monografias que orienta.
    * **Administrador:** Tem controle total sobre o sistema através da interface de administração.
* **Fluxo de Aprovação para Professores:** Para garantir a segurança, novos cadastros de professores entram em um estado "pendente" e precisam ser aprovados manualmente por um administrador para ganhar acesso total.
* **CRUD de Monografias:** Funcionalidades completas para Criar, Ler, Atualizar e Deletar trabalhos.
* **Upload de Arquivos:** Permite o upload de documentos (PDF) associados a cada monografia.
* **Registro de Auditoria:** Rastreia todas as alterações (criação, edição) feitas em uma monografia, registrando quem fez a alteração e quando.
* **Ambiente Portátil:** Utiliza Docker para gerenciar o banco de dados PostgreSQL, facilitando a configuração do ambiente em qualquer máquina.

## Tecnologias Utilizadas

* **Backend:** Python 3.11, Django 5.1
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Banco de Dados:** PostgreSQL (gerenciado via Docker)
* **Autenticação:** `django-allauth`
* **Auditoria:** `django-simple-history`
* **Containerização:** Docker, Docker Compose

## Pré-requisitos

Para rodar este projeto, você precisará ter os seguintes softwares instalados na sua máquina:
* [Python 3.9+](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação.

**1. Clone o Repositório**
Abra seu terminal e clone o projeto do GitHub:
```bash
git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
cd <nome_da_pasta_do_projeto>
```

**2. Inicie o Banco de Dados com Docker**
Este comando irá baixar a imagem do PostgreSQL e iniciar o banco de dados em segundo plano. Certifique-se de que o Docker Desktop está rodando.
```bash
docker-compose up -d
```
> O `-d` significa "detached", ou seja, o terminal ficará livre. Para parar o contêiner do banco depois, use `docker-compose down`.

**3. Crie e Ative o Ambiente Virtual Python**
É uma boa prática isolar as dependências do projeto.
```bash
# Crie o ambiente
python -m venv venv

# Ative o ambiente
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

**4. Instale as Dependências do Python**
Instale todas as bibliotecas listadas no `requirements.txt`.
```bash
pip install -r requirements.txt
```

**5. Aplique as Migrações no Banco de Dados**
Este comando irá criar todas as tabelas no banco de dados que está rodando no Docker.
```bash
python manage.py migrate
```

**6. Crie um Superusuário (Administrador)**
Esta conta será usada para acessar a interface de administração (`/admin/`).
```bash
python manage.py createsuperuser
```
Siga os passos no terminal para definir o e-mail e a senha do administrador.

**7. Execute o Servidor Django**
```bash
python manage.py runserver
```
O site estará disponível no endereço: **http://127.0.0.1:8000/**

## Fluxo de Uso e Aprovação de Professores

O sistema possui um fluxo de aprovação para garantir que apenas professores legítimos tenham acesso às funcionalidades de orientação.

**1. Configuração Inicial do Admin**
Após criar o superusuário, acesse a área administrativa (`/admin/`) e crie os seguintes **Grupos**:
* `Alunos`
* `Professores`
* `Professores Pendentes`

**2. Cadastro de Aluno**
O cadastro de alunos é **100% automático**. Ao se cadastrar com o perfil "Sou Aluno(a)", o usuário já é adicionado ao grupo `Alunos` e pode usar o sistema imediatamente.

**3. Cadastro de Professor**
* Um usuário se cadastra escolhendo o perfil "Sou Professor(a)" e preenche seus dados (titulação, área de pesquisa).
* O sistema cria a conta e o perfil do professor, mas o adiciona automaticamente ao grupo **`Professores Pendentes`**.
* Neste estado, o professor pode fazer login, mas verá apenas uma mensagem no dashboard informando que sua conta aguarda aprovação.
* **Ação do Administrador:** O administrador do sistema deve acessar a interface (`/admin/`), ir até a lista de "Usuários", encontrar o professor pendente e **manualmente movê-lo** do grupo `Professores Pendentes` para o grupo `Professores`.
* Após a aprovação, o professor terá acesso total ao seu dashboard e funcionalidades.
