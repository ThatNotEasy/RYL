<?php

add_hook('core/headermenu', 'plugin_headermenu');

function plugin_headermenu($version) {
    return array(
        array('#index.php', 'Login'),
    );
}