import re
import zipfile
from pathlib import Path

import os

# Create a valid filename from a URL
def sanitize_filename(url):
    """Sanitize URL into a valid filename."""
    filename = re.sub(r'[^a-zA-Z0-9]', '_', url)  # Replace non-alphanumeric chars with '_'
    filename = re.sub(r'_+', '_', filename)  # Remove multiple underscores
    return filename.strip('_')  # Remove trailing underscores


# Create zipfile
def zip_file(url, source_path):
    """Compress a file or directory into a ZIP archive, preserving subdirectory structure."""
    try:
        os.makedirs(source_path, exist_ok=True)
        os.makedirs("reports", exist_ok=True)
        sanitized = sanitize_filename(url)
        zip_path = os.path.join("reports", f"{sanitized}.zip")

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Path not found: {source_path}")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            path = Path(source_path)
            if path.is_dir():
                for file in path.rglob("*"):
                    if file.is_file():
                        zipf.write(file, file.relative_to(path.parent))
            else:
                zipf.write(path, path.name)

        return zip_path
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass
        return None

