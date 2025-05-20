# ROS2 Installation (Docker) on Raspberry Pi OS 64-bit (Bookworm/Bullseye)

## Docker Installation on Raspberry Pi OS 64-bit (Bookworm/Bullseye)

This README file provides detailed instructions for installing Docker Engine on your Raspberry Pi OS 64-bit system. **These instructions are for Docker Engine (command-line interface), not Docker Desktop, which is not compatible with the Raspberry Pi's ARM64 architecture.**

### Prerequisites

* A Raspberry Pi 4B running Raspberry Pi OS 64-bit (either Bookworm or Bullseye).
* Terminal access (either directly or via SSH).
* `sudo` privileges.

### Installation Steps

1.  **Update the package list:**

    ```bash
    sudo apt update
    ```

    This command refreshes the list of available packages from the repositories.

2.  **Install necessary packages to use the Docker repository:**

    ```bash
    sudo apt install ca-certificates curl gnupg
    ```

    * `ca-certificates`: Allows verification of website authenticity.
    * `curl`: A command-line tool for transferring data.
    * `gnupg`: A tool for data encryption and signing.

3.  **Add Docker's official GPG key:**

    ```bash
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```

    This step adds Docker's key to your system to verify the authenticity of the packages.

4.  **Add the Docker repository to APT:**

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

    This adds the official Docker repository to your system's list of software sources.

5.  **Update the package list again:**

    ```bash
    sudo apt update
    ```

    This updates the package list to include the Docker packages from the newly added repository.

6.  **Install Docker Engine, Docker CLI, containerd.io, and the Docker Compose plugin:**

    ```bash
    sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    ```

    * `docker-ce`: The Docker Community Edition engine.
    * `docker-ce-cli`: The command-line interface for Docker.
    * `containerd.io`: A high-level container runtime.
    * `docker-compose-plugin`: Allows using `docker compose` for multi-container applications.

7.  **Add your user to the `docker` group (recommended for running Docker commands without `sudo`):**

    Replace `$USER` with your actual username if needed, but in most cases, this will add the currently logged-in user.

    ```bash
    sudo usermod -aG docker $USER
    ```

8.  **Apply the group changes:**

    You need to log out of your current session and log back in, or simply reboot your Raspberry Pi for the group changes to take effect.

    ```bash
    sudo reboot
    ```

### Verifying the Installation

After rebooting, open a terminal and run:

```bash
docker run hello-world
