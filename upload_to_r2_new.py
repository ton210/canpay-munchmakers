import os
import boto3
from botocore.client import Config
import mimetypes

def upload_to_r2():
    """Upload optimized images and assets to Cloudflare R2"""
    
    # R2 configuration
    r2_endpoint = 'https://0e6d346a9d941a3a45d02b7fe387cdaf.r2.cloudflarestorage.com'
    access_key = 'a450d3d4b5ecf998466e15ba6a884093'
    secret_key = '7323f180d819d8cf47f8b43c27631543548f0f3b89fc9ac39f9d01994cb72e07'
    bucket_name = 'munchmakers-grinder'
    public_url = 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev'
    
    # Create S3 client configured for R2
    s3_client = boto3.client(
        's3',
        endpoint_url=r2_endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    def upload_file(local_path, remote_path):
        """Upload a single file to R2"""
        try:
            content_type = mimetypes.guess_type(local_path)[0] or 'application/octet-stream'
            
            s3_client.upload_file(
                local_path,
                bucket_name,
                remote_path,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'public, max-age=86400'  # Cache for 24 hours
                }
            )
            print(f"+ Uploaded {remote_path}")
            return True
        except Exception as e:
            print(f"- Failed to upload {remote_path}: {e}")
            return False
    
    # Upload product images
    images_dir = 'website/assets/images/products'
    if os.path.exists(images_dir):
        print("Uploading product images...")
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                local_path = os.path.join(images_dir, filename)
                remote_path = f"images/products/{filename}"
                upload_file(local_path, remote_path)
    
    # Upload CanPay logo
    logo_path = 'website/assets/images/canpay-logo.svg'
    if os.path.exists(logo_path):
        print("Uploading CanPay logo...")
        upload_file(logo_path, 'images/canpay-logo.svg')
    
    # Upload CSS and JS files
    for asset_type in ['css', 'js']:
        asset_dir = f'website/assets/{asset_type}'
        if os.path.exists(asset_dir):
            print(f"Uploading {asset_type} files...")
            for filename in os.listdir(asset_dir):
                local_path = os.path.join(asset_dir, filename)
                remote_path = f"{asset_type}/{filename}"
                upload_file(local_path, remote_path)
    
    print(f"""
Upload complete! 

Your R2 public URL: {public_url}

Next steps:
1. Update image URLs in HTML files to use: {public_url}/images/
2. Test the website with R2 images
3. Deploy the website files

Example image URL: {public_url}/images/products/aluminum-ashtray-black.png
""")

if __name__ == "__main__":
    print("R2 Upload Script")
    print("================")
    print("Uploading CanPay store assets to Cloudflare R2...")
    print()
    
    upload_to_r2()