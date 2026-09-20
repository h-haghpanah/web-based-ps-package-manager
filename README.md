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
   Open your web browser and go to http://localhost:85 (or the port you have configured in config.ini).

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

## Repository Type Configuration (PS4 / PS5)

The application allows you to select the target console's **Repository Type** directly from the Settings panel. This determines which payload is required on your console to receive and install packages sent from the app.

1. **Access Settings:** Open the settings panel and locate the **Repository Type** option.
2. **Choose PS4 or PS5**, depending on the console you're sending packages to.

### PS4
If **PS4** is selected as the repository type, your console must have a package installer payload running in order to receive and install files sent from this app.

- Install the payload from: [pkg-zone.com/details/FLTZ00003](https://pkg-zone.com/details/FLTZ00003)
- Once the payload is running on your PS4, packages sent from the app will be received and installed automatically.

### PS5
If **PS5** is selected as the repository type, your console must be running the **ps5downloader** payload to receive files sent from the app.

- Download and install the payload: [ps5_file_downloader repository](https://github.com/h-haghpanah/ps5_file_downloader)

By default, files sent to the PS5 are placed in `/data/etaHEN/games`, using single-file game formats (exFAT, PFSC, etc.). 

> **Note:** If you have **ShadowMount** or **etaHEN's ShadowMount Plus** payload active on your PS5, games will be installed automatically once received.

#### PS5 Send Method
When **PS5** is selected, a **PS5 Send Method** option appears in Settings so you can choose which homebrew receives the packages:

| Method | Payload | Port |
| --- | --- | --- |
| `ps5_file_downloader` | [ps5_file_downloader](https://github.com/h-haghpanah/ps5_file_downloader) | 8283 |
| `pkg_receiver` | `loopayeh-pkg_receiver` | 12800 |

The setting is stored in `config.ini` as `ps5_send_method` under the `[ps]` section. PS4 is unaffected and keeps using its own payload.

#### pkg_receiver behaviour
The receiver exposes two different transfer paths and the app picks one per file:

- **`.pkg` files** go to `POST /api/install`, which hands the URL to the system installer. The console downloads the package itself and the result appears as a toast on screen, so only a running/finished state is available to the app.
- **Every other file** (`.exfat`, `.ffpkg`, `.ffpfsc`, ...) goes to `POST /api/files/pull` with a destination inside `/data/homebrew`, which is the only jail the receiver accepts. This path reports real byte level progress.

Before a pull the app calls `GET /api/files/stat`; if a smaller partial file is already on the console the transfer is sent with `mode: resume`, otherwise it overwrites. It also sends `{"paused":0}` to `POST /api/pull/pause` first, because that flag is global and survives the previous transfer.

#### Download Monitor
With `pkg_receiver` selected, a download icon appears next to the settings button. The panel polls the console every two seconds and shows:

- the receiver build from `GET /api/version` and whether the console still hears this PC from `GET /api/pc` (an announcement older than 15s is treated as stale),
- busy state and job count from `GET /api/status`, plus `pullName`, `pullGot` and `pullWant` for the active copy,
- per file progress, with the size of finished or stopped transfers read back from `GET /api/fs/list` and `GET /api/files/stat`,
- **Pause / Resume** for the running copy, and **Clear Finished** to drop completed entries.

Transfer speed and ETA are calculated from the difference between two polls, since the receiver does not report them. When `pullWant` is `-1` (the source sent no `Content-Length`) the total size recorded at send time is used instead. Sent packages are tracked in `receiver_jobs.json`.

#### Console Discovery
The receiver broadcasts a `PKGSENDER` beacon to UDP port 12801 every three seconds. With `pkg_receiver` selected, a **Scan Network** button appears under **PS IP Addresses** in Settings; it listens for a few seconds and appends any console that answers.

## Using RAWG API
To fetch game metadata using the RAWG API:

1. Enable the RAWG API in the settings.
2. Sign up on the RAWG website and obtain your free API key: [Sign Up](https://rawg.io/signup)
3. Enter your API key in the `RAWG API Key` field.

## About Me
Hi, I'm **Hesam Haghpanah**, a developer and fan of video games. I developed this project to provide an easier way to manage and send PlayStation packages from a web-based platform. If you'd like to check out the code or contribute
If you have any questions or suggestions, feel free to reach out to me at: [h.haghpanah@outlook.com](mailto:h.haghpanah@outlook.com).

Hope you enjoy and have a great gaming time!

---

&copy; 2024 PlayStation Package Manager. All rights reserved.
