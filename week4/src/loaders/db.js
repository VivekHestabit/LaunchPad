const mongoose = require('mongoose');
const config = require('../config');
const logger = require('../utils/logger');

module.exports = async function conectDB() {
  try {
    await mongoose.connect(config.mongoUri);
    logger.info('Database connected ');
  } catch (err) {
    logger.error('Database connection failed', err);
    process.exit(1);
  }
};
