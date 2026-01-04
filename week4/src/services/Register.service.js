const User = require('../models/User');
const { getUser } = require('../repositories/user.respository');

async function RegisterUser(data) {
  const user = await User.create({
    name: data.name,
    email: data.email,
    password: data.password,
  });

  return user;
}

async function GetUser(params) {
  return await getUser(params);
}

module.exports = { RegisterUser, GetUser };
