# RYL2 Error Codes Reference

## Definitions

### GameMon Errors (110 - 200)

- **110**: `NPGAMEMON_ERROR_EXIST` - GameMon Already Exist
- **111**: `NPGAMEMON_ERROR_CREATE` - GameGuard Directory Create Error
- **112**: `NPGAMEMON_ERROR_NPSCAN` - npscan.des Error
- **113**: `NPGAMEMON_ERROR_THREAD` - CreateThread Error
- **114**: `NPGAMEMON_ERROR_INIT` - GameMon Initialize Error
- **115**: `NPGAMEMON_ERROR_GAME_EXIST` - Game Instance Already Exist
- **120**: `NPGAMEMON_ERROR_AUTH_INI` - .ini Authentication Fail
- **121**: `NPGAMEMON_ERROR_AUTH_NPGMUP` - npgmup.des Authentication Fail
- **122**: `NPGAMEMON_ERROR_AUTH_GAMEMON` - GameMon.des Authentication Fail
- **123**: `NPGAMEMON_ERROR_AUTH_NEWUP` - npgmup.des.new Auth Fail
- **124**: `NPGAMEMON_ERROR_AUTH_GAMEGUARD` - GameGuard.des Authentication Fail
- **130**: `NPGAMEMON_ERROR_DECRYPT` - .ini File Decryption Fail
- **141**: `NPGAMEMON_ERROR_CORRUPT_INI` - Corrupt ini File Error
- **142**: `NPGAMEMON_ERROR_CORRUPT_INI2` - Not Match GameName in ini File Error
- **150**: `NPGAMEMON_ERROR_NFOUND_INI` - ini File Not Found
- **151**: `NPGAMEMON_ERROR_NFOUND_NPGMUP` - npgmup.des Not Found
- **152**: `NPGAMEMON_ERROR_NFOUND_NEWUP` - npgmup.des.new Not Found
- **153**: `NPGAMEMON_ERROR_NFOUND_GG` - GameGuard.des Not Found
- **154**: `NPGAMEMON_ERROR_NFOUND_GM` - GameMon.des Not Found
- **155**: `NPGAMEMON_ERROR_CRYPTOAPI` - rsabase.dll is Corrupted
- **160**: `NPGAMEMON_ERROR_COMM` - Communication Init Error
- **170**: `NPGAMEMON_ERROR_EXECUTE` - GameMon Execute Error
- **171**: `NPGAMEMON_ERROR_EVENT` - GameMon Event Create Error
- **180**: `NPGAMEMON_ERROR_NPGMUP` - npgmup.dll Error
- **191**: `NPGAMEMON_ERROR_MOVE_INI` - Move ini Error
- **192**: `NPGAMEMON_ERROR_MOVE_NEWUP` - Move npgmup.des.new Error
- **200**: `NPGAMEMON_ERROR_ILLEGAL_PRG` - Detected an Illegal Program

### GameMon and SpeedCheck Errors (210 - 220)

- **210**: `NPGAMEMON_ERROR_GAMEMON` - GameMon Init Error
- **220**: `NPGAMEMON_ERROR_SPEEDCHECK` - SpeedCheck Init Error

### GameGuard Errors (230 - 299)

- **230**: `NPGAMEMON_ERROR_GAMEGUARD` - GameGuard Init Error

### Update Errors (310 - 399)

- **340**: `NPGMUP_ERROR_DOWNCFG` - Download Error
- **350**: `NPGMUP_ERROR_ABORT` - Canceled by User
- **360**: `NPGMUP_ERROR_AUTH` - File Authentication Error
- **361**: `NPGMUP_ERROR_AUTH_INI` - .ini Authentication Error
- **370**: `NPGMUP_ERROR_DECRYPT` - .ini Decrypt Error
- **380**: `NPGMUP_ERROR_CONNECT` - Connect to Update Server Fail
- **390**: `NPGMUP_ERROR_INI` - .ini is Corrupted

## Usage

- **Error Codes 110 - 200**: These errors are related to GameMon and its components, including initialization, file handling, and authentication issues.
- **Error Codes 210 - 220**: Errors specific to GameMon and SpeedCheck initialization.
- **Error Code 230**: Pertains to GameGuard initialization issues.
- **Error Codes 340 - 399**: Concerns update process errors, such as downloading, authentication, and connection issues.

Refer to these codes to diagnose and troubleshoot server issues. Each code provides insights into specific problems within the server's components and processes.
