const { z } = require('zod');

const createUserSchema = z.object({
  name: z.string().min(3),
  email: z.string().email(),
  password: z.string().min(8),
});

const loginUserSchema = z.object({
  email: z.string().email(),
  password: z.string(),
});

const updateUserSchema = z.object({
  name: z.string().min(3).optional(),
  password: z.string().min(8).optional(),
});

module.exports = {
  createUserSchema,
  loginUserSchema,
  updateUserSchema,
};
