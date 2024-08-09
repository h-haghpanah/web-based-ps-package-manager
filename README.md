# PlayStation Package Manager - Documentation

## Overview
Welcome to the PlayStation Package Manager! This web-based application allows you to manage and send PlayStation packages (PKGs) to your local or remote PlayStation consoles effortlessly. The application integrates with the RAWG API to fetch game metadata and provides a flexible setup for managing local or remote package repositories.

## Key Features
- **Web-Based Interface:** Access the application from any device with a web browser.
- **RAWG API Integration:** Fetch game metadata automatically for easy management and identification.
- **Multiple Repository Support:** Configure both local and remote package repositories for flexible storage options.
- **PlayStation Management:** Define and manage multiple PlayStation consoles, choosing which to send packages to.
- **Package Types:** Organize game packages into Install, Update, and DLC categories for each game.

## Installation
Follow these steps to install and run the PlayStation Package Manager:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/h-haghpanah/web-based-ps-package-manager.git
   cd web-based-ps-package-manager
   ```
2. **Install Requirements:**
   Make sure you have Python installed. Then, install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   Start the application by running:
   ```bash
   python app.py
   ```
4. **Access the Application:**
   Start the application by running:
   ```bash
   python app.py
   ```
## Initial Configuration
To set up the PlayStation Package Sender, follow these steps:

1. **Access Settings:** Click the settings button at the top of the interface.
2. **Local Package Repository:** Toggle the switch to `ON` if you are using a local repository. Enter the local IP address in the `Local IP Address` field. The default port is 85, which can be changed in the `config.ini` file under the `local_port` setting.
3. **Remote Package Repository:** If using a remote repository, toggle the `Local Package Repository` switch to `OFF`. Enter the remote repository's web address in the `Remote Repository Web Address` field (e.g., `http://192.168.1.10:8080`).
4. **Ensure Firewall Settings:** Make sure your system's firewall allows inbound connections on the specified port and web server.
5. **File Organization:** Store your game packages in folders with the following structure:

    ```
    /[Game Name]/
        ├── Install/
        ├── Update/
        └── DLC/
    ```

6. **Remote Server Configuration:** If using a remote server, place the `index.php` file from `remote_web_server_files/` in the root directory of your remote web server. This is critical for providing file and folder information.

## Managing PlayStation Consoles
To define and manage your PlayStation consoles:

1. In the settings, go to the **PS IP Addresses** section.
2. Enter each console's details in the format: `[Friendly Name]=[IP Address]`. Example: `hesam=192.168.1.20`
3. Use the dropdown menu at the top of the main interface to select which console to send packages to.

## Using RAWG API
To fetch game metadata using the RAWG API:

1. Enable the RAWG API in the settings.
2. Sign up on the RAWG website and obtain your free API key: [Sign Up](https://rawg.io/signup)
3. Enter your API key in the `RAWG API Key` field.

## About Me
Hi, I'm **Hesam Haghpanah**, a developer and fan of video games. I developed this project to provide an easier way to manage and send PlayStation packages from a web-based platform. If you'd like to check out the code or contribute, you can find the repository at:

[Repository Link](https://github.com/h-haghpanah/web-based-ps-package-manager.git)

If you have any questions or suggestions, feel free to reach out to me at: [h.haghpanah@outlook.com](mailto:h.haghpanah@outlook.com).

Hope you enjoy and have a great gaming time!

---

&copy; 2024 PlayStation Package Sender. All rights reserved.
