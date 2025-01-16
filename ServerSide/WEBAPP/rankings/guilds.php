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


$stmt = odbc_prepare($Get_Game, "SELECT TOP 25 gi.nGuildID, gi.strGuildName, gi.tnGuildLevel, gi.nGuildFame, ci.Name AS OwnerName
FROM RYLgame.dbo.TblGuildInfo gi
LEFT JOIN RYLgame.dbo.CharInfo ci ON gi.nGuildID = ci.Guild
ORDER BY gi.nGuildFame DESC");

$result = odbc_execute($stmt);

echo "<div class='h2-title h2-title-content flex-s-c'><span>TOP RANKING</span></div>";
echo "<div class='topTitle'>Top 25 Guilds</div>
<div class='table-row table-scroll'>
<table class='rankingTable' width='100%'>
<thead>
<tr>
<td>Place</td><td></td><td>Guild</td><td>Owner</td><td>Level</td><td>Fame</td>
</tr>
</thead>
<tbody>";

$rank = 1;
while ($row = odbc_fetch_array($stmt))
  {
    if ($row['tnNationType'] == "1") { 
	$logobro = "<img src='../files/images/gameclass/human-logo.png' width='40' height='55'>";
	$racebro = "Kartefant"; 
    }
    if ($row['tnNationType'] == "2") {
	$logobro = "<img src='../files/images/gameclass/akkan-logo.png' width='40' height='55'>";
	$racebro = "Merkhadia";
    }

	if ($row['nGuildFame'] >= 1000) {
   	$row['nGuildFame'] = floor($row['nGuildFame']);
	}
	$formatted_fame = number_format($row['nGuildFame']);

    echo "<tr>
		<td>" . $rank . "</td>
		<td></td>
		<td>" . $row['strGuildName'] . "</td>
		<td>" . $row['OwnerName'] . "</td>
		<td>" . $row['tnGuildLevel'] . "</td>
		<td><strong><font color='orange'>$formatted_fame</font></strong></td>";
		
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