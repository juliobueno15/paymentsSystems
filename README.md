# README

### Criando o ambiente virtual para projeto já existente

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