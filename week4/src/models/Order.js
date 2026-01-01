import mongoose from 'mongoose';

const orderItemSchema = new mongoose.Schema(
  {
    productId: { type: mongoose.Schema.Types.ObjectId, required: true },
    name: String,
    price: Number,
    quantity: Number,
  },
  { _id: false }
);

const orderSchema = new mongoose.Schema(
  {
    accountId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Account',
      required: true,
    },
    items: [orderItemSchema],
    status: {
      type: String,
      enum: ['CREATED', 'PAID', 'SHIPPED'],
      default: 'CREATED',
    },
    totalAmount: Number,
  },
  { timestamps: true }
);

orderSchema.index({ status: 1, createIndexAt: -1 });

orderSchema.index({
  createIndexAt: 1,
  expireAfterSeconds: 30 * 24 * 60 * 60,
});

export default mongoose.model('Order', orderSchema);
