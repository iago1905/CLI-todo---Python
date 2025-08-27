import datetime
import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timezone

TASK_FILE = Path("bd2.json")
STATUS_VALID = {"todo", "in-progress", "done"}


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
def returnByState(tasks: List[Dict[str, any]], status: str) -> List[Dict[str, any]]:
    aux = []
    for t in tasks:
        if t["status"] == status:
            aux.append(t)
    return aux


if __name__ == "__main__":
    tasks = loadTasks()

    tasks.append({"id": 1, "description": "probar save", "status": "todo"})
    addTask(tasks, "probar addTask")
    print(returnTask(tasks, 1))
    modifyState(returnTask(tasks, 1), "done")
    if deleteTask(tasks, 333):
        print("Borrado")
    else:
        print("No borrado")
    print(returnTask(tasks, 1))
    print(returnTask(tasks, 55555))
    print(returnTask(tasks, 2))
    modifyDesc(returnTask(tasks, 55555), "jaime")
    print(returnTask(tasks, 55555))
    print(returnDone(tasks, "done"))
    saveTasks(tasks)
