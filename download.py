from time import sleep
import requests
import zipfile
import os
import py7zr

def download_zip(index, download_dir):
    urls = [
        f"https://packs.ppy.sh/S{index}%20-%20osu%21%20Beatmap%20Pack%20%23{index}.zip", 
        f"https://packs.ppy.sh/S{index}%20-%20Beatmap%20Pack%20%23{index}.7z"
    ]
    
    for url in urls:
        try:
            extension = url.split(".")[-1]
            local_filename = os.path.join(download_dir, f"osu_beatmap_pack_{index}.{extension}")
            
            if os.path.exists(local_filename):
                print(f"{local_filename} already exists, skipping download.")
                return local_filename
            
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_filename
        except requests.exceptions.RequestException as e:
            pass
    print(f"Failed to download Beatmap pack {index}: {e}")    
    return None        

def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except zipfile.BadZipFile as e:
        print(f"Failed to extract {zip_path}: {e}")
        return False

def extract_7z(zip_path, extract_to):
    try:
        with py7zr.SevenZipFile(zip_path, mode='r') as z:
            z.extractall(path=extract_to)
        return True
    except Exception as e:
        print(f"Failed to extract {zip_path}: {e}")
        return False

def execute_files(directory):
    is_first_map = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".osz"):
                filepath = os.path.join(root, file)
                try:
                    os.startfile(filepath)
                    if is_first_map:
                        input("Press ENTER to when Osu! is started...")
                        is_first_map = False
                except Exception as e:
                    print(f"Failed to execute {filepath}: {e}")

def delete_zip_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".7z") or file.endswith(".zip"):
                filepath = os.path.join(root, file)
                try:
                    os.remove(filepath)
                    print(f"Deleted {filepath}")
                except Exception as e:
                    print(f"Failed to delete {filepath}: {e}")

if __name__ == "__main__":
    print("This scipt will download and extract all Osu! Beatmap packs\nfrom START_INDEX to END_INDEX to current directory.\nThen when Osu! is opened you need to press ENTER\nto start executing all Osu! map files\n")
    first = int(input("Enter start index of the Osu! Beatmap pack: "))
    last = int(input("Enter end index of the Osu! Beatmap pack: "))

    download_dir = "."

    download_dir = os.path.abspath(download_dir)
    os.makedirs(download_dir, exist_ok=True)

    for index in range(first, last + 1):
        print(f"\nDownloading ZIP file for index {index}...")
        zip_path = download_zip(index, download_dir)
        if zip_path:
            print(f"Extracting ZIP file {zip_path}...")

            extension = zip_path.split(".")[-1]
            if extension == "zip":
                extract_zip(zip_path, download_dir)
            elif extension == "7z":
                extract_7z(zip_path, download_dir)
            else:
                print(f"Error: Bad file extension: {extension}")
            

    print("\nExecuting files...")
    execute_files(download_dir)
    
    print("\nRemoving .ZIP files...")
    delete_zip_files(download_dir)

    input("\nPress any button to quit...")
    quit()