import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    print("Received event:", event)

    bucket = event.get('bucket')
    key = event.get('key')

    if not bucket or not key:
        raise ValueError(f"Missing bucket or key. Got bucket={bucket}, key={key}")

    s3 = boto3.client('s3')

    # Step 1: Fetch original image
    try:
        image_obj = s3.get_object(Bucket=bucket, Key=key)
        image_data = image_obj['Body'].read()
        print(f"Fetched image '{key}' from bucket '{bucket}'")
    except Exception as e:
        print(f"Failed to fetch image: {e}")
        raise

    # Step 2: Resize image
    try:
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((128, 128))
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        print("Image resized successfully")
    except Exception as e:
        print(f"Image processing failed: {e}")
        raise

    # Step 3: Upload resized image to target bucket
    resized_key = f"resized-{key}"
    try:
        print(f"Uploading resized image to bucket: 'riley-resized-images-bucket', key: '{resized_key}'")
        response = s3.put_object(
            Bucket='riley-resized-images-bucket',
            Key=resized_key,
            Body=buffer,
            ContentType='image/jpeg'
        )
        print("PutObject response:", response)
    except Exception as e:
        print(f"Failed to upload resized image: {e}")
        raise

    return {
        'status': 'success',
        'resized_key': resized_key
    }