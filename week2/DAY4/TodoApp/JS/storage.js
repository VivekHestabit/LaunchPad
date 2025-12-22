const Storage_KEY = 'todos';

function saveTodos(todos) {
  localStorage.setItem(Storage_KEY, JSON.stringify(todos));
}

function loadTodos() {
  return JSON.parse(localStorage.getItem(Storage_KEY)) || [];
}
