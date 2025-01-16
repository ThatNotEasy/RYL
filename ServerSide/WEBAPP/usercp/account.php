<?php
session_start();
error_reporting(0);


if (!isset($_SESSION["UID"])) {
    echo '<script>alert("Please login")</script>';
    echo '<script>window.location.href = "/pages/login";</script>';
}

$UID = $_SESSION["UID"];

include "../files/inc/modules/header.php";

//echo "<script>alert(" . $UID . ")</script>";
?>
<body>
<div class="wrapper">
<header>
<div class="topPanel">
<div class="btn btn-drop" data-class="topPanel-left">
<span></span>
<span></span>
<span></span>
</div>
<div class="topPanel-wrapper flex-c">
<div class="topPanel-left flex-c">
<?php include "../files/inc/modules/navbar.php"; ?>
</div>
</div>
</div>
<!-- top-panel -->
<div class="hand-animation">
<div class="light-hand"></div>
<div class="rune-hand"></div>
</div>
<div class="sparks">
<div class="spark_1"></div>
<div class="spark_2"></div>
<div class="spark_3"></div>
<div class="spark_4 spark-big"></div>
</div>
<div class="logo">
<a href=""><img src="../files/images/row-new3.png" alt="" class="bright"></a>
</div>
<?php include "../files/inc/modules/download.php"; ?>
</header><!-- .header-->
<style>
  .alert {
  padding: 20px;
  background-color: #f44336; /* Red */
  color: white;
  margin-bottom: 15px;
}

.alert-success {
  padding: 20px;
  background-color: #04AA6D; /* Red */
  color: white;
  margin-bottom: 15px;
}

.alert-warning {
  padding: 20px;
  background-color: #ff9800; /* Red */
  color: white;
  margin-bottom: 15px;
}

/* The close button */
.closebtn {
  margin-left: 15px;
  color: white;
  font-weight: bold;
  float: right;
  font-size: 22px;
  line-height: 20px;
  cursor: pointer;
  transition: 0.3s;
}

/* When moving the mouse over the close button */
.closebtn:hover {
  color: black;
}
</style>	
<main class="main"><aside>

						<?php include "../files/inc/modules/default.php"; ?>		
						<?php include "../files/inc/modules/social.php"; ?>

</aside>
	
<div class="content">
<div class="h2-title h2-title-content flex-s-c">
<span>Game Accounts</span>
</div>
<div class="ticketTitle flex-s-c">
<div class="ticketTitle-number">
Total Game Accounts: 1 / 10
</div>
<a class="button">Create Account</a>
</div>

<?php
echo '
<div class="table-row table-scroll">
<table class="tableTicket">
<thead>
<tr>
<td>Account</td> <td>Registered in</td> <td>Online Points</td><td></td>
</tr>
</thead>';
{
$stmt2 = odbc_prepare($Get_User, 'SELECT account,email, jointime, lastlogin, Points FROM usertbl WHERE UID = ?');
                                $result = odbc_execute($stmt2, array($UID));
			echo '<tbody>
<tr>';
                                while ($data = odbc_fetch_array($stmt2))
			{
				echo '<td>' . $data['account'] . ' </td>';
				echo '<td>' . $data['jointime'] . '</td>';
				#echo '<td>Last Login : ' . $data['lastlogin'] . '</td>';
				echo '<td>' . $data['Points'] . '</td>';
				# echo '</tr>';
				echo '<td>
<a href="/shops/premium"><span class="message-button">Redeem Online Points</span></a>
<p></p>
<a href="/usercp/mypassword"><span class="message-button">Change Password</span></a>
<p></p>
<span class="message-button">E-Mail - ' . $data['email'] . '</span>
<!---<a href="/usercp/myemail"><span class="message-button">Change Email</span></a>
<p></p>---!>';
           		}
			echo '</tr></tbody></table><br>';
}

echo '</div><div class="page-title"><span>My Characters</span></div>';
echo '
<div class="table-row table-scroll">
<table class="tableTicket">
<thead>
<tr>
<td> </td> <td>Name</td> <td>Level</td><td> Class </td><td>Fame</td><td>Medal</td>
</tr>
</thead>';

$stmt = odbc_prepare($Get_Game, 'SELECT CharInfox.Name as Name,CharInfox.CID as CID, CharInfox.Level as Level, CharInfox.Fame as Fame, 
					CharInfox.Mileage as Medal, CharInfox.Class as Class
                    		FROM UserInfo as UserInfox
                            	JOIN CharInfo as CharInfox
                            	 ON UserInfox.Char1 = CharInfox.CID
                           	 OR UserInfox.Char2 = CharInfox.CID
                                 OR UserInfox.Char3 = CharInfox.CID
                                 OR UserInfox.Char4 = CharInfox.CID
                                 OR UserInfox.Char5 = CharInfox.CID
                            
                            	 WHERE UID = ?');
                                $result = odbc_execute($stmt, array($UID));
    while ($data = odbc_fetch_array($stmt))
			{
    if ($data['Class'] == "1") { 
	$class = "Fighter";
	$picture = "<img src='../files/images/gameclass/icon/warrior.png' alt='row'>";
    } ;
    if ($data['Class'] == "2") {
        $class = "Rogue";
	$picture = "<img src='../files/images/gameclass/icon/assassin.png' alt='row'>";
    } ;
    if ($data['Class'] == "3") {
        $class = "Mage";
	$picture = "<img src='../files/images/gameclass/icon/sorcerer.png' alt='row'>";
    } ;
    if ($data['Class'] == "4") {
        $class = "Acolyte";
	$picture = "<img src='../files/images/gameclass/icon/enchanter.png' alt='row'>";
    } ;
    if ($data['Class'] == "5") {
        $class = "Defender";
	$picture = "<img src='../files/images/gameclass/icon/defender.png' alt='row'>";
    } ;
    if ($data['Class'] == "6") {
        $class = "Warrior";
	$picture = "<img src='../files/images/gameclass/icon/warrior.png' alt='row'>";
    } ;
    if ($data['Class'] == "7") {
        $class = "Assassin";
	$picture = "<img src='../files/images/gameclass/icon/assassin.png' alt='row'>";
    } ;
    if ($data['Class'] == "8") {
        $class = "Archer";
	$picture = "<img src='../files/images/gameclass/icon/archer.png' alt='row'>";
    } ;
    if ($data['Class'] == "9") {
        $class = "Sorcerer";
	$picture = "<img src='../files/images/gameclass/icon/sorcerer.png' alt='row'>";
    } ;
    if ($data['Class'] == "10") {
        $class = "Enchanter";
	$picture = "<img src='../files/images/gameclass/icon/enchanter.png' alt='row'>";
    } ;
    if ($data['Class'] == "11") {
        $class = "Priest";
	$picture = "<img src='../files/images/gameclass/icon/priest.png' alt='row'>";
    } ;
    if ($data['Class'] == "12") {
        $class = "Cleric";
	$picture = "<img src='../files/images/gameclass/icon/cleric.png' alt='row'>";
    } ;
    if ($data['Class'] == "17") {
        $class = "Combatant";
	$picture = "<img src='../files/images/gameclass/icon/attacker.png' alt='row'>";
    } ;
    if ($data['Class'] == "18") {
        $class = "Officiator";
	$picture = "<img src='../files/images/gameclass/icon/rune.png' alt='row'>";
    } ;
    if ($data['Class'] == "19") {
        $class = "Templar";
	$picture = "<img src='../files/images/gameclass/icon/templar.png' alt='row'>";
    } ;
    if ($data['Class'] == "20") {
        $class = "Attacker";
	$picture = "<img src='../files/images/gameclass/icon/attacker.png' alt='row'>";
    } ;
    if ($data['Class'] == "21") {
        $class = "Gunner";
	$picture = "<img src='../files/images/gameclass/icon/gunner.png' alt='row'>";
    } ;
    if ($data['Class'] == "22") {
        $class = "Rune";
	$picture = "<img src='../files/images/gameclass/icon/rune.png' alt='row'>";
    } ;
    if ($data['Class'] == "23") {
        $class = "Life";
	$picture = "<img src='../files/images/gameclass/icon/life.png' alt='row'>";
    } ;
    if ($data['Class'] == "24") {
        $class = "Shadow";
	$picture = "<img src='../files/images/gameclass/icon/shadow.png' alt='row'>";
    } ;
				echo '<tbody><tr>';
				echo '<td>' .  $picture . '</td>';
				echo '<td>' . $data['Name'] . '</td>';
				echo '<td>Lvl.' . $data['Level'] . '</td>';
				echo '<td>' .  $class . '</td>';
				echo '<td>' . $data['Fame'] . '</td>';
				echo '<td>' . $data['Medal'] . '</td>';

			echo '</tr></tbody>';
			}

			echo '</table>';
			echo '</div><br><br>';



				# Connection History
				echo '<div class="page-title"><span>Connection History</span></div>';
				echo '
				<div class="table-row table-scroll" style="margin: 1px 1px 1px 1px">
				<table class="tableTicket">
				<thead>
				<tr>
				<td>#</td> <td>IP</td> <td>Date and Time</td>
				</tr>
				</thead>';
			{
                                $result = odbc_execute($stmt2, array($UID));
			echo '<tbody><tr>';
                                while ($data = odbc_fetch_array($stmt2))
			{
				echo '<td>1</td>';
				echo '<td>2001:d08:dd:9302:a835:fad6:8d98:819b</td>';
				echo '<td>' . $data['lastlogin'] . '</td>';


           		}
			echo '</tr></tbody></table><br>';
}

 ?>
</div>
</div>
</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	