module.exports = {
  apps: [
    {
      name: 'backend-api',
      script: 'server.js',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'local',
      },
    },
  ],
};
