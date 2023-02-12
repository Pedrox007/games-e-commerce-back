# Games E-Commerce
Esse é projeto back-end para uma aplicação de e-commerce de games.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
* Você possui `Python 3.8`
* Você possui `Poetry`
* Você possui `PostgreSQL 14.6`.

## 🚀 Instalando Games E-Commerce

Para instalar o Games E-Commerce, siga estas etapas:

Primeiramente, crie um arquivo `.env` na pasta `games_e_commerce`. Abrindo ele, insira as seguintes variáveis de ambiente substituindo os valores entre `<>` para os seus valores locais:
```
SECRET_KEY=<sua secret_key>
DEBUG=true
DB_NAME=<nome do seu database>
DB_USER=<seu usuario do postgres>
DB_PASSWORD=<sua senha>
DB_HOST=localhost
DB_PORT=5432
FREIGHT_PRICE=<o valor preferível de frete>
```

Após isso, basta rodar o seguinte comando na raiz do projeto para criar a virtual environment:
```
poetry install
```

Uma vez estando na raiz do projeto. Rode o seguinte comando para realizar as migrações:
```
python manage.py migrate
```

Com isso, o projeto está devidamente instalado. Você notará que as migrações iráo criar os produtos constados no arquivo `json` que se encontra em `commercial/statics/data/products.json`. Agora basta rodar o seguinte comando para iniciar o `Django Server`:
```
python manage.py runserver
```

Finalmente o projeto estará rodando no seu [localhost](http://localhost:8000/admin).

## ☕ Usando o Projeto

Após rodar o `Django Server`, para acessar o `Django Admin`, você precisará criar o superusuário. Para isso, basta rodar o seguinte comando:
```
python manage.py createsuperuser
```
Após isso, você irá poder manipular e acessar os dados das tabelas de maneira mais rápida.

O projeto também possui suporte para Swagger Docs. Basta acessar a rota [http://localhost:8000/schema/swagger-ui/](http://localhost:8000/schema/swagger-ui/). Nele você vai ter acesso à todas as rotas da api rest que o projeto possui, junto com cada schema de cada rota. Todas as rotas possuem filtros próprios, onde podem ser visualizados no detalhar da rota do Swagger Docs.

## :checkered_flag: Disposição Finais
O projeto possui testes unitários. Para checa-los basta rodar o comando:
```
python manage.py test
```
