require('dotenv').config();
const logger = require('./utils/logger');
const connectDB = require('../src/loaders/db');
const createApp = require('./loaders/app');
const config = require('../src/config');

async function startServer() {
  const app = createApp();

  await connectDB();

  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });
  process.on('SIGINT', () => {
    logger.info('Server shutting down...');
    server.close(() => process.exit(0));
  });
}

startServer();
