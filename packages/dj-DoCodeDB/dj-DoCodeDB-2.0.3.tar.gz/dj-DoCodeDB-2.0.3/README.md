# dj-DoCodeDB (Django-App)

[![N|Solid](https://docode.com.mx/img/poweredbydocode.png)](https://docode.com.mx/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

DoCodeDB es una Aplicacion para el manejo en la Base de Datos, implementando una vista de tabla personalizable, asi como la posibilidad de cargar un Spinner(Loader) personalizado pre-configurado.

### Tecnologia

DoCodeDB se implementa con las siguientes librerias previamente instaladas:

* [Django](https://www.djangoproject.com/) - Python base framework (v2.2)
* [docode-managedb](https://pypi.org/project/docode-managebd/) - Libreria para el manejo de base de datos (DoCode)
* [django-sendgrid-v5](https://pypi.org/project/django-sendgrid-v5/) - Libreria para el envio de correos por medio de SendGrid

### Instalacion

DoCodeDB requiere [Python](https://www.python.org/) v3+ para funcionar.

Instalar por medio de [pip](https://pypi.org/project/pip/)

```sh
$ pip install dj-DoCodeDB
```
### Estructura de la App
La aplicacion tiene una estructura comun de una app [Django](https://www.djangoproject.com/)
```sh
DoCodeDB/
	procesos
	static
	templates
	templatetags
	apps.py
	urls.py
	views.py
```

### Configuracion:

Agregar la App a "INSTALLED_APPS" dentro de los **settings.py**
```sh
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DoCodeDB',
]
```

Agregar las urls de **DoCodeDB** a tu archivo de proyecto **urls.py**
```sh
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DoCodeDB.urls')),
]
```

### Uso:

Una vez instalada la App:
-La libreria **dc_form** contiene el metodo **dc_verificarform()** el cual recibe los siguientes parametros:

1. *request* = Metodo de peticion
2. *model* = Modelo que se esta utilizando
3. *None* = Sustituir por template ej. 'Loader.html'

**views.py**
                    
```sh
from DoCodeDB.procesos import dc_form

def mi_vista(request):
 context = {}

 sub_context = dc_form.dc_verificarform(request,model,None)
 context.update(sub_context)

return context
```
Utiliza **context.update()** para actualizar tu contexto actual, ya que la libreria regresa un contexto y este se debe de fusionar con tu contexto


#### Configuracion de Template
Dentro de la App existe un template pre-configurado para manejar los modelos
```sh
datos_tabla.html
```
Solo incluye este modal en la vista que carga el **contexto** para manejar los modulos de la base de datos:

```sh
<!-- Se incluye el template base -->
{% extends 'base.html' %}

<!-- Se agrega en el bloque de contenido la tabla -->
{% block content %}
    {% include 'datos_tabla.html' %}
{% endblock content %}
```

### Configuracion de Template **Personalizado**
La App contiene un template con la configuracion base para implementar una tabla personalizada

```sh
datos_tabla_min.html
base_p_tabla.html
```

**Template Reducido**
La App contiene varios template que dejan fuera las librerias asi como busqueda por encabezado

```sh
base_p_tabla_min.html
```

Dejando fuera las siguientes librerias:
```sh
<!-- JQUERY -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
<!-- Bootstrap -->
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.3/css/responsive.bootstrap4.min.css">
```


#### Uso de template personalizado
Se incluye el template de configuracion base dentro de un **bloque content** para despues agregar la tabla con el **id="table_id"**

```sh
{% block content %}
  {% include 'base_p_tabla.html' %}
  <!-- Tabla Personalizada -->
  <table id="table_id">Mi Tabla</table>
{% endblock content %}
```
La estructura basica de una tabla para funcionar con la APP es la siguiente:

```sh
<!-- TABLA -->
<table id="table_id">
 <thead>
  <tr>
   <th>Folio</th> <!-- Personalizado -->
    {% for campo in campos %}
     <th>{{campo.nombre}}</th>
    {% endfor %}
    <th></th>
  </tr>
 </thead>
 <tbody>
  {% load filtros %} <!-- Cargar los filtrso dentro de la App -->
  {% for registro in registros %}
   <tr>
    <td>{{registro.id}}</td> <!-- Personalizado -->
    {% for dato in registro|contenido:campos %}
     <td>{{dato}}</td>
    {% endfor %}
    <td>
     <div class="row">
      <div class="col-sm-6">
       <button class="boton-editar" type="button" onclick="editar_registro({{registro.id}},'{{object_name}}','{{appname}}')">                      
        Editar
       </button>
      </div>
      <div class="col-6">
       <button class="boton-eliminar" type="button" onclick="eliminar_registro({{registro.id}})">
        Eliminar
       </button>
      </div>
     </div>
    </td>
   </tr>
  {% endfor %}
 </tbody>
</table>
<!-- TABLA -->
```

-Se obtienen los campos del modelo:
```sh
{% for campo in campos %}
	<th>{{campo.nombre}}</th>
{% endfor %}
```

-Se Carga los filtros y se obtienen los registros del modelo:
```sh
{% load filtros %} 
{% for registro in registros %}
```
-Se asignan los datos en base a los campos del modelo:
```sh
{% for dato in registro|contenido:campos %}
	<td>{{dato}}</td>
{% endfor %}
```

### Envio de Correo (SendGrid)
La aplicacion contienen un configuracion para enviar correos por medio de de SendGrid (django-sendgrid-v5) una vez instalada se puede proceder a configurar

#### Configruracion SendGrid
Agregamos las siguientes lineas en el archivo de settings

**settings.py**
```sh
# <=================== EMAIL CONFIGURATION =============>
ENVIAR_CORREO = True
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = ""
#Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# <=================== EMAIL CONFIGURATION =============>
```

**Modelo Tsendgrid**
Dentro del panel administrativo en el modelo **Tsendgrids** colocar la **key** proporcionada por SendGrid


Importar el metodo desde la aplicacion para ser utilizado, entre los parametros **template** es el template de correo a ser enviado, para este template se le agregara como contexto la informacion dentro de **info[]**

```sh
import DoCodeDB.procesos.correo_sendGrid as _correo

info = [
  ('origen', "MiCorreo"),
  ('nombre', nombre),
  ('telefono', telefono),
  ('correo', correo),
  ('mensaje', mensaje),
]
# PARAMETROS ==> (origen,correo_enviar,cc,info,template)
if not _correo.enviar_correo('origen@email.com','destino@email.com',None,info,'correo_form.html'):
  print('Correo no enviado')
```

La plataforma contiene un template base para envio de correo, pero se puede personalizar uno propio

**correo_form.html**
```sh
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <h2>Correo de contacto para la plataforma {{origen}}</h2>
    <p>Usuario: {{nombre}}</p>
    <p>Telefono: {{telefono}}</p>
    <p>Correo: {{correo}}</p>
    <p>Mensaje: {{mensaje}}</p>
  </body>
</html>
```


#### Actualizacion v1.2

- Se retiran botones para el template 'datos_tabla.html'
- Se retira titulo por default en modales 'datos_tabla.html' y 'base_p_tabla.html'

#### Actualizacion v1.4

- Proceso para aceptar modelos con 'IntegerField'
- Se implementa FontAwesome, para no mostrar botones en los reportes

#### Actualizacion v1.5

- Manejo de multiples formularios creados por usuarios

#### Actualizacion v1.6

- Acepta modelos con atributos Integer
- Se ajusta llamada de metodos editar y eliminar para funcionar en paginacion de tablas
- Procurar agregar los metodos __str__ y __unicode__ dentro de los modelos

#### Actualizacion v1.8

- Se implementa el envio de formularios por medio de correo utilizando [SendGrid](https://sendgrid.com/)
- Se agrega template reducido para moviles **datos_tabla_min.html**

#### Actualizacion v1.9

- Se implementa el uso de ImageField para los modelos en [Django](https://www.djangoproject.com/) - Python base framework (v2.2)

#### Actualizacion v2.0.0

- Para esta version se realizan ajustes en los modales al momento de utilizar las tablas personalizadas, modelales como "nuevo" y "editar"

#### Actualizacion v2.0.1

- Se repara error de id duplicados en el DOM al momento de utilizar "FileField"

#### Actualizacion v2.0.2

- Se nombra la seccion de archivos "FileSection" y "FileSection_editar"

#### Actualizacion v2.0.3

- Ahora se regresa el registro que se agrega o se edita en el sub_context


Licencia
----
MIT License

Copyright (c) 2019 DoCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.