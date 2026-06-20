<?php if ( is_singular() ) : ?>
<section id="toc">
    <?php 
    if ( ! wp_is_mobile() && ! is_front_page() && ! is_home() && ( ( is_singular( 'post' ) && get_field( 'toc_enabled' ) ) || ( is_singular( 'page' ) && '' === get_page_template_slug() ) ) ) {
        global $post;

		$toc        = new CD\Content\Toc( $post->post_content );
		$toc_markup = $toc->getToc( true );

        echo wp_kses_post( $toc_markup );
	}
    ?>
</section>
<?php endif; ?>