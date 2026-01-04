const Product = require('../models/Product.js');

const findProducts = async (query, options) => {
  return Product.find(query).sort(options.sort);
};

const countProducts = async (query) => {
  return Product.countDocuments(query);
};

const softDeleteById = async (id) => {
  return Product.findByIdAndUpdate(id, {
    isDeleted: true,
    deletedAt: new Date(),
  });
};

const ProductRepository = async (data) => {
  return Product.create(data);
};

module.exports = {
  findProducts,
  countProducts,
  softDeleteById,
  ProductRepository,
};
