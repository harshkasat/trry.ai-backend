import re
import zipfile
from pathlib import Path
from typing import Optional

import os

# Create a valid filename from a URL
def sanitize_filename(url):
    """Sanitize URL into a valid filename."""
    filename = re.sub(r'[^a-zA-Z0-9]', '_', url)  # Replace non-alphanumeric chars with '_'
    filename = re.sub(r'_+', '_', filename)  # Remove multiple underscores
    return filename.strip('_')  # Remove trailing underscores


# Create zipfile
def zip_file(main_dir: Optional[str] = 'reports', output_zip:Optional[str] = 'reports.zip'):
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(main_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Create relative path starting from main directory
                    arcname = os.path.relpath(file_path, start=os.path.dirname(main_dir))
                    zipf.write(file_path, arcname)

        print(f"ZIP archive created sucessfully : {output_zip}")
        return output_zip
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
        if os.path.exists(main_dir):
            try:
                os.remove(main_dir)
            except:
                pass
        return None

