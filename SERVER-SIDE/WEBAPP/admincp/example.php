<?php

    require_once("cn_api.php");
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
<html>

<body>

   <section id="blog">

        <div class="container">
            <div class="col-sm-8">

                <div class="nav nav-tabs">
                    <?php

                    $_self_page = explode('/', PHP_SELF);
                    $_self_page = $_self_page[count($_self_page)-1];
                    if ($_self_page[0] === '/') { $_self_page = substr($_self_page, 1); }
                    $_self_page = getoption('http_script_dir') . '/' . $_self_page;

                    ?>
                    <b>Navigation</b>:
                    <a href="<?php echo $_self_page; ?>">Main page</a> |
                    <a href="<?php echo $_self_page; ?>?do=archives">Archives</a> |
                    <a href="<?php echo $_self_page; ?>?do=rss">RSS</a> |
                    <a href="<?php echo $_self_page; ?>?do=stats">Stats</a> |
                </div>

                <!-- MAIN CONTENT, FIRST -->

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
                    include ("show_news.php");
                }
                ?>

            </div>

    </section>

</body>
</html>