import docker
from datetime import datetime

def save_docker_images(output_folder):
    # Initialize Docker client
    client = docker.from_env()

    try:
        # Get all running containers
        containers = client.containers.list()
        
        if not containers:
            print("No running containers found.")
            return

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for container in containers:
            container_name = container.name
            container_id = container.id
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image_name = f"{container_name}_{timestamp}.tar"
            image_path = os.path.join(output_folder, image_name)

            print(f"Creating image for container: {container_name} ({container_id})")

            # Commit the container to an image
            image = container.commit()

            # Save the image to a tar file
            with open(image_path, 'wb') as image_file:
                for chunk in image.save():
                    image_file.write(chunk)

            print(f"Image saved at: {image_path}")

    except docker.errors.DockerException as e:
        print(f"Error communicating with Docker: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    output_folder = "./docker_images"
    save_docker_images(output_folder)
