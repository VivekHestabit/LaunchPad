class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

class BadRequestError extends AppError {
  constructor(message) {
    super(message, 'BAD_REQUEST');
  }
}

module.export = { AppError, BadRequestError };
