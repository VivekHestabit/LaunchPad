const {
  findProducts,
  countProducts,
  softDeleteById,
  ProductRepository,
} = require('../repositories/product.repository.js');
const { BadRequestError } = require('../utils/error.js');

const getProductsService = async (params) => {
  const {
    search,
    minPrice,
    maxPrice,
    tags,
    sort = 'createdAt:desc',
    page = 1,
    isDeleted,
  } = params;

  const query = {};

  if (isDeleted == 'true') {
    query.isDeleted = true;
  }

  if (!isDeleted) query.isDeleted = false;

  if (search) {
    query.$or = [
      { name: { $regex: search, $options: 'i' } },
      { description: { $regex: search, $options: 'i' } },
    ];
  }

  if (minPrice || maxPrice) {
    query.price = {};
    if (minPrice) query.price.$gte = Number(minPrice);
    if (maxPrice) query.price.$lte = Number(maxPrice);
  }

  if (tags) {
    query.tags = { $in: tags.split(',') };
  }

  const [sortField, sortOrder] = sort.split(':');

  const options = {
    sort: { [sortField]: sortOrder === 'desc' ? -1 : 1 },
  };

  const data = await findProducts(query, options);
  const total = await countProducts(query);

  return { data, total, page };
};

const deleteProductService = async (id) => {
  const result = await softDeleteById(id);
  if (!result) throw new BadRequestError('Product not found');
};

const addProdcutService = async (data) => {
  if (!data.name || !data.price) {
    throw new Error('Name or Price not given');
  }
  const ProdcutData = {
    ...data,
    isDeleted: false,
  };
  const product = await ProductRepository(ProdcutData);
  return product;
};

module.exports = {
  getProductsService,
  deleteProductService,
  addProdcutService,
};
