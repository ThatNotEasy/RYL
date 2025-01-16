<?php

    require_once("../admincp/cn_api.php");
	$entry = cn_api_get_entry();

    //$template = 'bootstrap'; // for test

    // Play with settings --------------------------------------------------
    $pw = REQ('pw');

    $theme = 'cosmo'; // default theme

    if (isset($pw['PHP_SELF']) && $pw['PHP_SELF']) $PHP_SELF = $pw['PHP_SELF'];
    if (isset($pw['template']) && $pw['template']) $template = $pw['template'];
    if (isset($pw['theme']) && $pw['theme']) $theme = $pw['theme'];

    if (isset($pw['start_from']) && $pw['start_from']) $start_from = $pw['start_from'];
    if (isset($pw['number']) && $pw['number']) $number = $pw['number'];
    if (isset($pw['archive']) && $pw['archive']) $archive = $pw['archive'];
    if (isset($pw['category']) && $pw['category']) $category = $pw['category'];
    if (isset($pw['ucat']) && $pw['ucat']) $ucat = $pw['ucat'];
    if (isset($pw['sortby']) && $pw['sortby']) $sortby = $pw['sortby'];
    if (isset($pw['dir']) && $pw['dir']) $dir = $pw['dir'];
    if (isset($pw['page_alias']) && $pw['page_alias']) $page_alias = $pw['page_alias'];
    if (isset($pw['tag']) && $pw['tag']) $tag = $pw['tag'];
    if (isset($pw['user_by']) && $pw['user_by']) $user_by = $pw['user_by'];

    if (isset($pw['static']) && $pw['static']) $static = $pw['static'];
    if (isset($pw['reverse']) && $pw['reverse']) $reverse = $pw['reverse'];
    if (isset($pw['only_active']) && $pw['only_active']) $only_active = $pw['only_active'];
    if (isset($pw['no_prev']) && $pw['no_prev']) $no_prev = $pw['no_prev'];
    if (isset($pw['no_next']) && $pw['no_next']) $no_next = $pw['no_next'];
    // ---------------------------------------------------------------------

    if (isset($_GET['do'])&& $_GET['do'] == "rss") include("rss.php");
?>
<?php
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
<div class="content"><div>
<div class="h2-title h2-title-content flex-s-c"><span>News</span></div><h2>
</div>
 <div class="row news-article">
</div>
<div class="col-xs-7 news-content">

                <?php

                /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Here we decide what page to include
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
                if (isset($_GET['search']) && $_GET['search']) {
                    include ("search.php");
                }
                else if (isset($_GET['do']) && $_GET['do'] == 'archives') {
                    include ("show_archives.php");
                }
                else if (isset($_GET['do']) && $_GET['do'] == "stats") {
                    echo "You can download the stats addon and include it here to show how many news, comments ... you have"; // include("$path/stats.php");
                } else {
                    include ("../admincp/show_news.php");
                }
                ?>


</main>
</div>	
<?php include "../files/inc/modules/footer.php"; ?>	