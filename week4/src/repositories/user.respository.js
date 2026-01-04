const userModel = require('../models/User');

const User = async (data) => {
  return userModel.create(data);
};

const getUser = async (query) => {
  return userModel.find(query);
};

module.exports = { User, getUser };
