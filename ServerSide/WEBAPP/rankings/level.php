<?
include "../files/inc/modules/header.php";
?>
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
<body>
<main class="main"><aside>

						<?php include "../files/inc/modules/default.php"; ?>		
						<?php include "../files/inc/modules/social.php"; ?>

</aside>
	
<div class="content">
<?php


$stmt = odbc_prepare($Get_Game, "
SELECT TOP 25 CharInfo.cid, CharInfo.Name, CharInfo.Class, CharInfo.Race, CharInfo.Level, CharInfo.Fame, CharInfoEx.cid, CharInfoEx.ServerID, ISNULL(TblGuildInfo.strGuildName, '-') AS strGuildName,
CASE WHEN tblCurrentUser.uid = TblUnifiedCharList.uid THEN '[ Online ]' ELSE '' END AS OnlineStatus

FROM RYLgame.dbo.CharInfo AS CharInfo
LEFT JOIN RYLgame.dbo.TblGuildMember AS TblGuildMember ON CharInfo.cid = TblGuildMember.nCID
LEFT JOIN RYLgame.dbo.TblGuildInfo AS TblGuildInfo ON TblGuildMember.nGuildID = TblGuildInfo.nGuildID
LEFT JOIN RYLgame.dbo.TblUnifiedCharList AS TblUnifiedCharList ON CharInfo.cid = TblUnifiedCharList.Newcid
LEFT JOIN ROWPay.dbo.tblCurrentUser AS tblCurrentUser ON TblUnifiedCharList.uid = tblCurrentUser.uid
LEFT JOIN RYLgame.dbo.CharInfoEx AS CharInfoEx ON CharInfo.cid = CharInfoEx.cid

ORDER BY Level DESC");

$result = odbc_execute($stmt);

echo "
	<div class='h2-title h2-title-content flex-s-c'><span>TOP RANKINGS</span></div>";
echo "<div class='topTitle'>Top 25 Players</div>

<div class='table-row table-scroll'>
<table class='rankingTable' width='100%'>
<thead>
<tr>
<td>Place</td> 
<td></td>
<td>Player</td>
<td>Class</td>
<td>Last seen</td>
<td class='text-center'>Guild</td>
<td>Level/Fame</td>
</tr>
</thead>
<tbody>";

$rank = 1;
while ($row = odbc_fetch_array($stmt)) {

	if ($row['Fame'] >= 1000) {
   	$row['Fame'] = floor($row['Fame']);
	}
	$formatted_fame = number_format($row['Fame']);

	if ($row['Mileage'] >= 1000) {
   	$row['Mileage'] = floor($row['Mileage']);
	}
	$formatted_medal = number_format($row['Mileage']);

    if ($row['Race'] == "0") { 
	$logobro = "<img src='../files/images/slide/human-logo.png' width='40' height='50'>";
	$racebro = "Kartefant"; 
    }
    if ($row['Race'] == "1") {
	$logobro = "<img src='../files/images/slide/akkan-logo.png' width='40' height='50'>";
	$racebro = "Merkhadia";
    }
    if ($row['Class'] == "1") { 
	$class = "Fighter";
	$picture = "<img src='../files/images/gameclass/icon/warrior.png'>";
    } ;
    if ($row['Class'] == "2") {
        $class = "Rogue";
	$picture = "<img src='../files/images/gameclass/icon/assassin.png'>";
    } ;
    if ($row['Class'] == "3") {
        $class = "Mage";
	$picture = "<img src='../files/images/gameclass/icon/sorcerer.png'>";
    } ;
    if ($row['Class'] == "4") {
        $class = "Acolyte";
	$picture = "<img src='../files/images/gameclass/icon/enchanter.png'>";
    } ;
    if ($row['Class'] == "5") {
        $class = "Defender";
	$picture = "<img src='../files/images/gameclass/icon/defender.png'>";
    } ;
    if ($row['Class'] == "6") {
        $class = "Warrior";
	$picture = "<img src='../files/images/gameclass/icon/warrior.png'>";
    } ;
    if ($row['Class'] == "7") {
        $class = "Assassin";
	$picture = "<img src='../files/images/gameclass/icon/assassin.png'>";
    } ;
    if ($row['Class'] == "8") {
        $class = "Archer";
	$picture = "<img src='../files/images/gameclass/icon/archer.png'>";
    } ;
    if ($row['Class'] == "9") {
        $class = "Sorcerer";
	$picture = "<img src='../files/images/gameclass/icon/sorcerer.png'>";
    } ;
    if ($row['Class'] == "10") {
        $class = "Enchanter";
	$picture = "<img src='../files/images/gameclass/icon/enchanter.png'>";
    } ;
    if ($row['Class'] == "11") {
        $class = "Priest";
	$picture = "<img src='../files/images/gameclass/icon/priest.png'>";
    } ;
    if ($row['Class'] == "12") {
        $class = "Cleric";
	$picture = "<img src='../files/images/gameclass/icon/cleric.png'>";
    } ;
    if ($row['Class'] == "17") {
        $class = "Combatant";
	$picture = "<img src='../files/images/gameclass/icon/attacker.png'>";
    } ;
    if ($row['Class'] == "18") {
        $class = "Officiator";
	$picture = "<img src='../files/images/gameclass/icon/rune.png'>";
    } ;
    if ($row['Class'] == "19") {
        $class = "Templar";
	$picture = "<img src='../files/images/gameclass/icon/templar.png'>";
    } ;
    if ($row['Class'] == "20") {
        $class = "Attacker";
	$picture = "<img src='../files/images/gameclass/icon/attacker.png'>";
    } ;
    if ($row['Class'] == "21") {
        $class = "Gunner";
	$picture = "<img src='../files/images/gameclass/icon/gunner.png'>";
    } ;
    if ($row['Class'] == "22") {
        $class = "Rune";
	$picture = "<img src='../files/images/gameclass/icon/rune.png'>";
    } ;
    if ($row['Class'] == "23") {
        $class = "Life";
	$picture = "<img src='../files/images/gameclass/icon/life.png'>";
    } ;
    if ($row['Class'] == "24") {
        $class = "Shadow";
	$picture = "<img src='../files/images/gameclass/icon/shadow.png'>";
    } ;

    if ($row['ServerID'] == "201326850") { 
	$map = "Almighty Land"; 
    }

    if ($row['ServerID'] == "150995202") { 
	$map = "Karthena Viceroyalty"; 
    }

    if ($row['ServerID'] == "301990146") { 
	$map = "Caenarvaron"; 
    }

    if ($row['ServerID'] == "268435714") { 
	$map = "Battle Ground"; 
    }

    if ($row['ServerID'] == "285212930") {
	$map = "Pandora"; 
    }

    echo "<tr>
		<td>" . $rank . "</td>
		<td>" . $row['OnlineStatus'] . "</td>
		<td>" . $row['Name'] . " </td>
		<td> $picture $class</td>
		<td style='font-size: 13px; color: grey; text-shadow: 0 0 8px #ff9900'>$map </td>
		<td>".$row['strGuildName']."</td>
		<td>".$row['Level']." / <font style='vertical-align: top; font-size: 15px; color: #cc9900; text-shadow: 0 0 8px #ff9900'>$formatted_fame</font></td>";
		
    echo "</tr>";

    $rank++;
}
echo "</tr></tbody></table>";

?>

</div>
</div>
</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	