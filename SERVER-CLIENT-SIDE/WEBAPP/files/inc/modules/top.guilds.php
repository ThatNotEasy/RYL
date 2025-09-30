<?php

$stmt = odbc_prepare($Get_Game, "SELECT TOP 10 gi.nGuildID,  gi.nGuildGold, gi.strGuildName, gi.tnGuildLevel, gi.nGuildFame, ci.Name AS OwnerName
FROM TblGuildInfo gi
LEFT JOIN CharInfo ci ON gi.nGuildID = ci.Guild
ORDER BY gi.nGuildFame DESC");

$result = odbc_execute($stmt);
echo "<div class='rankings blockHome'>

<div class='h2-title h2-title-table flex-s-c'>
<span>Rankings</span>
<div class='tabTable'>
<a >Top Guild</a>
</div>
</div>";

echo "
<div class='table tabTable-block active' id='players'>
<div class='tableBlock'>
<div class='tableBlock-title'>
<div class='tableBlock-title_player'>Guild</div>
<div class='tableBlock-title_level'>Level</div>
<div class='tableBlock-title_score'>Fame</div>
</div>";

$rank = 1;
while ($row = odbc_fetch_array($stmt))
  {
    if ($row['tnNationType'] == "1") { 
	$logobro = "<img src='files/images/gameclass/human-logo.png' width='22' height='22' alt='row'>";
	$racebro = "Kartefant"; 
    }
    if ($row['tnNationType'] == "2") {
	$logobro = "<img src='files/images/gameclass/slide/akkan-logo.png' width='22' height='22' alt='row'>";
	$racebro = "Merkhadia";
    }

	if ($row['nGuildGold'] >= 1000) {
   	$row['nGuildGold'] = floor($row['nGuildGold']);
	}

	$formatted_gold = number_format($row['nGuildGold']);

	if ($row['nGuildFame'] >= 1000) {
   	$row['nGuildFame'] = floor($row['nGuildFame']);
	}
	$formatted_fame = number_format($row['nGuildFame']);

    echo "<div class='tableBlock-content'>";
    echo "<div class='tableBlock-conten_number'>" . $rank . "</div>
    <div class='tableBlock-conten_name'>".$logobro." <a href> ".$row['strGuildName']."
	<div class='tablePopup'>
	<span class='tablePopup-title'>" . $row['strGuildName'] . "</span>
	<div class='tablePopup-ava'>$logobro </div>
	<div class='tablePopup-block'>
	<span>Level:</span> <span>" . $row['tnGuildLevel'] . "</span>
	</div>
	<div class='tablePopup-block'>
	<span>Owner:</span> <span>" . $row['OwnerName'] . "</span>
	</div>

	<div class='tablePopup-block'>
	<span>Race:</span> <span>$racebro </span>
	</div>

	<div class='tablePopup-block'>
	<span>Fame:</span> <span>$formatted_fame</span>
	</div>

	<div class='tablePopup-block'>
	<span>Gold:</span> <span>$formatted_gold</span>
	</div>

	</div>
	</a></div>

    <div class='tableBlock-conten_lvl'><span class='color-yellow'>" . $row['tnGuildLevel'] . "</div>
    <div class='tableBlock-conten_scr'>" . $row['nGuildFame'] . "</div>";
    $rank++;
echo "</div>";
}
echo "</div>";
echo "</div>";
echo "	<div class='all-button'>
		<a href='/rankings/guilds' class='button'>View All</a>
	</div>";
echo "</div>";

?>


