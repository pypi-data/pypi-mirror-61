# docode-managebd

[![N|Solid](https://docode.com.mx/img/poweredbydocode.png)](https://docode.com.mx/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

docode-managebd es una libreria para manejar los procesos de la base de datos utlizando el framework Django==2.X

### Tecnologia

docode-managebd se implementa con las siguientes tecnologias:

* [Django](https://www.djangoproject.com/) - Python base framework!

### Instalacion

docode-managebd requiere [Python](https://www.python.org/) v3+ para funcionar.

Instalar por medio de [pip](https://pypi.org/project/pip/)

```sh
$ pip install docode-managebd
```

### Uso:

Una vez instalada la libreria en el entorno virtual

Importar la libreria en [Python](https://www.python.org/):
```sh
import docode_managebd.procesos_bd as proc
```

#### Metodos:

Una vez que se realiza el import se pueden utilizar los metodos de la libreria

```sh
proc.obtener_campos(modelo)
```
```sh
proc.verificar_formulario(request,modelo)
```
```sh
proc.alta_registro(request,modelo)
```
```sh
proc.eliminar_registro(request,modelo)
```
```sh
proc.editar_registro(request,modelo)
```
```sh
proc.modal_editar(id,modelo):
```


#### Configuracion de Template
Puedes utlizar tus propios templates con un <input> oculto para identificar que tipo es:
[tipo] = ('nuevo', 'eliminar', 'editar')
```sh
<input class="d-none" type="text" name="idForm" value="[tipo]">
```
Por cada formulario envia el [id] del registro para su proceso solamente para eliminar y editar.

Eliminar:
```sh
<input id="idEliminar" class="d-none" type="text" name="idEliminar" value="">
```
Editar:
```sh
<input id="idEditar" class="d-none" type="text" name="idEditar" value="">
```

### Versiones

**Version 0.0.5:** Se implementa el uso de campos FileFiled para los modelos

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