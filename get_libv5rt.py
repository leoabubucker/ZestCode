import urllib.request
import urllib.error
import json
import sys
import os
import zipfile
import shutil

def fetch_manifest(manifest_url):
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
    }
    req = urllib.request.Request(manifest_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            manifest = json.loads(data)
            return manifest
    except Exception as e:
        print(f"Error fetching manifest: {e}")
        sys.exit(1)

def download_zip(file_name):
    # Construct the URL using the file name from the manifest.
    url = f"https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/cpp/{file_name}.zip"
    print(f"Downloading from: {url}")

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
    }
    req = urllib.request.Request(url, headers=headers)

    zip_filename = f"{file_name}.zip"
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
        sys.exit(1)

    print(f"Downloaded file saved as: {zip_filename}")
    return zip_filename

def extract_zip(zip_filename):
    # Set extraction path to firmware/libv5rt/sdk relative to the script's location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extract_path = os.path.join(script_dir, "firmware", "libv5rt", "sdk")
    os.makedirs(extract_path, exist_ok=True)

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
                if not member_new:
                    continue
                target_path = os.path.join(extract_path, member_new)
                if member.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
        print(f"Extracted file contents to: {extract_path}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting ZIP file: {e}")
        sys.exit(1)

def main():
    manifest_url = "https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/cpp/manifest.json"
    manifest = fetch_manifest(manifest_url)
    
    if "latest" not in manifest:
        print("Manifest does not contain 'latest' field.")
        sys.exit(1)
    
    latest_version = manifest["latest"]
    print(f"Latest version from manifest: {latest_version}")
    
    zip_file = download_zip(latest_version)
    extract_zip(zip_file)
    
    try:
        os.remove(zip_file)
        print(f"Deleted zip file: {zip_file}")
    except Exception as e:
        print(f"Error deleting zip file: {e}")

if __name__ == "__main__":
    main()
