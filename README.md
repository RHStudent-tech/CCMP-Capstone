# CCMP-Capstone
Files used in CCMP capstone project
# Serverless Image Resizing Pipeline

## Overview

This project implements a serverless image processing pipeline using AWS Lambda, S3, and IAM. The Lambda function resizes images uploaded to a source S3 bucket and stores the resized versions in a target bucket.

## Components

### 1. `resize_and_upload.py`
- Python Lambda function triggered manually or via API
- Fetches image from `riley-original-images-bucket`
- Resizes to 512x512 thumbnail
- Uploads to `riley-resized-images-bucket` with prefix `resized-`

### 2. `BucketPolicy.json`
- IAM inline policy attached to Lambda role
- Grants:
  - `s3:GetObject` from `riley-original-images-bucket`
  - `s3:PutObject` to `riley-resized-images-bucket`

### 3. `PublicReadBucketPolicy.json`
- S3 bucket policy for `riley-resized-images-bucket`
- Enables public read access to all objects
- Required due to `BucketOwnerEnforced` setting (ACLs disabled)

### 4. `generate_presigned_url.py` (optional)
- Local utility to generate secure, time-limited access to resized images
- Useful for sharing without public bucket access

## Usage

### Trigger Lambda

```json
{
  "bucket": "riley-original-images-bucket",
  "key": "Tyberos.jpeg"
}
