<?php

$stmt = odbc_prepare($Get_Game, "SELECT TOP 10 * FROM CharInfo ORDER BY Level DESC, Fame DESC");
$stmt2 = odbc_prepare($Get_Game, "SELECT TOP 10 gi.nGuildID,  gi.nGuildGold, gi.strGuildName, gi.tnGuildLevel, gi.nGuildFame, ci.Name AS OwnerName
FROM RYLgame.dbo.TblGuildInfo gi
LEFT JOIN RYLgame.dbo.CharInfo ci ON gi.nGuildID = ci.Guild
ORDER BY gi.nGuildFame DESC");


$result = odbc_execute($stmt);
$result = odbc_execute($stmt2);

echo "<div class='rankings blockHome'>
<div class='h2-title h2-title-table flex-s-c'>
<span>Rankings</span>
<div class='tabTable'>
<a >Top Players</a>
</div>
</div>";

echo "
<div class='table tabTable-block active' id='players'>
<div class='tableBlock'>
<div class='tableBlock-title'>
<div class='tableBlock-title_player'>Player</div>
<div class='tableBlock-title_level'>Level</div>
<div class='tableBlock-title_score'>Fame</div>
</div>";

$rank = 1;
while ($row = odbc_fetch_array($stmt))
  {
    if ($row['Sex'] == "1") { 
	$Sex = "Male"; 
    }

    if ($row['Sex'] == "2") { 
	$Sex = "Female"; 
    }

    if ($row['Sex'] == "3") { 
	$Sex = "Male"; 
    }

    if ($row['Sex'] == "4") { 
	$Sex = "Female"; 
    }

    if ($row['Race'] == "0") { 
	$logobro = "<img src='/files/images/gameclass/human-logo.png' width='50' height='65' alt='row'>";
	$racebro = "Kartefant"; 
    }
    if ($row['Race'] == "1") {
	$logobro = "<img src='/files/images/gameclass/akkan-logo.png' width='50' height='65' alt='row'>";
	$racebro = "Merkhadia";
    }
    if ($row['Class'] == "1") { 
	$class = "Fighter";
	$picture = "<img src='/files/images/gameclass/icon/warrior.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/warrior.png' alt='row'>";
    } ;
    if ($row['Class'] == "2") {
        $class = "Rogue";
	$picture = "<img src='/files/images/gameclass/icon/assassin.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/assassin.png' alt='row'>";
    } ;
    if ($row['Class'] == "3") {
        $class = "Mage";
	$picture = "<img src='/files/images/gameclass/icon/sorcerer.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/sorcerer.png' alt='row'>";
    } ;
    if ($row['Class'] == "4") {
        $class = "Acolyte";
	$picture = "<img src='/files/images/gameclass/icon/enchanter.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/enchanter.png' alt='row'>";
    } ;
    if ($row['Class'] == "5") {
        $class = "Defender";
	$picture = "<img src='/files/images/gameclass/icon/defender.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/defender.png' alt='row'>";
    } ;
    if ($row['Class'] == "6") {
        $class = "Warrior";
	$picture = "<img src='/files/images/gameclass/icon/warrior.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/warrior.png' alt='row'>";
    } ;
    if ($row['Class'] == "7") {
        $class = "Assassin";
	$picture = "<img src='/files/images/gameclass/icon/assassin.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/assassin.png' alt='row'>";
    } ;
    if ($row['Class'] == "8") {
        $class = "Archer";
	$picture = "<img src='/files/images/gameclass/icon/archer.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/archer.png' alt='row'>";
    } ;
    if ($row['Class'] == "9") {
        $class = "Sorcerer";
	$picture = "<img src='/files/images/gameclass/icon/sorcerer.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/sorcerer.png' alt='row'>";
    } ;
    if ($row['Class'] == "10") {
        $class = "Enchanter";
	$picture = "<img src='/files/images/gameclass/icon/enchanter.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/enchanter.png' alt='row'>";
    } ;
    if ($row['Class'] == "11") {
        $class = "Priest";
	$picture = "<img src='/files/images/gameclass/icon/priest.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/priest.png' alt='row'>";
    } ;
    if ($row['Class'] == "12") {
        $class = "Cleric";
	$picture = "<img src='/files/images/gameclass/icon/cleric.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/cleric.png' alt='row'>";
    } ;
    if ($row['Class'] == "17") {
        $class = "Combatant";
	$picture = "<img src='/files/images/gameclass/icon/attacker.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/attacker.png' alt='row'>";
    } ;
    if ($row['Class'] == "18") {
        $class = "Officiator";
	$picture = "<img src='/files/images/gameclass/icon/rune.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/rune.png' alt='row'>";
    } ;
    if ($row['Class'] == "19") {
        $class = "Templar";
	$picture = "<img src='/files/images/gameclass/icon/templar.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/templar.png' alt='row'>";
    } ;
    if ($row['Class'] == "20") {
        $class = "Attacker";
	$picture = "<img src='/files/images/gameclass/icon/attacker.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/attacker.png' alt='row'>";
    } ;
    if ($row['Class'] == "21") {
        $class = "Gunner";
	$picture = "<img src='/files/images/gameclass/icon/gunner.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/gunner.png' alt='row'>";
    } ;
    if ($row['Class'] == "22") {
        $class = "Rune";
	$picture = "<img src='/files/images/gameclass/icon/rune.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/rune.png' alt='row'>";
    } ;
    if ($row['Class'] == "23") {
        $class = "Life";
	$picture = "<img src='/files/images/gameclass/icon/life.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/life.png' alt='row'>";
    } ;
    if ($row['Class'] == "24") {
        $class = "Shadow";
	$picture = "<img src='/files/images/gameclass/icon/shadow.png' alt='row'>";
	$badge = "<img src='/files/images/gameclass/badge/shadow.png' alt='row'>";
    } ;

	if ($row['HP'] >= 1000) {
   	$row['HP'] = floor($row['HP'] );
	}
	$formatted_hp = number_format($row['HP']);

	if ($row['MP'] >= 1000) {
   	$row['MP'] = floor($row['MP']);
	}
	$formatted_mp = number_format($row['MP']);

	if ($row['Mileage'] >= 1000) {
   	$row['Mileage'] = floor($row['Mileage']);
	}

	$formatted_medal = number_format($row['Mileage']);

	if ($row['Gold'] >= 1000) {
   	$row['Gold'] = floor($row['Gold']);
	}

	$formatted_gold = number_format($row['Gold']);

    echo "<div class='tableBlock-content'>";
    echo "<div class='tableBlock-conten_number'>" . $rank . "</div>
    	  <div class='tableBlock-conten_name'>".$picture." <a href>".$row['Name']." 

	<div class='tablePopup'>
	<span class='tablePopup-title'>".$row['Name']."</span>
	<div class='tablePopup-ava'> $badge </div>
	<div class='tablePopup-block'>
	<span>Level:</span> <span>" . $row['Level'] . "</span>
	</div>
	<div class='tablePopup-block'>
	<span>Class:</span> <span>$class</span>
	</div>
	<div class='tablePopup-block'>
	<span>Race:</span> <span>$racebro</span>
	</div>
	<div class='tablePopup-block'>
	<span>Sex:</span> <span>$Sex</span>
	</div>

	<div class='tablePopup-block'>
	<span>Gold :</span><span>$formatted_gold</span>
	</div>

	<div class='tablePopup-block'>
	<span>Medal :</span><span>$formatted_medal</span>
	</div>

	</div>
	</a></div>

                  <div class='tableBlock-conten_lvl'><span class='color-yellow'>" . $row['Level'] . "</div>
 	  <div class='tableBlock-conten_scr'>" . $row['Fame'] . "</div>";
    $rank++;
echo "</div>";
}
echo "</div>";
echo "</div>";
echo "	<div class='all-button'>
		<a href='/rankings/fame' class='button'>View All</a>
	</div>";

echo "</div>";

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
while ($row = odbc_fetch_array($stmt2))
  {
    if ($row['tnNationType'] == "1") { 
	$logobro = "<img src='/files/images/slide/human-logo.png' width='22' height='22'>";
	$racebro = "Kartefant"; 
    }
    if ($row['tnNationType'] == "2") {
	$logobro = "<img src='/files/images/slide/akkan-logo.png' width='22' height='22'>";
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