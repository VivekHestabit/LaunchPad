const http = require('http');

const PORT = 3001;
const INSTANCE = process.env.INSTANCE_NAME || 'unknown';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      message: 'Response from backend',
      instance: INSTANCE,
    })
  );
});

server.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
