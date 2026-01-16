const express = require('express');
const todoRoute = require('./routes/todo');

// This function aggregates all routes
module.exports = () => {
  const app = express.Router();

  // Load the Todo routes
  todoRoute(app);

  return app;
};
