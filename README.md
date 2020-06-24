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


### Criando novos módulos do projeto

##### No diretório do projeto execute
- `./manage.py startapp <modulo>`

##### Logo após a criação de uma nova app, é necessário registrá-la
##### adicionando o nome da app <modulo> na lista 'INSTALLED_APPS' do arquivo
##### <nome do projeto>/settings.py

#### Após criar classes do bd no model
- `./manage.py makemigrations`
- `./manage.py migrate`


### Criando novo projeto
```
python3 -m venv venvtemp
source ./venvtemp/bin/activate
pip install django
django-admin startproject <nome do projeto>
deactivate
rm -rf venvtemp
cd <nome do projeto>
python3 -m venv <nome da sua venv>
source ./<nome da sua venv>/bin/activate
echo "Django==2.X.Y" > requirements.txt
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```

### Links Relacionados

> https://docs.djangoproject.com/pt-br/2.0/intro/tutorial01
> https://docs.djangoproject.com/pt-br/2.0/topics/
