import mongoose from 'mongoose';
import AccountRepository from '../repositories/account.repository.js';
import OrderRepository from '../repositories/order.repository.js';

await mongoose.connect('mongodb://localhost:27017/week4_db');

const acc1 = await AccountRepository.create({
  name: 'Alice',
  email: 'alice1@test.com',
  password: 'password123',
});

const acc2 = await AccountRepository.create({
  name: 'Bob',
  email: 'bob2@test.com',
  password: 'password123',
});

await OrderRepository.create({
  accountId: acc1._id,
  amount: 500,
  status: 'completed',
  deliveredAt: new Date(),
});

await OrderRepository.create({
  accountId: acc1._id,
  amount: 300,
});

await OrderRepository.create({
  accountId: acc2._id,
  amount: 900,
  status: 'completed',
  deliveredAt: new Date(),
});

console.log('Seed data inserted');
process.exit(0);
