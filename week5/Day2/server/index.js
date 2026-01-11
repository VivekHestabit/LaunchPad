const express = require('express');
const mongoose = require('mongoose');

const app = express();

app.use(express.json());

mongoose
  .connect('mongodb://mongo:27017/day2db')
  .then(() => console.log('mongoDB connected'))
  .catch((err) => console.log('Error : ', err));

app.get('/', (req, res) => {
  res.json({ message: 'Hellow from backend docker ' });
});

app.listen(5000, () => {
  console.log('Server running on PORT : 5000');
});
