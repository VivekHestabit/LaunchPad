import logo from './logo.svg';
import './App.css';

function App() {
  console.log('Vivek');

  console.log('vivek1');
  const handleClick = () => {
    fetch('http://localhost:5000/')
      .then((res) => res.json())
      .then((data) => console.log('Data', data))
      .catch((err) => console.log('error', err));
  };
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button style={{ height: '50px', width: '50px' }} onClick={handleClick}>
          Click me
        </button>
      </header>
    </div>
  );
}

export default App;
