const express = require('express');
const validate = require('../middlewares/validate');
const { createProductSchema } = require('../validations/product.validation');

const {
  addProduct,
  getProducts,
  deleteProduct,
} = require('../controllers/product.controller');

const router = express.Router();

router.post('/', validate(createProductSchema), addProduct);
router.get('/', getProducts);
router.delete('/:id', deleteProduct);

module.exports = router;
