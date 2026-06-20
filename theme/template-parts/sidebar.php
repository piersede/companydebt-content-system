<?php
switch ( $args['selected_sidebar'] ) {
	case 'sidebar-primary':
		$sidebar_class = 'sidebar--default';
		break;

	case 'custom-sidebar-1':
		$sidebar_class = 'sidebar--contact';
		break;

	case 'custom-sidebar-2':
		$sidebar_class = 'sidebar-menu';
		break;

	case 'sidebar-take-the-test':
		$sidebar_class = 'sidebar--take-the-test';
		break;
	default:
		$args['selected_sidebar'] = 'sidebar-primary';
		$sidebar_class            = 'sidebar--default';

}
?>

<div class="sidebar  <?php echo esc_attr( $sidebar_class ); ?>"
     style="padding-bottom: 15px">
	<?php dynamic_sidebar( $args['selected_sidebar'] ); ?>
</div>
