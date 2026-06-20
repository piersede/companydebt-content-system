<?php

namespace CD\Widgets;

//use Cd20\Theme\Content as Content;

class Table_Of_Content extends \WP_Widget {
	public function __construct() {
		parent::__construct(
			'CD_Table_Of_Content_Widget',
			__( 'CD TOC Widget', 'cd20' ),
			array(
				'description' => __( 'Displays Table of Content', 'cd20' ),
				'classname'   => 'widget__toc'
			)
		);
	}

	public function widget( $args, $instance ) {
		$toc = new Content\Toc( get_the_content() );

		if ( $toc->count > 0 ) {
			?>
			<section class="widget  widget__toc">
				<div class='toc'>
					<div class='toc__heading  active'>Table of Contents</div>
					<?php echo $toc->getToc(); ?>
				</div>
			</section>

			<?php
		}
	}
}
