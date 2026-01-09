const http = require('http');

const server = http.createServer((req, res) => {
  console.log('Request received');
  res.end('Hello from container');
});

server.listen(3000, () => {
  console.log('Server started on port 3000');
});
