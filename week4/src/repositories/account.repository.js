const Account = require('../models/Account.js');

class AccountRepository {
  async create(data) {
    return Account.create(data);
  }
  async findById(id) {
    return Account.findById(id);
  }

  async findPaginated({ cursor, limit = 10 } = {}) {
    const query = cursor ? { _id: { $lt: cursor } } : {};
    return Account.find(query).sort({ _id: -1 }).limit(limit);
  }
  async update(id, data) {
    return Account.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }
  async delete(id) {
    return Account.findByIdAndDelete(id);
  }
}

module.exports = new AccountRepository();
