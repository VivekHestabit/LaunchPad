module.exports = {
  apps: [
    {
      name: 'backend-api',
      script: 'server.js',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'local',
        MONGO_URI: 'mongodb://127.0.0.1:27017/week4_db',
        PORT: 3005,
      },
    },
    {
      name: 'email-worker',
      script: 'jobs/worker.job.js',
      instances: '1',
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'local',
      },
    },
  ],
};
