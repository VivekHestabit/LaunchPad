// Root module orchestrating all components

module "raw_s3" {
  source = "./modules/s3/raw"
  bucket_name = "${var.environment}-${var.aws_region}-raw-data"
  tags        = var.tags
}

module "processed_s3" {
  source = "./modules/s3/processed"
  bucket_name = "${var.environment}-${var.aws_region}-processed-data"
  tags        = var.tags
}

module "ingestion_queue" {
  source = "./modules/sqs/ingestion"
  queue_name = "${var.environment}-ingest-queue"
  tags        = var.tags
}

module "api_gateway" {
  source     = "./modules/api_gateway"
  api_name   = "${var.environment}-api"
  lambda_arn = module.ingestion_lambda.lambda_arn
  tags       = var.tags
}

module "ingestion_lambda" {
  source           = "./modules/lambda/ingestion"
  function_name    = "${var.environment}-ingest"
  handler          = "handler.lambda_handler"
  runtime          = "python3.11"
  role_name        = "${var.environment}-ingest-role"
  sqs_queue_url    = module.ingestion_queue.queue_url
  tags             = var.tags
}

module "step_function" {
  source          = "./modules/stepfunctions/etl"
  name            = "${var.environment}-etl"
  state_machine_arn = module.etl_state_machine.arn
  tags            = var.tags
}

module "athena_workgroup" {
  source       = "./modules/athena/workgroup"
  name         = "${var.environment}-athena"
  s3_output    = module.processed_s3.bucket_arn
  tags         = var.tags
}

// Outputs
output "api_invoke_url" {
  description = "API Gateway Invoke URL"
  value       = module.api_gateway.invoke_url
}
output "s3_raw_bucket" {
  description = "Raw S3 Bucket ARN"
  value       = module.raw_s3.bucket_arn
}
output "s3_processed_bucket" {
  description = "Processed S3 Bucket ARN"
  value       = module.processed_s3.bucket_arn
}
