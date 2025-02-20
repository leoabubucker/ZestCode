import urllib.request
import urllib.error
import sys
import os
import zipfile
import shutil

def download_zip(name):
    # Construct the URL using the provided file name.
    url = f"https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/cpp/{name}.zip"
    print(f"Downloading from: {url}")

    # Set up headers to mimic a browser.
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
    }
    req = urllib.request.Request(url, headers=headers)

    zip_filename = f"{name}.zip"
    try:
        with urllib.request.urlopen(req) as response:
            with open(zip_filename, "wb") as out_file:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    out_file.write(chunk)
    except urllib.error.URLError as e:
        print(f"Error downloading file: {e}")
        return False

    print(f"Downloaded file saved as: {zip_filename}")
    
    # Set extraction path to firmware/libv5rt/sdk relative to the script's location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extract_path = os.path.join(script_dir, "firmware", "libv5rt", "sdk")
    os.makedirs(extract_path, exist_ok=True)

    # Extract the ZIP file manually, removing any common top-level directory.
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            members = zip_ref.namelist()
            # Determine common prefix among all members.
            common_prefix = os.path.commonprefix(members)
            if common_prefix and not common_prefix.endswith('/'):
                common_prefix = common_prefix.rsplit('/', 1)[0] + '/'
            print(f"Common prefix: '{common_prefix}'")
            
            for member in members:
                # Remove the common prefix if it exists.
                member_new = member[len(common_prefix):] if common_prefix and member.startswith(common_prefix) else member
                # Skip entries that result in an empty name.
                if not member_new:
                    continue
                # Determine the full target path.
                target_path = os.path.join(extract_path, member_new)
                # Create directory if the member is a directory.
                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
        print(f"Extracted file contents to: {extract_path}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting ZIP file: {e}")
        return False

    # Delete the zip file after extraction.
    try:
        os.remove(zip_filename)
        print(f"Deleted zip file: {zip_filename}")
    except Exception as e:
        print(f"Error deleting zip file: {e}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_zip.py <filename_without_extension>")
        sys.exit(1)
    file_name = sys.argv[1]
    download_zip(file_name)
