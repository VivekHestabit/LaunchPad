const express = require('express');
const logger = require('../utils/logger');
const routes = require('../routes/index');
const securityMiddlewares = require('../middlewares/security');

require('dotenv').config();

module.exports = function createApp() {
  const app = express();

  app.use(express.json({ limit: '10kb' }));
  securityMiddlewares.map((mw) => app.use(mw));

  logger.info('Middlewares loaded');
  app.use('/api', routes);

  logger.info('Routes mounted: 0 endpoints');

  return app;
};
