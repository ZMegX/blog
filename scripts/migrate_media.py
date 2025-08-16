import os
import django
import cloudinary.uploader
import sys
from pathlib import Path

# ---------------------------
# Setup Django
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings') 

django.setup()

from blog.models import Post 

# ---------------------------
# Loop through all posts
# ---------------------------
for post in Post.objects.all():
    # Skip if no image
    if not post.image:
        continue

    # Skip if already a Cloudinary URL
    if post.image.url.startswith("http"):
        print(f"Skipping {post.title}, already uploaded.")
        continue

    # Handle Windows or Linux paths
    image_path = Path(post.image.path)
    if not image_path.exists():
        print(f"File does not exist: {image_path}")
        continue

    print(f"Uploading {image_path} ...")
    
    try:
        upload_result = cloudinary.uploader.upload(
            str(image_path),  # convert Path to str
            folder="posts/"   # optional folder in Cloudinary
        )
        # Update image field to the new Cloudinary URL
        post.image = upload_result["secure_url"]
        post.save()
        print(f"Saved {post.title} -> {post.image.url}")

    except Exception as e:
        print(f"Error uploading {post.title}: {e}")

print("Migration complete!")
