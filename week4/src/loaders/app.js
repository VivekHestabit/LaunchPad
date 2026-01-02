const express = require('express');
const logger = require('../utils/logger');
require('dotenv').config();

module.exports = function createApp() {
  const app = express();

  // middlewares
  app.use(express.json());
  logger.info('Middlewares loaded');

  // routes (empty for now)
  logger.info('Routes mounted: 0 endpoints');

  return app;
};
