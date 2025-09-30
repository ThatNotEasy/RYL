<?PHP
# ODBC Connection
$SqlUser = "sa";
$SqlPass = "0JOv3z74Ji8E";

$UserDB = "youxiuser";
$GameDB = "RYLgame";
$DonateDB = "ROW_Item";
$Get_User = odbc_connect("$UserDB", "$SqlUser", "$SqlPass");
$Get_Game = odbc_connect("$GameDB", "$SqlUser", "$SqlPass");
$Get_Donate = odbc_connect("$DonateDB", "$SqlUser", "$SqlPass");

if (!$Get_User) {
    die("Connection failed: " . odbc_errormsg());
}

if (!$Get_Game) {
    die("Connection failed: " . odbc_errormsg());
}
if (!$Get_Donate) {
    die("Connection failed: " . odbc_errormsg());
}

# ODBC Connection End

?>