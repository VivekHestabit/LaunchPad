const express = require('express');
const { addUser } = require('../controllers/product.controller');
const { getUser } = require('../controllers/product.controller');
const validate = require('../middlewares/validate');
const { createUserSchema } = require('../validations/user.validation');

const router = express.Router();

router.post('/', validate(createUserSchema), addUser);
router.get('/', getUser);

module.exports = router;
