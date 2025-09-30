<?php

session_start();
error_reporting(0);


if (!isset($_SESSION["UID"])) {
    echo '<script>alert("Please login")</script>';
    echo '<script>window.location.href = "/pages/login";</script>';
}

$UID = $_SESSION["UID"];


#echo "<script>alert(" . $UID . ")</script>";

include "../include/database.config.php";
include "../files/inc/modules/header.php";

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
							<div class="content"><div>	
 <?php

 $stmt = odbc_prepare($Get_Donate, 'SELECT * FROM SellItem WHERE Type IN (1) ORDER BY CreateID ASC');
 $result = odbc_execute($stmt, array(0));
		echo '		<div class="h2-title h2-title-content flex-s-c"><span>Item shop</span></div>
		<div class="table-row table-scroll">
		<table class="table table-condensed table-hover table-striped">';
                while ($Data = odbc_fetch_array($stmt)) {

		 ?>
		<thead>
		<tr>			
               		 <th colspan="2" style="float: left; color: #a97fff; text-shadow: 0 0 8px #9966ff"> <br> &nbsp;<?= $Data['ItemName'] ?>  </th>
               		 <th> <br><br></th>
		</tr>
		</thead>
		<tbody>
		<tr>	
		<td style="width:25%;"><img src="/files/images/<?= $Data['Photo_URL'] ?>" alt=""></td>	
                      	<td style="width:100%; color: white;"><?= $Data["ItemInfo"] ?></td>
		</tr>
		<tr>
	    	<td style="width:25%;">Quantity : <?= $Data['Amount'] ?> </td>
                    	<td style="width:100%; color: #a97fff">Price : <?= $Data['Price'] ?></td>	
		</tr>


		<tr>
<td style="width:25%;"></td>
<td style="width:100%; color: #a97fff">
			<a href="buy?pid=<?= $Data['CreateID'] ?>" class="button" style="float: right;"> 
			Buy Now!</a>
</td>
		</tr>

                <?php } ?>
		</tbody>
		</table>	



</div>
</div>
</div>
</div>
</main>
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	