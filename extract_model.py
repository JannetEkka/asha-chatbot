import tarfile
import os

# Specify the exact path to your tar.gz file
file_path = "D:/Projects/asha-chatbot/models/20250420-045926-chewy-assumption.tar.gz"

# Create extraction directory
extract_dir = "D:/Projects/asha-chatbot/src/models/chewy-assumption/"
os.makedirs(extract_dir, exist_ok=True)

# Extract the tar.gz file
with tarfile.open(file_path, "r:gz") as tar:
    tar.extractall(path=extract_dir)

print(f"Model extracted to: {extract_dir}")