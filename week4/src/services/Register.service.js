const User = require('../models/User');
const { getUser } = require('../repositories/user.respository');
const { sendEmailJob } = require('../jobs/email.job');
const logger = require('../utils/logger');

async function RegisterUser(data, requestId) {
  logger.info('User registration started');
  const user = await User.create({
    name: data.name,
    email: data.email,
    password: data.password,
  });
  logger.info('user Added to DB : ');

  await sendEmailJob({
    email: user.email,
    name: user.name,
    type: 'WELCOME_EMAIL',
  });

  logger.info('Send email job added to queue', { requestId });

  return user;
}

async function GetUser(params) {
  return await getUser(params);
}

module.exports = { RegisterUser, GetUser };
