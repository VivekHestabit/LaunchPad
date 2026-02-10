const AccountService = require('../services/account.service');

class AccountController {
  async create(req, res, next) {
    try {
      const account = await AccountService.createAccount(req.body);
      res.status(201).json(account);
    } catch (error) {
      next(error);
    }
  }

  async getById(req, res, next) {
    try {
      const account = await AccountService.getAccountById(req.params.id);
      res.status(200).json(account);
    } catch (error) {
      next(error);
    }
  }

  async getPaginated(req, res, next) {
    try {
      const { cursor, limit } = req.query;
      const accounts = await AccountService.getAccountsPaginated({
        cursor,
        limit: Number(limit),
      });
      res.status(200).json(accounts);
    } catch (error) {
      next(error);
    }
  }

  async update(req, res, next) {
    try {
      const account = await AccountService.updateAccount(
        req.params.id,
        req.body
      );
      res.status(200).json(account);
    } catch (error) {
      next(error);
    }
  }

  async delete(req, res, next) {
    try {
      await AccountService.deleteAccount(req.params.id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new AccountController();
