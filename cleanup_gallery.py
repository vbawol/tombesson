import json
import os

# Load the JSON data
with open('photoapp/data.json', 'r') as f:
    data = json.load(f)

# Extract image filenames from JSON
json_images = set(item['image'] for item in data)

# List files in gallery folder
gallery_path = 'images/gallery'
gallery_files = set(os.listdir(gallery_path))

# Find files in gallery not in JSON
to_remove = gallery_files - json_images

print("Images in gallery not in JSON:")
for img in sorted(to_remove):
    print(img)

# Remove them
for img in to_remove:
    os.remove(os.path.join(gallery_path, img))
    print(f"Removed: {img}")

print(f"Removed {len(to_remove)} images.")