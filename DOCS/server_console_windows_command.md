# RYL2 Server Executables Guide

## Overview
This guide provides an overview of the various server executables used in the RYL2 server setup. These executables are used to manage and control different aspects of the server, including authentication, user identification, login, database, chat, and game functionalities.

## AuthServer RYL2

- **statlog**: Logs server statistics.
- **statclear**: Clears the server statistics.
- **reloadpass**: Reloads passwords from the database.
- **flush**: Flushes the server data.
- **reloadsetup**: Reloads server setup configurations.
- **startserver**: Starts the authentication server.

## UIDServer RYL2

- **perflog**: Logs server performance.
- **statlog**: Logs server statistics.
- **statclear**: Clears server statistics.
- **flush**: Flushes server data.
- **reload**: Reloads server configurations.

## LoginServer RYL2

- **reloadscript**: Reloads login server scripts.
- **reloadsetup**: Reloads login server setup configurations.
- **flush**: Flushes login server data.
- **ip_admin_only**: Restricts access to admin IPs only.
- **ip_open_all**: Allows access from all IPs.
- **ip_open_allowed**: Allows access from specified IPs.
- **server_open**: Opens the server for login.
- **server_ready_patch**: Applies patches and prepares the server.
- **server_close**: Closes the server.

## DBAgentServer RYL2

- **siegetime**: Manages siege time settings.
- **reloadsiegetime**: Reloads siege time settings.
- **reloadadmin**: Reloads admin settings.
- **loadchar <UID> <CID>**: Loads a character with the specified UID and CID.
- **connect**: Connects to the database.
- **reloadsetup**: Reloads database agent server setup configurations.
- **flush**: Flushes database agent server data.

## ChatServer RYL2

- **statlog**: Logs chat server statistics.
- **reloadsetup**: Reloads chat server setup configurations.
- **connect**: Connects to the chat server.
- **flush**: Flushes chat server data.
- **log**: Logs chat server activities.
- **pool**: Manages chat server connections pool.

## GameServer RYL2

- **resetdummies**: Resets dummy players in the game.
- **setdummies <id>**: Sets dummies with the specified ID.
- **statlog**: Logs game server statistics.
- **statclear**: Clears game server statistics.
- **lotteryevent**: Manages lottery events in the game.
- **autobalance**: Automatically balances the game.
- **notify <text>**: Sends a notification with the specified text.
- **itemdroplist**: Lists available items for drop.
- **itemdrop <nick> <itemID> <amount>**: Drops specified items for a player with the given nickname.
- **flush**: Flushes game server data.
- **reloadsetup**: Reloads game server setup configurations.
- **log**: Logs game server activities.
- **pool**: Manages game server connections pool.
- **connect**: Connects to the game server.
- **startserver**: Starts the game server.

## Usage Tips

- Ensure that you use these commands as per the requirements of your server environment.
- Commands that modify server configurations or data (like `flush`, `reloadsetup`, etc.) should be used with caution to avoid unintended disruptions.
- Regularly back up your server data and configurations to prevent data loss.

## Additional Resources

For more detailed instructions and troubleshooting, refer to the server documentation or support forums related to RYL2.

Feel free to adjust or add more details based on your specific server setup and requirements.
