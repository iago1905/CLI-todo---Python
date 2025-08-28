import argparse
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timezone

TASK_FILE = Path("bd.json")
STATUS_VALID = {"todo", "in-progress", "done"}


# Consola
def main_cli(argv=None) -> None:

    parser = argparse.ArgumentParser(description="CLI Todo Aplicacion")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Subcomando add
    p = sub.add_parser("add", help="Añadir una nueva tarea")
    p.add_argument("-d", "--desc", type=str, help="Descripción de la tarea")

    # Subcomando list
    p = sub.add_parser("list", help="Listar tareas")
    p.add_argument(
        "--status",
        "-s",
        type=str,
        choices=STATUS_VALID,
        help="Filtrar por estado (todo, in-progress, done)",
    )

    # Subcomando update
    p = sub.add_parser("update", help="Actualizar una tarea")
    p.add_argument("--id", "-i", type=int, help="ID de la tarea a actualizar")
    p.add_argument(
        "--status",
        "-s",
        type=str,
        choices=STATUS_VALID,
        help="Nuevo estado de la tarea (todo, in-progress, done)",
    )
    p.add_argument("--desc", "-d", type=str, help="Nueva descripción de la tarea")

    # Subcomando delete
    delete_parser = sub.add_parser("delete", help="Borrar una tarea")
    delete_parser.add_argument("--id", "-i", type=int, help="ID de la tarea a borrar")

    args = parser.parse_args(argv)
    tasks = loadTasks()

    if args.cmd == "add":
        addTask(tasks, args.desc)
        saveTasks(tasks)
        print("Tarea añadida.")

    elif args.cmd == "update":
        t = returnTask(tasks, args.id)
        if not t:
            print(f"No se encontró tarea con ID {args.id}")
            return
        modifyDesc(t, args.desc) if args.desc else None
        modifyState(t, args.status) if args.status else None
        saveTasks(tasks)

    elif args.cmd == "delete":
        if deleteTask(tasks, args.id):
            saveTasks(tasks)
            print(f"Tarea con ID {args.id} borrada.")
        else:
            print(f"No se encontró tarea con ID {args.id}")

    elif args.cmd == "list":

        if args.status:
            t = returnByState(tasks, args.status)
            printTasks(t)
        else:
            printTasks(tasks)


#####


# Crear json si no existe
def ensurebd(path: Path = TASK_FILE) -> None:
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


# Devolver tareas
def loadTasks(path: Path = TASK_FILE) -> List[Dict[str, Any]]:
    ensurebd()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("El JSON está sin tareas")
        return data
    except Exception as e:
        raise ValueError(f"Archivo JSON error: {e}")


# Guardar tareas  sobra???
def saveTasks(tasks: List[Dict[str, Any]], path: Path = TASK_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# Crear tarea
def addTask(tasks: List[Dict[str, Any]], description: str) -> None:
    """Añade una tarea"""
    task = {
        "id": lastID(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now(timezone.utc).isoformat(),  # No es UTC + 2+
        "updatedAt": datetime.now(timezone.utc).isoformat(),  # No es UTC + 2+
    }
    tasks.append(task)


# Ver ultimo id
def lastID(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1  # El ID maximo + 1


# Devolver tarea por id
def returnTask(tasks: List[Dict[str, Any]], id_task: int) -> Dict[str, Any] | None:
    """Devuelve la tarear por ID"""
    for t in tasks:
        if t["id"] == id_task:
            return t
    return None


# Modificar Estado por ID
def modifyState(task: Dict[str, Any], new_status: str) -> None:
    """Cambiar estado de tarea"""
    if task is None or not isinstance(task, dict):
        raise ValueError("No esta bien seleccionada la tarea")

    if new_status not in STATUS_VALID:
        raise ValueError(f"Estado no valido, debe ser uno de {STATUS_VALID}")

    task["status"] = new_status
    task["updatedAt"] = datetime.now(timezone.utc).isoformat()  # No es UTC + 2


# Modificar Descripcion por ID
def modifyDesc(task: Dict[str, Any], new_desc: str) -> None:
    """Cambiar descripcion de tarea"""
    if task is None or not isinstance(task, dict):
        raise ValueError("No esta bien seleccionada la tarea")

    task["description"] = new_desc
    task["updatedAt"] = datetime.now(timezone.utc).isoformat()  # No es UTC + 2


# Borrar tarea por ID
def deleteTask(tasks: List[Dict[str, Any]], id_task: int) -> bool:
    """Borra task por id"""
    for i, t in enumerate(tasks):
        if t["id"] == id_task:
            del tasks[i]
            return True
    return False


# Listar dones
def returnByState(tasks: List[Dict[str, any]], status: str) -> List[Dict[str, Any]]:
    aux = []
    for t in tasks:
        if t["status"] == status:
            aux.append(t)
    return aux


# Tabla presentacion tareas
def printTasks(tasks: List[Dict[str, Any]]) -> None:
    """Imprime las tareas en formato tabla"""
    if not tasks:
        print("No hay tareas")
        return

    print(
        f"{'ID':<5} {'Description':<30} {'Status':<12} {'Created At':<35} {'Updated At':<35}"
    )
    print("-" * 100)
    for t in tasks:
        created_at = t.get("createdAt", "N/A")
        updated_at = t.get("updatedAt", "N/A")
        print(
            f"{t['id']:<5} {t['description']:<30} {t['status']:<12} {created_at:<5} {updated_at:<35}"
        )


if __name__ == "__main__":
    main_cli()

### Ejemplos de task
# [
#  {
#    "id": 1,
#    "description": "probar save",
#    "status": "done",
#    "updatedAt": "2025-08-27T23:09:24.426868+00:00"
#  },
#  {
#    "id": 2,
#    "description": "probar addTask",
#    "status": "todo",
#    "createdAt": "2025-08-27T23:09:06.081217+00:00",
#    "updatedAt": "2025-08-27T23:09:06.081217+00:00"
#  },
#  {
#    "id": 3,
#    "description": "probar addTask",
#    "status": "todo",
#    "createdAt": "2025-08-27T23:09:24.426868+00:00",
#    "updatedAt": "2025-08-27T23:09:24.426868+00:00"
#  }
# ]
