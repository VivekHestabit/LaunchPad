const { Queue } = require('bullmq');

const emailQueue = new Queue('email-queue', {
  connection: {
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
  },
});

const sendEmailJob = async (data) => {
  await emailQueue.add('send-email', data, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  });
};

module.exports = { sendEmailJob };
