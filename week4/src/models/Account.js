import mongoose from 'mongoose';

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
    firstName: { type: String, required: true, trim: true },
    lastName: { type: String, required: true, trim: true },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },

    password: { type: String, required: true },

    status: { type: String, enum: ['ACTIVE', 'INACTIVE'], default: 'ACTIVE' },

    adresses: [addressSchema],
  },
  { timestamps: true }
);

accountSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

accountSchema.virtual('fullName').get(function () {
  return `${this.firstName} ${this.lastName}`;
});

accountSchema.on('index', (err) => {
  if (err) {
    console.log('Indexed are not created ', err);
  } else {
    console.log('Indexes are created');
  }
});

accountSchema.index({ status: 1, createdAt: -1 });

export default mongoose.model('Account', accountSchema);
