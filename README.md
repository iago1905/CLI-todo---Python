# CLI todo

Aplicación de línea de comandos para gestionar tareas usando Python y JSON.

## 🚀 Instalación

```bash
git clone https://github.com/tuusuario/cli-todo.git
cd cli-todo
pip install -e .
```

## Uso
# Añadir tarea
todo add -d "Comprar leche"

# Listar todas
todo list

# Listar por estado
todo list -s done
todo list -s todo
todo list -s in-progress

# Actualizar tarea
todo update -i 1 -d "Comprar pan" -s in-progress

# Borrar tarea
todo delete -i 1

