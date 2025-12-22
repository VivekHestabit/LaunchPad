const inpt = document.getElementById('input');
const addbtn = document.getElementById('Addbtn');
const list = document.getElementById('todolist');

let todos = loadTodos();

function RenderTodos() {
  list.innerHTML = '';
  todos.forEach((todo, index) => {
    const li = document.createElement('li');

    li.innerHTML = `
         <span>${todo.text}</span>
         <button onclick="editTodo(${index})">Edit</button>
         <button onclick="DeleteTodo(${index})">Delete</button>
        `;

    list.appendChild(li);
  });
  saveTodos(todos);
}

function addTodos(input) {
  if (!inpt.value.trim()) {
    return;
  }
  todos.push({ text: inpt.value });
  inpt.value = '';
  RenderTodos();
}

function DeleteTodo(index) {
  todos.splice(index, 1);
  RenderTodos();
}

function editTodo(index) {
  const Newtxt = prompt('Edit todo : ', todos[index].text);
  if (Newtxt !== null) {
    todos[index].text = Newtxt;
    RenderTodos();
  }
}

addbtn.addEventListener('click', () => {
  addTodos();
});

RenderTodos();
