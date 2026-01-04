export const errorMiddleware = (err, req, res, next) => {
  res.status(400).json({
    success: false,
    message: err.message || 'Something went wrong',
    code: err.code || 'INTERNAL_ERROR',
    timestamp: new Date().toISOString(),
    path: req.originalUrl,
  });
};
