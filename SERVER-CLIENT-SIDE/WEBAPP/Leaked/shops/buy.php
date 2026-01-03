<?php
session_start();
error_reporting(0);


if (!isset($_SESSION["UID"])) {
    echo '<script>alert("Please login")</script>';
    echo '<script>window.location.href = "/pages/login";</script>';
}

$UID = $_SESSION["UID"];
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
include "../include/get.account.php";
?>

<body>
	<div class="h2-title h2-title-content flex-s-c"><span>Buy item</span></div>
	<div class="table-row table-scroll">
	<table class="table table-condensed table-hover table-striped">
                <form class="form-horizontal" action="" method="post">
                    <?php
                    $PID = $_GET['pid'];
                    $stmt = odbc_prepare($Get_Donate, 'SELECT * FROM SellItem WHERE CreateID = ?');
                    $result = odbc_execute($stmt, array($PID));
                    $Data = odbc_fetch_array($stmt);

                    $ProductPrice =  $Data['Price'];
                    $ProductProtoypeID =  $Data['ItemPrototypeID'];
                    $Amount = $Data['Amount'];

                    ?>


<div class="container">
<div class="accBlock flex">
<div style="flex: 1 1 0% !important;">
<div class="formGroup" style>
<span>Select your character</span>
<select name="bankcode" style="height:58px !important">
<pre style="
    padding: 30px 25px;
    background-color: rgb(6, 21, 38);
    color: rgb(214, 222, 235);
    border-radius: 6px;
    font-size: 14px;
    overflow: auto;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;
    word-wrap: normal;
    tab-size: 4;
    line-height: 1.4;
    text-align: left;
  ">
<code style="font-family: JetBrains Mono, Menlo, Monaco, monospace;"><span style="color: #999;">undefined</span></code></pre>
<option value="0">
                                <?php
                                include "../include/database.config.php";
                                $stmt = odbc_prepare($Get_Game, '
                            SELECT CharInfox.Name as Name,CharInfox.CID as CID
                    
                            FROM UserInfo as UserInfox
                            
                            JOIN CharInfo as CharInfox
                            
                            ON UserInfox.Char1 = CharInfox.CID
                            OR UserInfox.Char2 = CharInfox.CID
                            OR UserInfox.Char3 = CharInfox.CID
                            OR UserInfox.Char4 = CharInfox.CID
                            OR UserInfox.Char5 = CharInfox.CID
                            
                            WHERE UID = ?
                            ');
                                $result = odbc_execute($stmt, array($UID));

                                while ($data = odbc_fetch_array($stmt)) {
                                    echo '<option value="' . $data['CID'] . '">' . $data['Name'] . '</option>';
                                }


                                ?>
</option>
</select>
</div>
</div>
<div>
<div class="formGroup" style>
<span> Points</span>
<div class="fieldGroup-input" style="width: fit-content !important; height:58px !important"><?= GetPoint($UID) ?></div>
</div>
</div>
</div>
                    <?php

                    if (isset($_POST['bankcode'])) {
                        //echo $_POST['bankcode'];
                        $CID = $_POST['bankcode'];
                        if ($CID == 0) {
                            echo '<div class="alert-warning"><span class="closebtn">&times;</span><strong>Failed!</strong> Please select your character !!
			</div>';
                           echo '<script>setTimeout(function(){ window.location.href = window.location.href; }, 5000);</script>';
                            die();
                        }
                        if (GetPoint($UID) < $ProductPrice) {
                            echo '<div class="alert-warning"><span class="closebtn">&times;</span><strong>Failed!</strong> Not enough point !!
			</div>';
                            die();
                        } else {
                            DeductPoint(GetPoint($UID), $ProductPrice);
                        }
                    }

                    function DeductPoint($CurentPoint, $ProductPrice)
                    {
                        global $UID;
                        global $CID;
                        global $Amount;
                        global $ProductProtoypeID;

                        if (true == SetPoint($CurentPoint - $ProductPrice, $UID)) {
                             //echo '<p style="color:red;">Not enough point to buy this item</p>';

                            InsertItem($UID, $CID, $ProductProtoypeID, $Amount);
                        } else {
                            echo "<div class='alert-warning'><span class='closebtn'>&times;</span><strong>Failed!</strong> Failed to Points !!
			</div>";
	            echo "<script>setTimeout(function(){ window.location.href = window.location.href; }, 5000);</script>";
                        }
                    }

                    function InsertItem($UID, $CID, $ProtoypeID, $Amount)
                    {
                        global $Get_Game;
                        $stmt = odbc_prepare($Get_Game, 'INSERT INTO TblWebItemInfo (UID,CID,ItemPrototypeID,Amount) VALUES (?,?,?,?)');
                        $result = odbc_execute($stmt, array($UID, $CID, $ProtoypeID, $Amount));
                        $status = odbc_num_rows($stmt);

                        if ($status > 0)
	              echo '<div class="alert-success"><span class="closebtn">&times;</span><strong>Done!</strong> Item purchase success . Have fun!
			</div>';
	              echo '<script>setTimeout(function(){ window.location.href = window.location.href; }, 5000);</script>';
   	            //echo '<script>alert("Item purchase success !"); window.location.href = window.location.href;</script>';
                    }

                    ?>

		<thead>
		<tr>			
               		 <th colspan="2" style="float: left; font-size: 16px; color: #a97fff; text-shadow: 0 0 8px #9966ff"> <br> &nbsp;&nbsp;&nbsp; <?= $Data['ItemName'] ?>  </th>
               		 <th> <br><br></th>
		</tr>
		</thead>
<tbody>
<tr>	
		<td style="width:30%;"><img src="/files/images/<?= $Data['Photo_URL'] ?>" alt=""></td>	
                      	<td style="width:100%; color: white;"><?= $Data["ItemInfo"] ?></td>
</tr>
<tr>
	      <td style="width:30%;">Quantity : <?= $Data['Amount'] ?> </td>
                       <td style="width:100%; color: #a97fff">Price : <?= $Data['Price'] ?></td>
	

</tr>
</table>
<button type="submit" class="button" style="float: right;">Purchase</button>

</form>
</div>
</div>
</div>
</div>
</main>
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	