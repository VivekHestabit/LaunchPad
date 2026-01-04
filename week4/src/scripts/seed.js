// const AccountRepository = require('../repositories/account.repository.js');
const mongoose = require('mongoose');
const AccountRepository = require('../repositories/account.repository.js');
const OrderRepository = require('../repositories/order.repository.js');

async function seedDatabase() {
  try {
    await mongoose.connect('mongodb://localhost:27017/week4_db');

    // const acc1 = await AccountRepository.create({
    //   name: 'Alice',
    //   email: 'alice1@test.com',
    //   password: 'password123',
    // });

    // const acc2 = await AccountRepository.create({
    //   name: 'Bob',
    //   email: 'bob2@test.com',
    //   password: 'password123',
    // });

    (async () => {
      const page1 = await AccountRepository.findPaginated({ limit: 2 });
      console.log('Page 1:', page1);

      const cursor = page1[page1.length - 1]._id;

      const page2 = await AccountRepository.findPaginated({
        cursor,
        limit: 2,
      });
      console.log('Page 2:', page2);
    })();

    const acc3 = await AccountRepository.create({
      name: 'Charlie',
      email: 'charlie3@test.com',
      password: 'password123',
    });

    const acc4 = await AccountRepository.create({
      name: 'David',
      email: 'david4@test.com',
      password: 'password123',
    });

    const acc5 = await AccountRepository.create({
      name: 'Emma',
      email: 'emma5@test.com',
      password: 'password123',
    });

    const acc6 = await AccountRepository.create({
      name: 'Sophia',
      email: 'sophia6@test.com',
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
  } catch (err) {
    console.error('Seed failed:', err);
    process.exit(1);
  }
}

seedDatabase();
