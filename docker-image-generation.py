import os
import subprocess
import tarfile
from pathlib import Path

def get_docker_containers():
    """Retrieve the list of running Docker containers."""
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.ID}}"], capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().split("\n")
        return container_ids if container_ids != [''] else []
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Docker containers: {e}")
        return []

def create_docker_image(container_id, output_folder):
    """Create an image of the Docker container and save it as a tar file."""
    try:
        image_name = f"backup_{container_id}"
        tar_file_path = Path(output_folder) / f"{image_name}.tar"

        # Commit the container to an image
        subprocess.run(["docker", "commit", container_id, image_name], check=True)

        # Save the image to a tar file
        with tarfile.open(tar_file_path, "w") as tar:
            subprocess.run(["docker", "save", "-o", str(tar_file_path), image_name], check=True)

        print(f"Image for container {container_id} saved to {tar_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating image for container {container_id}: {e}")

def main():
    output_folder = "docker_images"

    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Retrieve running Docker containers
    containers = get_docker_containers()
    if not containers:
        print("No running Docker containers found.")
        return

    total_containers = len(containers)
    print(f"Found {total_containers} running Docker container(s).")

    # Create and save images for each container
    for index, container_id in enumerate(containers, start=1):
        print(f"Processing container {index}/{total_containers} (ID: {container_id})...")
        create_docker_image(container_id, output_folder)
        progress = (index / total_containers) * 100
        print(f"Progress: {progress:.2f}%")

    print("All Docker containers have been processed.")

if __name__ == "__main__":
    main()
import os
import subprocess
import tarfile
from pathlib import Path

def get_docker_containers():
    """Retrieve the list of running Docker containers."""
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.ID}}"], capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().split("\n")
        return container_ids if container_ids != [''] else []
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Docker containers: {e}")
        return []

def create_docker_image(container_id, output_folder):
    """Create an image of the Docker container and save it as a tar file."""
    try:
        image_name = f"backup_{container_id}"
        tar_file_path = Path(output_folder) / f"{image_name}.tar"

        # Commit the container to an image
        subprocess.run(["docker", "commit", container_id, image_name], check=True)

        # Save the image to a tar file
        with tarfile.open(tar_file_path, "w") as tar:
            subprocess.run(["docker", "save", "-o", str(tar_file_path), image_name], check=True)

        print(f"Image for container {container_id} saved to {tar_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating image for container {container_id}: {e}")

def main():
    output_folder = "docker_images"

    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Retrieve running Docker containers
    containers = get_docker_containers()
    if not containers:
        print("No running Docker containers found.")
        return

    total_containers = len(containers)
    print(f"Found {total_containers} running Docker container(s).")

    # Create and save images for each container
    for index, container_id in enumerate(containers, start=1):
        print(f"Processing container {index}/{total_containers} (ID: {container_id})...")
        create_docker_image(container_id, output_folder)
        progress = (index / total_containers) * 100
        print(f"Progress: {progress:.2f}%")

    print("All Docker containers have been processed.")

if __name__ == "__main__":
    main()
