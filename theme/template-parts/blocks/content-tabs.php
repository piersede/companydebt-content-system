<section class="tabs-section container ">
    <p class="tabs-title"><?php the_field( 'tabs_title' ); ?></p>
    <div class="tabbed__page-header--buttons">
        <div class="tabs__buttons">
            <?php
            $page_tabs = get_field( 'tabs' );
            foreach ( $page_tabs as $index => $single_tab ) :
                ?>
                <div class="tab__link--container <?php echo 0 === $index ? 'active' : ''; ?>" data-value="tab-<?php echo $index; ?>">
                    <?php echo wp_get_attachment_image( $single_tab['tab_image']['id'], '', '', array( 'class' => 'tab__image attachment-tab__image' ) ); ?>
                    <div class="tab__link"><?php echo $single_tab['tab_title']; ?></div>
                </div>
                <?php
            endforeach;
            ?>
        </div>
    </div>
    <div class="tabs__content">
        <?php
        foreach ( $page_tabs as $index => $single_tab ) : ?>
            <div class="tab__content  tab-<?php echo esc_attr( $index ); ?> <?php echo 0 === $index ? 'active' : ''; ?>">
<!--                <h2 class="tab__page-title">--><?php //echo esc_attr( $single_tab['tab_post']->post_title ); ?><!--</h2>-->
                <?php
                    $tab_post_id  = $single_tab['tab_post']->ID;
                    $content_post = get_post( $tab_post_id );
                    $content      = $content_post->post_content;
                    $content      = new CD\Content\Footnotes( $content );
                    $content      = $content->getPostFootnotesMarkup();
                    $content      = apply_filters( 'the_content', $content );
                    $content      = str_replace( ']]>', ']]&gt;', $content );
                    echo wp_kses_post( $content );
                ?>
            </div>
        <?php endforeach; ?>
    </div>
</section>