import mongoose from 'mongoose';

const ProdcutSchema = new mongoose.Schema({
  name: String,
  description: String,
  price: Number,
  tags: [String],
  isDeletedAt: { type: String, default: false },
  deletedAt: { type: Date, default: null },
  createdAt: { type: Date, default: Date.now() },
});

export default mongoose.model('Product', ProdcutSchema);
