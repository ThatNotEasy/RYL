# Installation Guide for Patch

## Overview

This guide will walk you through the installation of the patch which includes various components such as `Patch.exe`, `update\default.htm`, `Login.dat`, `nPro Server`, `Apache Server`, and custom assets like a desktop shortcut and customized background and billboard.

## Components Included

- **Patch.exe**: Main executable for the patch.
- **update\default.htm**: Default HTML file for updates.
- **Login.dat**: File containing login data.
- **nPro Server**: Server component required for the patch.
- **Apache Server**: Apache server component.
- **Desktop Shortcut**: Shortcut to the application on the desktop.
- **Customized Background and Billboard**: Custom visual assets for the application.

## Installation Steps

1. **Download and Extract**
   - Download the installation package (e.g., `patch.zip`).
   - Extract the contents to a temporary directory.

2. **Run the Installation Script**
   - Navigate to the extracted directory.
   - Execute the installation script by double-clicking `install.bat`.

3. **Follow the On-Screen Prompts**
   - The script will handle the following:
     - Extracting files.
     - Installing and configuring the Apache server.
     - Modifying the `Login.dat` file with the correct server IP and domain.
     - Creating a desktop shortcut.
     - Adding customized background and billboard files.
     - Setting up `Start.bat` and `Close.bat` scripts for server management.

## Configuration Details

### Update `Login.dat`

- The `Login.dat` file will be updated automatically with server information:
  - **Server IP**: Read from `update\server_ip.txt`.
  - **Server Domain**: Read from `update\server_domain.txt`.

### Desktop Shortcut

- A desktop shortcut will be created named `YourApp.lnk`, which points to the main executable of the application.

### Apache Configuration

- The Apache server will be installed and configured to use the `default.htm` file located in `update\`.

### Background and Billboard

- The custom background and billboard files will be placed in the appropriate user directories.

## Troubleshooting

- **Disk Busy Error**: If the disk is busy, the script will prompt you to use `start.bat` with a disk letter.
- **Server Not Starting**: Ensure that no other instance of the Apache server is running and check for errors in `Start.bat`.

## Contact

For additional help or support, please contact [Your Support Email] or visit [Your Support Website].

## License

This patch and associated files are provided under [Your License] terms.

## Disclaimer

This installation guide and associated files are provided "as-is" without any warranty of any kind. Use them at your own risk.
