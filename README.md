# CLI todo

Aplicación de línea de comandos para gestionar tareas usando Python y JSON.

## 🚀 Instalación

```bash
git clone https://github.com/tuusuario/cli-todo.git
cd cli-todo
pip install -e .
```
### Recomendacion
Crea y activa un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

## 🔩 Como usarlo 

### Añadir tarea
```bash
> todo add 
      usage: todo add [-h] [-d DESC]
      
      options:
        -h, --help            show this help message and exit
        -d DESC, --desc DESC  Descripción de la tarea
```

### Borrar tarea
```bash
> todo delete -h
        usage: todo delete [-h] [--id ID]
        
        options:
          -h, --help      show this help message and exit
          --id ID, -i ID  ID de la tarea a borrar
```

### Actualizar tarea
```bash
> todo update -h
        usage: todo update [-h] [--id ID] [--status {todo,done,in-progress}] [--desc DESC]
        
        options:
          -h, --help            show this help message and exit
          --id ID, -i ID        ID de la tarea a actualizar
          --status {todo,done,in-progress}, -s {todo,done,in-progress}
                                Nuevo estado de la tarea (todo, in-progress, done)
          --desc DESC, -d DESC  Nueva descripción de la tarea
```

### Actualizar tarea
```bash
> todo list -h
        usage: todo list [-h] [--status {todo,done,in-progress}]
        
        options:
          -h, --help            show this help message and exit
          --status {todo,done,in-progress}, -s {todo,done,in-progress}
```
