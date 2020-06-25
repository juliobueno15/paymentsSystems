# README

### Requisitos
- `python >= 3.5`

#### No diretório raiz do projeto executar o comando
- `python3 -m venv <nome da sua venv>`
- `source ./<nome da sua venv>/bin/activate`
- `pip install -r requirements.txt`

#### Cria estrutura do BD
- `./manage.py migrate`

### Criar usuário admistrativo
- `./manage.py createsuperuser`

#### Executar o servidor de desenvolvimento
- `./manage.py runserver`

## entrar no sistema
Após executar o servidor, deve-se entrar em http://localhost:8000/ para se ter acesso a página do sistema. No canto superior direito haverá um botão para login que levará o usuário a uma página onde ele pode efetuar o login com os dados registrados como super user ou então cadastrar-se como novo usuário.

## Arquivos inseridos no sistema
Os arquivos inseridos no sistema ficaram no diretório raiz do projeto dentro da pasta **media** 