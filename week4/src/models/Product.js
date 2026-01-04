const mongoose = require('mongoose');

const ProdcutSchema = new mongoose.Schema({
  name: String,
  description: String,
  price: Number,
  tags: [String],
  isDeleted: { type: String, default: false },
  deletedAt: { type: Date, default: null },
  createdAt: { type: Date, default: Date.now() },
});

module.exports = mongoose.model('Product', ProdcutSchema);
