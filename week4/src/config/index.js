const path = require('path');
const dotenv = require('dotenv');
const env = process.env.NODE_ENV || 'local';

dotenv.config({
  path: path.resolve(process.cwd(), `.env.${env}`),
});

module.exports = {
  env,
  port: process.env.PORT,
  mongoUri: process.env.MONGO_URI,
};
