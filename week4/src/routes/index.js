const express = require('express');

const ProductRoutes = require('../routes/product.routes');
const router = express.Router();
const RegisterRoutes = require('./User.routes');
const AccountRegister = require('./AccountRegister.routes');

router.use('/products', ProductRoutes);
router.use('/register', RegisterRoutes);
router.use('/Account', AccountRegister);
module.exports = router;
