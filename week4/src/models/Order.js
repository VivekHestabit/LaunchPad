const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema(
  {
    accountId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Account',
      required: true,
    },
    items: Number,
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

module.exports = mongoose.model('Order', orderSchema);
