# Tiny Router
Tiny Router é um roteador de caminhos para aplicações [Flask](https://github.com/pallets/flask). A biblioteca centraliza a definição e gerenciamento das rotas utilizadas na aplicação, criar, editar, remover ou trocar controladores facilmente evitando conflitos.

- [Criando rotas](#criando-rotas)
- [Registrando rotas](#registrando-rotas)
- [Funções Helper](#funções-helper)
    - [Métodos HTTP](#métodos-http)
    - [Préfixos](#préfixos)
- [Dicas de uso](#dicas-de-uso)

## Criando rotas

Uma rota é representada pela classe ```Route```. Ela possui os seguinte atributos:

* **endpoint** - Nome utilizado para identificar a rota. Em caso de endpoints com múltiplos termos, recomendado separá-los por ponto ou sublinhado.
* **rule** - Caminho para um recurso específico
* **view** - Função ou classe que irá manipular a requisição
* **methods** - Métodos HTTP para chamada da rota (Default: ```{'GET'}```)
* **parameters** - Parâmetros que podem ser passados na url.

Ao criar uma rota apenas são obrigatórios ```endpoint```, ```rule``` e ```view```.

Exemplo de uma rota simples:
```python
from tinyrouter import Route
from views import user_index

Route('user.index', '/user', user_index)
```
Por padrão, as rotas são definidas para aceitas apenas o método ```GET```. Entretanto outros métodos podem ser definidos, ou até mais de um.
```python
from tinyrouter import Route
from views import user_index

# Definição dos métodos
methods = ['GET', 'POST']

Route('user.index', '/user', user_index, methods)
```
## Registrando as rotas

Primeiro cria-se uma instância do roteador
```python
from flask import Flask
from tinyrouter import Router

app = Flask(__name__)
router = Router(app)
```

E invoca o método ```register``` passando a lista de rotas que deseja registrar na aplicação
```python
'''
Importaçãoes anteriores
'''
from my_app.routes import routes

'''
 Instância da aplicação e do roteador
'''
router.register(routes)
```

Pronto! As rotas agora estão registradas na aplicação.

É possível registrar vários grupos de rotas.
```python
from webapp.routes import routes as web_routes
from api.routes import routes as api_routes

router.register(web_routes)
router.register(api_routes)
```
Ou ainda...
```python
router.register(web_routes, api_routes)
```

## Funções Helper
### **Métodos HTTP**
Criar uma rota que aceite apenas uma método HTTP utilizando Route fica da seguinte forma:
```python
# Importação da view...
from tinyrouter import Route


Route('cliente.create', '/cliente', cliente_create, ['POST'])
```
Entretanto esse processo pode ser encurtado com os helpers de métodos.
Utilizando os helpers, o exemplo acima ficaria assim:
```python
# Importação da view...
from tinyrouter.helpers import route_post as post

post('cliente.create', '/cliente', cliente_create)
```
O resultado será exatamente o mesmo. Os métodos suportados são:
- GET
- POST
- PUT
- DELETE


### **Préfixos**
Agrupar rotas de acordo com o recurso ou contexto utilizando o Route pode ser um pouco verboso, como por exemplo, rotas associadas ao recurso Cliente.

**[GET] - /cliente/** (Lista todos os Clientes)<br>
**[POST] - /cliente/** (Cria um novo registro de Cliente)<br>
**[GET] - /cliente/{id}** (Recupera um registro específico de Cliente)<br>
**[PUT] - /cliente/{id}** (Atualiza um registro específico de Cliente)<br>
**[DELETE] - /cliente/{id}** (Deleta um registro específico de Cliente )

É possível notar que para cada um dos endpoints foi necessário pôr o nome do recurso (Cliente) como préfixo. Utilizando o helper de préfixo esse trabalho não será mais necessário. A função recebe o préfixo a ser adicionado e as rotas que receberão o mesmo. Exemplo:

```python
# Importação das views
from tinyrouter.helpers import route_prefix as prefix
from tinyrouter.helpers import (route_get as get,\
                                route_post as post,\
                                route_put as put,\
                                route_delete as delete)

*prefix('cliente', 
        get('cliente.all', '/', cliente_all),
        post('cliente.create', '/', cliente_create),
        put('cliente.udpate', '/<id>', cliente_update),
        get('cliente.show'), '/<id>', cliente_show),
        delete('cliente.delete', '/<id>', cliente_delete)
    )
```
NOTA: *Ao utilizar o route_prefix é necessário pôr um * na frente da função pois é retornado uma coleção de rotas alteradas, e este artifício garante que as rotas serão "desempacotadas". Entretanto não impede que as novas rotas sejam armazenadas em uma variável.*

É possível também utilizar aninhamentos do ```route_prefix```
```python
# Importações...

*prefix('sistema', 
    *prefix('cliente',
        ...
    )
)
```
Com isso é possível agrupar diversos contextos com um mesmo préfixo sem a necessidade de definir por extenso um a um.

## Dicas de Uso
1. Utilizar um arquivo de rotas para cada parte da aplicação. Exemplo:
```python
# ./clientes/routes.py
from tinyrouter import Route
from .views

routes = [
    *route_prefix('/cliente',
        Route('cliente.index', '/', views.index),
        Route('cliente.show', '/<int:id>', views.show),
        Route('cliente.create', '/create', views.create, ['GET', 'POST'])
    )
]
```
```python
# ./app.py
from flask import Flask
from tinyrouter import Router
from clientes.routes import routes as rotas_clientes

app = Flask(__name__)
router = Router(app)
router.register(rotas_clientes)
```