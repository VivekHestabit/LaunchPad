const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const addressSchema = new mongoose.Schema(
  {
    city: { type: String, required: true },
    state: { type: String },
    country: { type: String, default: 'India' },
    pincode: { type: String },
  },
  { _id: false }
);

const accountSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },
    password: { type: String, required: true, select: false },
    status: { type: String, enum: ['ACTIVE', 'INACTIVE'], default: 'ACTIVE' },
    addresses: [addressSchema],
  },
  { timestamps: true }
);

accountSchema.pre('save', async function () {
  if (!this.isModified('password')) return;
  this.password = await bcrypt.hash(this.password, 10);
});

accountSchema.virtual('fullName').get(function () {
  return this.name || '';
});

accountSchema.index({ status: 1, createdAt: -1 });

module.exports = mongoose.model('Account', accountSchema);
