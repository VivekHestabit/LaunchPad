const { z } = require('zod');
const sanitizeHtml = require('sanitize-html');

const clean = (val) =>
  sanitizeHtml(val, {
    allowedTags: [],
    allowedAttributes: {},
  });

const createProductSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(3)
      .max(100)
      .transform(clean)
      .refine((val) => val.length >= 3, {
        message: 'Name must be at least 3 characters',
      }),
    description: z.string().trim().max(500).optional(),
    price: z.number().positive(),
    tags: z.array(z.string().trim()).optional(),
  })
  .strict();

const updateProductSchema = z
  .object({
    name: z.string().trim().min(3).max(100).optional(),
    description: z.string().trim().max(500).optional(),
    price: z.number().positive().optional(),
    tags: z.array(z.string().trim()).optional(),
  })
  .strict();

module.exports = {
  createProductSchema,
  updateProductSchema,
};
