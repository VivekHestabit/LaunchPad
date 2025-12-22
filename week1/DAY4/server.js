const express = require('express');
const app = express();
const PORT = 3000;

let counter = 0;

app.get('/ping', (req, res) => {
  const timestamp = new Date().toISOString();
  res.send({ timestamp });
});

app.get('/headers', (req, res) => {
  res.json(req.headers);
});

app.get('/count', (req, res) => {
  counter += 1;
  res.json({ count: counter });
});

app.listen(PORT, () => {
  console.log(`Sever is running on PORT ${PORT}`);
});
