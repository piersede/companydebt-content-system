<?php
/**
 * The sidebar containing the main widget area for the Take The Test template
 *
 * Renders the sidebar-take-the-test widget area, filtering out
 * the section sidebar menu (block-22) and empty block (block-21)
 * so only the 6 approved widgets display on every page.
 *
 * @package CompanyDebt
 */

if ( ! is_active_sidebar( 'sidebar-take-the-test' ) ) {
	return;
}

/**
 * Filter out section sidebar menus and empty blocks from the take-the-test sidebar.
 */
function cd_filter_take_the_test_sidebar_widgets( $sidebars_widgets ) {
	if ( isset( $sidebars_widgets['sidebar-take-the-test'] ) ) {
		$sidebars_widgets['sidebar-take-the-test'] = array_filter(
			$sidebars_widgets['sidebar-take-the-test'],
			function( $widget_id ) {
				$hidden = array( 'block-21', 'block-22' );
				return ! in_array( $widget_id, $hidden, true );
			}
		);
	}
	return $sidebars_widgets;
}
add_filter( 'sidebars_widgets', 'cd_filter_take_the_test_sidebar_widgets' );
?>

<aside id="secondary" class="widget-area">
	<?php dynamic_sidebar( 'sidebar-take-the-test' ); ?>
</aside><!-- #secondary -->

<?php
remove_filter( 'sidebars_widgets', 'cd_filter_take_the_test_sidebar_widgets' );
?>
