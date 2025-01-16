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
<div class="content">
<div class="h2-title h2-title-content flex-s-c">	
<span>Charge Cash Points</span>
</div>
<h2>"Cash Point" or also "Points" is a digital currency used in the KingOfFighter Item Mall. It's not a physical product. Once charged, you can use these points to purchase premium items for the game.</h2>
<h2>Before purchasing points, ensure you've read and fully understood with our <a href="/pages/tos" target="_blank">terms of services</a> and <a href="/pages/refund-policy" target="_blank">refund policy</a>. Proceeding with the purchase indicates your agreement to these terms. If you're not in agreement, please refrain from buying.</h2>
<div class="hero flex-s">
<div class="row" style="margin-bottom: 15px;">


<div class="heroLeft block-6">
<div class="heroLeft-img flex-c-c">
<img src="../files/images/pack1.png" alt width="90%" height="90%">
</div>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" onSubmit="return OpenWindow('1')" target="POPWIN">
<div class="heroLeft-button">
<span style="color:orange">1000 Cash Points</span>
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="mrjulianzzz@live.com">
<input type="hidden" name="item_name" value="1000 Cash Points">
<input type="hidden" name="item_number" value="1">
<input type="hidden" name="amount" value="10.00">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="return" value="success link should be here">
<input type="hidden" name="cancel_return" value="cancle return link should be here">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="lc" value="US">
<input type="hidden" name="bn" value="PP-BuyNowBF">
<input type="hidden" name="custom" value="<?echo ''.$_SESSION['UID'].'';?>">
<button type="submit" class="big-button-blue">Pay using Paypal</button>
</div>
</form>
</div>


<div class="heroLeft block-6">
<div class="heroLeft-img flex-c-c">
<img src="../files/images/pack2.png" alt width="90%" height="90%">
</div>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" onSubmit="return OpenWindow('1')" target="POPWIN">
<div class="heroLeft-button">
<span style="color:orange">2100 Cash Points</span>
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="mrjulianzzz@live.com">
<input type="hidden" name="item_name" value="2100 Cash Points">
<input type="hidden" name="item_number" value="1">
<input type="hidden" name="amount" value="20.00">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="return" value="success link should be here">
<input type="hidden" name="cancel_return" value="cancle return link should be here">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="lc" value="US">
<input type="hidden" name="bn" value="PP-BuyNowBF">
<input type="hidden" name="custom" value="<?echo ''.$_SESSION['UID'].'';?>">
<button type="submit" class="big-button-blue">Pay using Paypal</button>
</div>
</form>
</div>
</div>


<div class="row" style>
<div class="heroLeft block-6">
<div class="heroLeft-img flex-c-c">
<img src="../files/images/pack3.png" alt width="90%" height="90%">
</div>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" onSubmit="return OpenWindow('1')" target="POPWIN">
<div class="heroLeft-button">
<span style="color:orange">5500 Cash Points</span>
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="mrjulianzzz@live.com">
<input type="hidden" name="item_name" value="5500 Cash Points">
<input type="hidden" name="item_number" value="1">
<input type="hidden" name="amount" value="50.00">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="return" value="success link should be here">
<input type="hidden" name="cancel_return" value="cancle return link should be here">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="lc" value="US">
<input type="hidden" name="bn" value="PP-BuyNowBF">
<input type="hidden" name="custom" value="<?echo ''.$_SESSION['UID'].'';?>">
<button type="submit" class="big-button-blue">Pay using Paypal</button>
</div>
</form>
</div>


<div class="heroLeft block-6">
<div class="heroLeft-img flex-c-c">
<img src="../files/images/pack4.png" alt width="90%" height="90%">
</div>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" onSubmit="return OpenWindow('1')" target="POPWIN">
<div class="heroLeft-button">
<span style="color:orange">13000 Cash Points</span>
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="mrjulianzzz@live.com">
<input type="hidden" name="item_name" value="13000 Cash Points">
<input type="hidden" name="item_number" value="1">
<input type="hidden" name="amount" value="100.00">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="return" value="success link should be here">
<input type="hidden" name="cancel_return" value="cancle return link should be here">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="lc" value="US">
<input type="hidden" name="bn" value="PP-BuyNowBF">
<input type="hidden" name="custom" value="<?echo ''.$_SESSION['UID'].'';?>">
<button type="submit" class="big-button-blue">Pay using Paypal</button>
</div>
</form>
</div>


</div>
</div>
</div>
</main>
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	