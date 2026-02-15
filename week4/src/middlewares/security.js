const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const hpp = require('hpp');

const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

const securityMiddlewares = [
  helmet(),
  cors({
    origin: ['http://127.1.0.1:5501'],
    credentials: true,
  }),
  apiLimiter,
  hpp(),
];

module.exports = securityMiddlewares;
