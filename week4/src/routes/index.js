const express = require('express');

const ProductRoutes = require('../routes/product.routes');
const validate = require('../middlewares/validate');
const { createProductSchema } = require('../validations/product.validation');
const router = express.Router();
const RegisterRoutes = require('./Register.routes');

router.use('/products', validate(createProductSchema), ProductRoutes);
router.use('/register', RegisterRoutes);

module.exports = router;
