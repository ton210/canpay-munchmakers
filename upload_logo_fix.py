#!/usr/bin/env python3
"""
Upload the fixed CanPay logo to R2
"""

import boto3
from botocore.client import Config

def upload_logo():
    """Upload the corrected logo to R2"""
    
    # R2 configuration
    r2_endpoint = 'https://0e6d346a9d941a3a45d02b7fe387cdaf.r2.cloudflarestorage.com'
    access_key = 'a450d3d4b5ecf998466e15ba6a884093'
    secret_key = '7323f180d819d8cf47f8b43c27631543548f0f3b89fc9ac39f9d01994cb72e07'
    bucket_name = 'munchmakers-grinder'
    
    # Create S3 client configured for R2
    s3_client = boto3.client(
        's3',
        endpoint_url=r2_endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    
    try:
        # Upload the corrected logo
        logo_path = 'website/assets/images/canpay-logo.svg'
        s3_client.upload_file(
            logo_path,
            bucket_name,
            'images/canpay-logo.svg',
            ExtraArgs={
                'ContentType': 'image/svg+xml',
                'CacheControl': 'public, max-age=86400'
            }
        )
        
        print("Logo uploaded successfully!")
        print("CDN URL: https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev/images/canpay-logo.svg")
        
    except Exception as e:
        print(f"Error uploading logo: {e}")

if __name__ == "__main__":
    upload_logo()