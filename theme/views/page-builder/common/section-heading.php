<?php if ( $headings['supertitle'] ) { ?>
	<div class="section_supertitle"
		 style="color:<?php echo esc_attr( $colors['supertitle'] ); ?>">
		<?php echo esc_html( $headings['supertitle'] ); ?></div>
<?php } ?>

<?php if ( $headings['title'] ) { ?>
	<h3 class="section_title"
		style="color:<?php echo esc_attr( $colors['title'] ); ?>">
		<?php echo esc_html( $headings['title'] ); ?></h3>
<?php } ?>

<?php if ( $headings['description'] ) { ?>
	<div class="section_description"
		 style="color:<?php echo esc_attr( $colors['title'] ); ?>">
		<?php echo esc_html( $headings['description'] ); ?></div>
<?php } ?>
