<?php if (!defined('EXEC_TIME')) die('Access restricted!');

$current_dir = dirname(__FILE__);

do
{
    // Add Comment -----------------------------------------------------------------------------------------------------
    if (isset($allow_add_comment) && $allow_add_comment)
    {
        $break = include ("$current_dir/add_comment.php");
        if ($break === FALSE) { $CN_HALT = TRUE; break; }
    }

    // Show Full Story -------------------------------------------------------------------------------------------------
    if (isset($allow_full_story) && $allow_full_story)
    {
        $break = include ("$current_dir/full_story.php");
        if ($break === FALSE) { $CN_HALT = TRUE; break; }
    }

    // Show Comments ---------------------------------------------------------------------------------------------------
    if (isset($allow_comments) && $allow_comments)
    {
        $break = include ("$current_dir/comments.php");
        if ($break === FALSE) { $CN_HALT = TRUE; break; }
    }

    // Active News -----------------------------------------------------------------------------------------------------
    if (isset($allow_active_news) && $allow_active_news)
    {
        $break = include ("$current_dir/active_news.php");
        if ($break === FALSE) { $CN_HALT = TRUE; break; }
    }
}
while (FALSE);

// ---------------------------------------------------------------------------------------------------------------------
if ((!isset($count_cute_news_includes) or !$count_cute_news_includes) and $template != 'rss')
{

}

if(isset($count_cute_news_includes)) $count_cute_news_includes++;