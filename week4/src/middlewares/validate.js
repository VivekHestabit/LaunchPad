const validate =
  (schema, property = 'body') =>
  (req, res, next) => {
    const result = schema.safeParse(req[property]);

    if (!result.success) {
      return res.status(400).json({
        success: false,
        message: 'Validation error',
        errors: result.error.issues.map((e) => e.message),
      });
    }

    req[property] = result.data;
    next();
  };

module.exports = validate;
