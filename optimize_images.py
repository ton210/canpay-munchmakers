import os
import shutil
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

def optimize_image(input_path, output_path, max_width=800, quality=85):
    """Optimize image by resizing and compressing"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (handles RGBA, P mode, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path, 'PNG', optimize=True, quality=quality)
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_products():
    """Process all product images from source directory"""
    source_dir = r"C:\Users\billi\Green Lunar 2022 Dropbox\Tomer Nahumi\PC\Downloads\CanPayDebit"
    output_dir = r"website\assets\images\products"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    products = {
        "CanPay Aluminum Ashtray": "aluminum-ashtray",
        "CanPay Aluminum Grinders": "aluminum-grinder", 
        "CanPay Joint Case": "joint-case",
        "CanPay Tin Rolling Tray": "rolling-tray"
    }
    
    for product_name, product_id in products.items():
        product_path = os.path.join(source_dir, product_name)
        if not os.path.exists(product_path):
            print(f"Product directory not found: {product_path}")
            continue
            
        print(f"Processing {product_name}...")
        
        for file_name in os.listdir(product_path):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')):
                variant_name = os.path.splitext(file_name)[0].lower()
                variant_name = variant_name.replace(' ', '-').replace('\\', '-')
                
                input_file = os.path.join(product_path, file_name)
                output_file = os.path.join(output_dir, f"{product_id}-{variant_name}.png")
                
                if optimize_image(input_file, output_file):
                    print(f"  + Created {output_file}")
                else:
                    print(f"  - Failed to process {file_name}")

if __name__ == "__main__":
    process_products()
    print("Image optimization complete!")