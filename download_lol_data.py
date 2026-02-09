import requests
import os
import json
import sys

# Base URLs for DDragon
DDRAGON_BASE_URL = "https://ddragon.leagueoflegends.com"
DATA_DIR = "data"
CHAMPION_DIR = os.path.join(DATA_DIR, "champions")
ITEM_DIR = os.path.join(DATA_DIR, "items")
CHAMPION_IMAGE_DIR = os.path.join(CHAMPION_DIR, "images")
ITEM_IMAGE_DIR = os.path.join(ITEM_DIR, "images")

def create_directories():
    """Creates necessary directories for storing data."""
    os.makedirs(CHAMPION_DIR, exist_ok=True)
    os.makedirs(ITEM_DIR, exist_ok=True)
    os.makedirs(CHAMPION_IMAGE_DIR, exist_ok=True)
    os.makedirs(ITEM_IMAGE_DIR, exist_ok=True)
    print(f"Created data directories: {DATA_DIR}, {CHAMPION_DIR}, {ITEM_DIR}, {CHAMPION_IMAGE_DIR}, {ITEM_IMAGE_DIR}")

def get_latest_ddragon_version():
    """Fetches the latest DDragon version."""
    versions_url = f"{DDRAGON_BASE_URL}/api/versions.json"
    try:
        response = requests.get(versions_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        versions = response.json()
        latest_version = versions[0]
        print(f"Latest DDragon version: {latest_version}")
        return latest_version
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DDragon version: {e}", file=sys.stderr)
        sys.exit(1)

def download_json_data(url, save_path):
    """Downloads JSON data from a URL and saves it to a file."""
    print(f"Downloading data from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        with open(save_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Saved data to {save_path}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data from {url}: {e}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Error saving data to {save_path}: {e}", file=sys.stderr)
        return None

def download_image(url, save_path, image_filename):
    """Downloads an image from a URL and saves it to a file."""
    print(f"Downloading image: {image_filename}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}", file=sys.stderr)
    except IOError as e:
        print(f"Error saving image to {save_path}: {e}", file=sys.stderr)

def download_and_save_champions(version):
    """Downloads champion metadata and images."""
    champion_data_url = f"{DDRAGON_BASE_URL}/cdn/{version}/data/en_US/champion.json"
    champion_metadata = download_json_data(champion_data_url, os.path.join(CHAMPION_DIR, "champion_metadata.json"))

    if champion_metadata and "data" in champion_metadata:
        for champ_name, champ_info in champion_metadata["data"].items():
            image_filename = champ_info["image"]["full"]
            # Champion images don't use the version in their base URL
            champion_image_url = f"{DDRAGON_BASE_URL}/cdn/{version}/img/champion/{image_filename}"
            image_path = os.path.join(CHAMPION_IMAGE_DIR, image_filename)
            download_image(champion_image_url, image_path, image_filename)
        print("All champion images downloaded.")
    else:
        print("Could not download champion metadata or it's empty.", file=sys.stderr)

def download_and_save_items(version):
    """Downloads item metadata and images."""
    item_data_url = f"{DDRAGON_BASE_URL}/cdn/{version}/data/en_US/item.json"
    item_metadata = download_json_data(item_data_url, os.path.join(ITEM_DIR, "item_metadata.json"))

    if item_metadata and "data" in item_metadata:
        for item_id, item_info in item_metadata["data"].items():
            if "image" in item_info:
                image_filename = item_info["image"]["full"]
                item_image_url = f"{DDRAGON_BASE_URL}/cdn/{version}/img/item/{image_filename}"
                image_path = os.path.join(ITEM_IMAGE_DIR, image_filename)
                download_image(item_image_url, image_path, image_filename)
        print("All item images downloaded.")
    else:
        print("Could not download item metadata or it's empty.", file=sys.stderr)

def main():
    create_directories()
    latest_version = get_latest_ddragon_version()
    if latest_version:
        download_and_save_champions(latest_version)
        download_and_save_items(latest_version)
        print("Data download complete.")
    else:
        print("Failed to get latest DDragon version. Aborting.", file=sys.stderr)

if __name__ == "__main__":
    main()
