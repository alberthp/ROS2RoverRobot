# ROS2 Installation (Docker) on Raspberry Pi OS 64-bit (Bookworm/Bullseye)

## Docker Installation on Raspberry Pi OS 64-bit (Bookworm/Bullseye)

This README file provides detailed instructions for installing Docker Engine on Raspberry Pi OS 64-bit system. 


> [!IMPORTANT]  
> These instructions are for Docker Engine (command-line interface), not Docker Desktop, which is not compatible with the Raspberry Pi's ARM64 architecture.


### Prerequisites

* A Raspberry Pi 4B running Raspberry Pi OS 64-bit (either Bookworm or Bullseye).
* Terminal access (either directly or via SSH).
* `sudo` privileges.

### Installation Steps

1.  **Update the package list:**

    Refresh the list of available packages from the repositories.

    ```bash
    sudo apt update
    ```  

3.  **Install necessary packages to use the Docker repository:**

    ```bash
    sudo apt install ca-certificates curl gnupg
    ```

    * `ca-certificates`: Allows verification of website authenticity.
    * `curl`: A command-line tool for transferring data.
    * `gnupg`: A tool for data encryption and signing.

4.  **Add Docker's official GPG key:**

    Add Docker's key to the system to verify the authenticity of the packages.

    ```bash
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```
  
5.  **Add the Docker repository to APT:**

    Add the official Docker repository to the system's list of software sources.

    Choose the command corresponding to your Raspberry Pi OS version:

    **For Raspberry Pi OS 12 (Bookworm):**

    ```bash
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      bookworm stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

    **For Raspberry Pi OS 11 (Bullseye):**

    ```bash
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/debian](https://download.docker.com/linux/debian) \
      bullseye stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```


7.  **Update the package list again:**

    Update the package list to include the Docker packages from the newly added repository.

    ```bash
    sudo apt update
    ```

8.  **Install Docker Engine, Docker CLI, containerd.io, and the Docker Compose plugin:**

    ```bash
    sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    ```

    * `docker-ce`: The Docker Community Edition engine.
    * `docker-ce-cli`: The command-line interface for Docker.
    * `containerd.io`: A high-level container runtime.
    * `docker-compose-plugin`: Allows using `docker compose` for multi-container applications.

9.  **Add your user to the `docker` group (recommended for running Docker commands without `sudo`):**

    Replace `$USER` with the actual username if needed, but in most cases, this will add the currently logged-in user.

    ```bash
    sudo usermod -aG docker $USER
    ```

10.  **Apply the group changes:**

    You need to log out of your current session and log back in, or simply reboot your Raspberry Pi for the group changes to take effect.

    ```bash
    sudo reboot
    ```

### Verifying the Installation

After rebooting, open a terminal and run:

```bash
docker run hello-world
```

#### Verify Docker Installation (Quick Check) 

##### Option 1. Check Docker Status:
Open your terminal on the Raspberry Pi and run:

```Bash
sudo systemctl status docker
```
You should see ```Active: active (running)```. If not, you might need to start it with ```sudo systemctl start docker```.

##### Option 2. Test Docker without sudo (Optional but Recommended):

To avoid typing ```sudo``` every time you use Docker, add your user to the docker group:

```Bash
sudo usermod -aG docker $USER
```

You'll need to log out and log back in (or reboot your Pi) for this change to take effect. 
After logging back in, you should be able to run docker ```run hello-world``` without sudo.

## ROS2 Humble Hawksbill with Docker 

This guide sets up a **ROS 2 Humble** environment inside a Docker container on a **Raspberry Pi 4B** running **64-bit Raspberry Pi OS (Bookworm or Bullseye)**.

### Setup decissions
* Requirement: ROS 2 image compiled for the ARM64 architecture, which your Raspberry Pi 4B uses
* Deployment using ROS2 Humble Hawsbill for low layer OS compatiblity at developing time (mid 2025).
* Setup following most standard configuration using the official osrf/ros:humble image.

### Installation steps

1. Clone the Repository
    ```Bash
    git clone https://github.com/yourusername/ros2-docker-raspberrypi.git
    cd ros2-docker-raspberrypi
    ```
2. Pull the ROS 2 Humble Docker Image
     ```Bash
     docker pull osrf/ros:humble
     ```
3. Create the Workspace Directory
   This will be mounted into the container and persist your ROS packages.
    ```Bash
    mkdir -p ros2_docker_ws/src
    ```
4. Run the ROS 2 Humble Container
    ```Bash
    docker run -it \
      --net=host \
      --privileged \
      --name ros2_humble \
      -v $(pwd)/ros2_docker_ws:/root/ros2_ws \
      -v /dev:/dev \
      osrf/ros:humble
    ```
    where, Parameters:
* --net=host: Enables ROS 2 communication over DDS

* --privileged: Grants access to USB, GPIO, etc.

* -v /dev:/dev: Mounts hardware device access

* -v ros2_docker_ws:/root/ros2_ws: Mounts persistent workspace

5. Build the Workspace Inside the Container
    ```Bash
   source /opt/ros/humble/setup.bash
    cd /root/ros2_ws
    colcon build
    source install/setup.bash
    ```
 You, test running ROS 2 nodes, for example: ```ros2 run demo_nodes_cpp talker```

 6. Reboot and restart the Container
     ```Bash
     docker start -ai ros2_humble
    ```
 7. To remove the container
     ```Bash
     docker rm -f ros2_humble
    ```

The repository will then have the following structure:

ros2-docker-raspberrypi/

├── .dockerignore         # Files to exclude from builds (optional)

├── Dockerfile            # Optional custom build (not required)

├── README.md             # This file

└── ros2_docker_ws/       # ROS 2 workspace (shared with container)

    └── src/              # Source packages go here

    
