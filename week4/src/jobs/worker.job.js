const { Worker } = require('bullmq');

const worker = new Worker(
  'email-queue',
  async (job) => {
    console.log('Job type:', job.data.type);
    console.log('Sending email to:', job.data.email);

    await new Promise((res) => setTimeout(res, 3000));

    console.log('Email sent successfully');
  },
  {
    connection: {
      host: process.env.REDIS_HOST,
      port: process.env.REDIS_PORT,
    },
  }
);
