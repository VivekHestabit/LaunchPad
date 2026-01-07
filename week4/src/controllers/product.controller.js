const {
  getProductsService,
  deleteProductService,
  addProdcutService,
} = require('../services/product.service.js');
const { RegisterUser } = require('../services/Register.service.js');
const { GetUser } = require('../services/Register.service.js');

const getProducts = async (req, res, next) => {
  try {
    const result = await getProductsService(req.query);
    res.json({ success: true, ...result });
  } catch (err) {
    next(err);
  }
};

const deleteProduct = async (req, res, next) => {
  try {
    await deleteProductService(req.params.id);
    res.json({ success: true, message: 'Product soft-deleted' });
  } catch (err) {
    next(err);
  }
};

const addProduct = async (req, res, next) => {
  try {
    await addProdcutService(req.body);
    res.json({ success: true, message: 'Product Added successfully!' });
  } catch (err) {
    next(err);
  }
};

const addUser = async (req, res, next) => {
  try {
    await RegisterUser(req.body, req.requestId);
    res
      .status(201)
      .json({ success: true, message: 'User Registered Successfully !' });
  } catch (err) {
    next(err);
  }
};

const getUser = async (req, res, next) => {
  try {
    const user = await GetUser(req.query);
    res
      .status(200)
      .json({ success: true, message: 'User List fetched !!', user: user });
  } catch (err) {
    next(err);
  }
};

module.exports = {
  getProducts,
  deleteProduct,
  addProduct,
  addUser,
  getUser,
};
