require('dotenv').config();
const config = require('./config');
const logger = require('./utils/logger');
const connectDB = require('./loaders/db');
const createApp = require('./loaders/app');

async function startServer() {
  const app = createApp();

  await connectDB();

  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });

  // graceful shutdown
  process.on('SIGINT', () => {
    logger.info('Server shutting down...');
    server.close(() => process.exit(0));
  });
}

startServer();
