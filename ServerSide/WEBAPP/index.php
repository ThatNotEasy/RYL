<?php
include "files/inc/modules/header.php";
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

					<?php include "files/inc/modules/navbar.php"; ?>

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
<a href=""><img src="files/images/row-new3.png" alt="" class="bright"></a>
</div>
<?php include "files/inc/modules/download.php"; ?>
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
<main>	



					<?php include "files/inc/modules/slider.php"; ?>	

					<?php include "files/inc/modules/news.php"; ?>


					<span class="line"></span>
										
					<div class="mainHomeBlock flex-s">


						<?php include "files/inc/modules/top.players.php"; ?>
					</div>
					<div class="mainHomeBlock flex-s">

						<?php include "files/inc/modules/top.guilds.php"; ?>
					</div>
						<?php include "files/inc/modules/social.php"; ?>	

					</div>
<?php include "files/inc/modules/bigslide.php"; ?>	
<span class="line"></span>
<?php include "files/inc/modules/media.php"; ?>
</div>
</div>
</main>	
</div>	
<?php include "files/inc/modules/footer.php"; ?>	