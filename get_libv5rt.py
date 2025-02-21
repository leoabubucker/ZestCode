import urllib.request
import urllib.error
import json
import sys
import os
import zipfile
import shutil

MANIFEST_URL = "https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/cpp/manifest.json"

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
    except urllib.error.URLError:
        print("No internet connection detected. Proceeding without online version check.")
        return None
    except Exception as e:
        print(f"Error fetching manifest: {e}")
        sys.exit(1)

def download_zip(file_name):
    # Construct the URL using the version passed (in its original format).
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
        raise e

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

def version_tuple(version_str):
    """Converts a version string like '20240802.15.00.00' to a tuple of integers."""
    try:
        return tuple(map(int, version_str.split('.')))
    except Exception:
        return ()

def main():
    # Expect a version argument passed on the command line.
    if len(sys.argv) < 2:
        print("Usage: script.py <version>")
        sys.exit(1)
    
    # The version should be in the format "V5_20240802_15_00_00"
    passed_version = sys.argv[1]
    # Normalize the version (remove "V5_" and convert underscores to dots)
    normalized_passed = passed_version.replace("V5_", "").replace("_", ".")
    print(f"Using version: {passed_version} (normalized: {normalized_passed})")
    
    # Attempt to fetch the online manifest to check for a later version.
    manifest = fetch_manifest(MANIFEST_URL)
    if manifest and "latest" in manifest:
        online_version_raw = manifest["latest"]
        normalized_online = online_version_raw.replace("V5_", "").replace("_", ".")
        # Compare version tuples
        if version_tuple(normalized_online) > version_tuple(normalized_passed):
            print(f"WARNING: A later SDK version is available online: {online_version_raw} "
                  f"(normalized: {normalized_online}) compared to the specified version {passed_version}.")
    
    # Determine the SDK installation directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sdk_dir = os.path.join(script_dir, "firmware", "libv5rt", "sdk")
    
    # If the SDK directory exists, check its version.
    if os.path.exists(sdk_dir):
        local_manifest_path = os.path.join(sdk_dir, "manifest.json")
        if os.path.exists(local_manifest_path):
            try:
                with open(local_manifest_path, "r") as f:
                    local_manifest = json.load(f)
                local_version = local_manifest.get("version", "")
                if local_version == normalized_passed:
                    print("SDK is already at the specified version. No update is necessary.")
                    sys.exit(0)
                else:
                    print(f"Local SDK version ({local_version}) differs from specified version. Deleting old installation...")
                    shutil.rmtree(sdk_dir)
            except Exception as e:
                print(f"Error reading local manifest: {e}. Removing SDK directory.")
                shutil.rmtree(sdk_dir)
        else:
            print("SDK directory exists but manifest.json not found. Removing directory.")
            shutil.rmtree(sdk_dir)
    
    # Attempt to download the SDK zip using the passed version.
    try:
        zip_file = download_zip(passed_version)
    except urllib.error.URLError as e:
        if os.path.exists(sdk_dir):
            print("No internet available. Using the existing SDK as the latest version.")
            sys.exit(0)
        else:
            print("No internet available and no local SDK is installed. Cannot proceed.")
            sys.exit(1)
    
    extract_zip(zip_file)
    
    try:
        os.remove(zip_file)
        print(f"Deleted zip file: {zip_file}")
    except Exception as e:
        print(f"Error deleting zip file: {e}")

if __name__ == "__main__":
    main()
