<section class="section-related-menu-widget">
    <?php
    if ( ! is_admin() ) {
        global $post;
        $menu_name = get_field( 'sidebar_menu_select', $post->ID );
        
        if ( $menu_name && 'none' !== $menu_name['label'] ) {
            echo $args['before_widget'];
            echo '<div class="widget__menu-title">' . $menu_name['label'] . ' Menu' . '</div>';
            ?>
            <div class="widget__menu-mobile-close"></div>
            <?php
            if ( $menu_name['label'] !== '0' ) {
                wp_nav_menu(
                    array(
                        'menu'        => $menu_name['value'],
                        'container'   => 'false',
                        'menu_class'  => 'widget__menu-menu',
                        'link_before' => '<span class="menu-item-text">',
                        'link_after'  => '</span>' .
                                         '<span class="menu-item-text__arrow"></span>'

                    )
                );
            }
            echo $args['after_widget'];
        }
    }
    ?>
</section>