import Account from '../models/Account.js';

class AccountRepository {
  async create(data) {
    return Account.create(data);
  }
  async findById(id) {
    return Account.findById(id);
  }

  async findPaginated({ cursor, limit = 10 }) {
    const query = cursor ? { _id: { $lt: cursor } } : {};
    return Account.find(query).sort({ _id: -1 }).limit(10);
  }
  async update(id, data) {
    return Account.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }
  async delete(id) {
    return Account.findByIdAnddelete(id);
  }
}

export default AccountRepository();
