const AccountRepository = require('../repositories/account.repository');
const { BadRequestError } = require('../utils/error');

class AccountService {
  async createAccount(data) {
    if (!data.email || !data.password || !data.name) {
      throw new BadRequestError('Required fields are missing');
    }

    return AccountRepository.create(data);
  }

  async getAccountById(id) {
    const account = await AccountRepository.findById(id);
    if (!account) {
      throw new BadRequestError('Account not found');
    }
    return account;
  }

  async getAccountsPaginated(params) {
    return AccountRepository.findPaginated(params);
  }

  async updateAccount(id, data) {
    const updatedAccount = await AccountRepository.update(id, data);
    if (!updatedAccount) {
      throw new BadRequestError('Account not found');
    }
    return updatedAccount;
  }

  async deleteAccount(id) {
    const deletedAccount = await AccountRepository.delete(id);
    if (!deletedAccount) {
      throw new BadRequestError('Account not found');
    }
    return deletedAccount;
  }
}

module.exports = new AccountService();
