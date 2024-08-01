# Server Setup Guide

## Overview
This guide provides basic setup instructions for your server, including installing the server files, setting up databases, and configuring the server. This guide is a work in progress and may not be complete. If you encounter issues such as a 'Server Error' when trying to log in, it may be due to database file issues. Assistance from others may be needed to reconstruct the database files.

## Prerequisites
1. **Server Files**:
   - Download the RYL2 Server Files: [RapidShare Webhosting + Webspace](http://example.com/ryl2-server-files)

2. **Database Software**:
   - You will need either Windows SQL Server 2000 (SP4) or Windows SQL Server 2005.
   - Download SQL Server 2005: [Microsoft SQL Server 2005 Trial](http://www.microsoft.com/sql/downloads/trial-software.mspx)
   - Download SQL Server 2000: [Microsoft SQL Server 2000](http://www.microsoft.com/downloads/details.aspx?FamilyID=8e2dfc8d-c20e-4446-99a9-b7f0213f8bc5)
   - Download SQL Server 2000 SP4: [Microsoft SQL Server 2000 SP4](http://www.microsoft.com/downloads/details.aspx?FamilyID=8e2dfc8d-c20e-4446-99a9-b7f0213f8bc5)

   **Note**: Install SQL Server in Mixed Mode and remember your username and password.

## Setting Up the Server Files

1. **Extract Server Files**:
   - Extract the downloaded server files to your desktop.
   - Inside the extracted folder, find the `comdatabase` archive.
   - Create a new folder named `comdatabase` in the directory.
   - Extract the contents of the `comdatabase` archive into this new folder.

2. **Database Setup**:

   ### MSSQL 2000

   - Refer to the [RYL 1 Server Guide](http://example.com/ryl1-server-guide) for instructions on adding a new database and restoring tables.
   - Create and name databases as follows:
     - `AdminTool`
     - `CharDelHistory`
     - `Part2_Zodiac`
     - `pay_gamemyth`
     - `RYLBillingDB_LOG`
     - `youxiCard`
     - `youxiuser`
   - Restore the databases using the names specified.

   ### MSSQL 2005

   - Log in to SQL Server Management Studio.
   - Create the following databases:
     - `AdminTool`
     - `CharDelHistory`
     - `Part2_Zodiac`
     - `pay_gamemyth`
     - `RYLBillingDB_LOG`
     - `youxiCard`
     - `youxiuser`
   - Restore each database by right-clicking the database, selecting `Tasks -> Restore -> Database`, and following the prompts.

## Configuring Server Files

1. **English Translation**:
   - Download the English translation of the Server Setup from [here](http://forum.ragezone.com/attachments/28194-setup_eng.rar?d=1150679491).
   - Replace the existing executable in the server files directory with the translated one.

2. **Server Setup Configuration**:
   - Run the server setup executable and configure it as follows:

   **Login Tab**:
   - Least Version: `1600`
   - Patch Address: Your IP

   **Auth Tab**:
   - ServerType: `YouxiLandAuth`
   - Server Group: `5=5`
   - DB Agent Address: Your IP
   - Leave all checkboxes unchecked.

   **DataSource Config**:
   - DB Type: `MSSQL`
   - DB Address: Your IP
   - DB Name: `youxiuser`
   - DB Username: `sa`
   - DB Password: Your Password

   **AdminTool Config**:
   - DB Type: `MSSQL`
   - DB Address: Your IP
   - DB Name: `AdminTool`
   - DB Username: `sa`
   - DB Password: Your Password

   **Game Tab**:
   - Zone Count: `3`
   - Zone: `5=Malaysia`
   - Configure each zone as described.

   **Agent Tab**:
   - Server Group: `5=5`
   - Nation: `1=Taiwan`
   - Server Type: `Part1`
   - BillingType: `JapanBilling`
   - Version: Your version (e.g., `1602`)
   - Sum Check: `0x414CA637` (for version 1602)
   - Patch Address: Your IP
   - UID Server Address: Your IP

   **Keeper Tab**:
   - Check `Free Mode`
   - Server Type: `JapanBilling`
   - HanUnitedBillingAddress: Your IP

   **Log And Chat Tab**:
   - Configure Log DB and Chat Server settings as described.

3. **Starting the Servers**:
   - Start servers in the following order:
     1. `RylLoginServer.exe`
     2. `RylUIDServer.exe`
     3. `RylDBAgentServer.exe`
     4. `RylAuthServer.exe`
     5. `RylChatServer.exe`
   - Start the map servers (`map8`, `map12`, and `map14`).

   **Note**: RylUIDServer.exe may require multiple attempts to start. Ensure that all server icons are visible in the system tray.

## Creating User Accounts

1. Open Enterprise Manager or SQL Server Management Studio.
2. Navigate to the `youxiuser` database.
3. Open the `usertbl` table and create a new user account by entering values for `account` and `passwd`.

## DemonSetup.ini Configuration

Save the following configuration into `C:\WINDOWS\DemonSetup.ini`:

```ini
[LoginServer]
ServerID=0
PingCheck=0
AloneMode=0
LeastPatchVer=1602
PatchAddr=YOURIPHERE

[AuthServer]
ServerID=1
AuthType=2
DBAgentAddr=YOURIPHERE
PingCheck=0
KoreanLangCheck=0
BattleServerAuth=0
TestGroupAuth=0
SupressCharCreate=0
SupressCharDelete=0
AuthDBType=MSSQL
AuthDBAddr=YOURIPHERE
AuthDBName=youxiuser
AuthDBUser=sa
AuthDBPass=YOURPASSHERE
AdminToolDBType=MSSQL
AdminToolDBAddr=YOURIPHERE
AdminToolDBName=AdminTool
AdminToolDBUser=sa
AdminToolDBPass=YOURPASSHERE

[Zone_ETC]
GameServerNation=5
BattleServerGroup=0
ZoneCount=3

[DBAgentServer]
ServerID=3
ServerType=22
BillingType=3
NationType=5
ClientVersion=1602
PatchAddress=YOURIPHERE
LoginServerAddr=YOURIPHERE
UIDServerAddr=YOURIPHERE
CheckSum=0x414CA637
LimitServerGroupUserNum=6000
LimitBattleUser=6000
PingCheck=0
AdminIPCheck=0
BattleServer=0
GameDBType=MSSQL
GameDBAddr=YOURIPHERE
GameDBName=Part2_Zodiac
GameDBUser=sa
GameDBPass=YOURPASSHERE
Part1UnifiedAgentAddr=
RestrictedPart1ToPart2Level=
MaxTransferCharNum=
Part2SelectableUnifiedServerNum=0

[UIDServer]
FreeCheck=1
IgnoreFlag=1
BillingType=3
HanUnitedBillingAddr=YOURIPHERE
HanUnitedBillingPort=
BillingDBType=MSSQL
BillingDBAddr=YOURIPHERE
BillingDBName=pay_gamemyth
BillingDBUser=sa
BillingDBPass=YOURPASSHERE

[LogServer]
LogDBType=MSSQL
LogDBAddr=YOURIPHERE
LogDBName=youxiCard
LogDBUser=sa
LogDBPass=YOURPASSHERE

[ChatServer]
ServerID=7
PingCheck=0
UserIPCheck=0
DBAgentAddress=YOURIPHERE
AdminToolDBType=MSSQL
AdminToolDBAddr=YOURIPHERE
AdminToolDBName=AdminTool
AdminToolDBUser=sa
AdminToolDBPass=YOURPASSHERE

[Zone_1200]
ServerID=201326594
PingCheck=0
SpeedHackCheck=0
LotteryEvent=0
LevelUpEvent=0
DeathPenaltyEvent=0
DBAgentServerAddr=YOURIPHERE
LogServerAddr=YOURIPHERE
ChatServerAddr=YOURIPHERE
ExpRate=1300
DropRate=1500
FameMin=10
FameMax=20
BattleUserLimit=3000
SetCount=1

[Zone_0800]
ServerID=134217730
PingCheck=0
SpeedHackCheck=0
LotteryEvent=0
LevelUpEvent=0
DeathPenaltyEvent=0
DBAgentServerAddr=YOURIPHERE
LogServerAddr=YOURIPHERE
ChatServerAddr=YOURIPHERE
ExpRate=1000
DropRate=1300
FameMin=0
FameMax=90000
BattleUserLimit=50
SetCount=2

[Zone_1400]
ServerID=234881026
PingCheck=0
SpeedHackCheck=0
LotteryEvent=0
LevelUpEvent=0
DeathPenaltyEvent=0
DBAgentServerAddr=YOURIPHERE
LogServerAddr=YOURIPHERE
ChatServerAddr=YOURIPHERE
ExpRate=1800
DropRate=2000
FameMin=0
FameMax=100000
BattleUserLimit=3000
SetCount=3
```
