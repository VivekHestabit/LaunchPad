const express = require('express');

const router = express.Router();

const users = [
  { id: 1, name: 'vivek' },
  { id: 2, name: 'Vikrant' },
];
router.get('/health', (req, res) => {
  res.json({ status: 'UP', message: 'Backend is health' });
});

router.get('/users', (req, res) => {
  res.status(200).send({ users });
});

router.post('/users', (req, res) => {
  const user = {
    id: users.length + 1,
    name: req.body.name,
  };
  users.push(user);

  res.status(201).json({ message: 'User create Successfully ', user });
});

router.get('/secure-info', (req, res) => {
  res.json({
    protocol: req.protocol,
    host: req.headers.host,
    forwardedProto: req.headers['x-forwarded-proto'] || null,
    message: 'This endpoint will prove HTTS late',
  });
});

module.exports = router;
