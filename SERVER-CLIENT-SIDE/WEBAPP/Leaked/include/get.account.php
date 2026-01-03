<?php
include "database.config.php";

function GetPoint($UID)
{
    global $Get_User;
    $stmt = odbc_prepare($Get_User, 'SELECT * FROM usertbl WHERE UID = ?');
    $result = odbc_execute($stmt, array($UID));
    $status = odbc_num_rows($stmt);
    $data = odbc_fetch_array($stmt);

    return $data["Points"];
}

function SetPoint($Point, $UID)
{
    global $Get_User;
    $stmt = odbc_prepare($Get_User, 'UPDATE usertbl SET Points = ? WHERE UID = ?');
    $result = odbc_execute($stmt, array($Point, $UID));
    $status = odbc_num_rows($stmt);
    return true;
    if ($status > 0) {
        return true;
    }
}
