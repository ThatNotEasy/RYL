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

// Define pagination parameters
$resultsPerPage = 25;

// Get the current page from the query parameter, default to 1 if not set
$current_page = isset($_GET['page']) ? (int)$_GET['page'] : 1;

// Calculate the offset based on the current page and results per page
$offset = ($current_page - 1) * $resultsPerPage;

// SQL Query to select all columns from usertbl and order by OnlineTime in descending order with pagination
$sqlQuery = "SELECT *, 
                CAST(OnlineTime AS INT) AS TotalSeconds,
                CASE WHEN usertbl.uid = tblCurrentUser.uid THEN '[ Online ]' ELSE '' END AS OnlineStatus
             FROM usertbl 
             LEFT JOIN ROWPay.dbo.tblCurrentUser ON usertbl.uid = tblCurrentUser.uid
             WHERE usertbl.uid NOT IN ('1', '2') AND OnlineTime > 100
             ORDER BY TotalSeconds DESC 
             OFFSET $offset ROWS FETCH NEXT $resultsPerPage ROWS ONLY";

// Execute the query
$result = odbc_exec($Get_User, $sqlQuery);

if (!$result) {
    die("Error in executing SQL query: " . odbc_errormsg($Get_User));
}

// Initialize row number
$rowNumber = $offset + 1;

// Display the results in a table format
echo '<div class="table-row table-scroll">
                    <table class="rankingTable" width="100%">
                        <thead>';
                            echo '<tr>';
                                echo '<td>Place</td>';
                                echo '<td></td>';
                                echo '<td>Name</td>';
                                echo '<td>Join Time</td>';
                                echo '<td>Last Login</td>';
                                echo '<td>Total Online</td>';
                            echo '</tr>';
                        echo '</thead>
                        <tbody>';

// Fetch and display the results
while ($row = odbc_fetch_array($result)) {
    $onlineTimeSeconds = $row['OnlineTime'];
    $formattedTime = formatSecondsToHoursMinutesSeconds($onlineTimeSeconds);
    $jointime = strtotime($row['jointime']);
    $lastlogin = strtotime($row['lastlogin']);

    $jointimeFormatted = date('d-m-Y H:i', $jointime);
    $lastloginFormatted = date('d-m-Y H:i', $lastlogin);

    echo '<tr>';
    echo '<td>' . $rowNumber . '</td>';
    echo '<td>'. $row['OnlineStatus'] . '</td>';
    echo '<td>' . $row['account'] . '</td>';
    echo '<td>' . $jointimeFormatted . '</td>';
    echo '<td>' . $lastloginFormatted . '</td>';
    echo '<td>' . $formattedTime . '</td>';
    echo '</tr>';

    // Increment row number
    $rowNumber++;
}

echo '</tbody></table></div>';

// Calculate total pages
$totalPages = ceil(getTotalRows() / $resultsPerPage);

// Add pagination links
echo "<div class='pagination1'>";

// Limit the number of displayed page links
$maxPagesToShow = 5;

// Page numbers
$startPage = max(1, $current_page - floor($maxPagesToShow / 2));
$endPage = min($totalPages, $startPage + $maxPagesToShow - 1);

for ($i = $startPage; $i <= $endPage; $i++) {
    echo "<a class='number1 " . ($i == $current_page ? 'active1' : '') . "' href='?page=$i'>$i</a>";
}

echo "</div>";
echo '<p style="display: flex;justify-content: flex-end;margin-top: 20px;">Total Pages: ' . $totalPages . '</p>'; // Display total pages

echo "<div style='clear:both;'></div>"; // Ensure proper clearing

// Close the connection
odbc_close($Get_User);

// Function to format seconds to hours, minutes, and seconds
function formatSecondsToHoursMinutesSeconds($seconds) {
    $hours = floor($seconds / 3600);
    $minutes = floor(($seconds % 3600) / 60);
    //$seconds = $seconds % 60;

    $formattedTime = "";

    if ($hours > 0) {
        $formattedTime .= sprintf("%02d", $hours) . " Hours ";
    }
    if ($minutes > 0 || $hours > 0) {
        $formattedTime .= sprintf("%02d", $minutes) . " Minutes ";
    }
    //if ($seconds > 0 || ($hours === 0 && $minutes === 0)) {
    //    $formattedTime .= sprintf("%02d", $seconds) . " Seconds ";
    //}

    return $formattedTime;
}

// Function to get the total number of rows
function getTotalRows() {
    global $Get_User;
    $query = "SELECT COUNT(*) AS totalRows FROM usertbl WHERE OnlineTime > 3600";
    $result = odbc_exec($Get_User, $query);
    $row = odbc_fetch_array($result);
    return $row['totalRows'];
}

?>

</div>
</div>
</main>	
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	
