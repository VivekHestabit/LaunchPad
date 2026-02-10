const express = require('express');
const AccountController = require('../controllers/account.controller');

const router = express.Router();

router.post('/', AccountController.create);
router.get('/', AccountController.getPaginated);
router.get('/:id', AccountController.getById);
router.put('/:id', AccountController.update);
router.delete('/:id', AccountController.delete);

module.exports = router;
