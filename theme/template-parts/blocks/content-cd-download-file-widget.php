<?php
if( get_field('style') === 'default' ) { ?>

<section class="section-widget-download">
    <a href="<?php the_field( 'button_link' ); ?>">
       <div class="widget-download-inner">
           <div class="widget-download-eyebrow">Free Download</div>
           <div class="widget-download-row">
               <div class="widget-download-img">
                   <?php echo wp_get_attachment_image( 79739, 'medium', false, ["class" => "download-pdf-img", "alt" => "Stressed Directors Guide"] ); ?>
               </div>
               <div class="widget-download-text">
                   <div class="title">Stressed Directors Guide</div>
                   <div class="widget-download-desc">Practical steps for cash flow, creditor threats, and closure</div>
               </div>
           </div>
           <div class="button widget-download-button">Download the Guide</div>
           <div class="widget-download-subtext">100% Free &middot; Regularly Updated</div>
       </div>
    </a>
</section>
<?php } ?>
<?php
    if( get_field('style') === 'design22' ) { ?>
        <section class="section-widget-download-design22">
            <div class="title"><?php the_field( 'title' ); ?></div>
            <div class="widget-content">
	            <?php echo wp_get_attachment_image( 79739, 'medium', false, ["class" => "download-pdf-img", "alt" => "Stressed Directors Guide"] ); ?>
                <div class="button widget-download-button">
                    <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/icon-pdf.png' ) ?>" alt="5 Starts" width="30" height="30">
                    <div class="button-text"><?php the_field( 'button_text' ); ?></div>
                </div>
            </div>
        </section>
<?php } ?>
<div class="section-widget-download-popup-wrapper">
    <div class="section-widget-download-popup">
        <div class="download-popup-heading">
            <div class="download-popup-widget-close"><img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/icon-cancel-48.png' ) ?>" alt="5 Starts" width="30" height="30">
            </div>
        </div>
	    <?php if( have_rows('popup') ): ?>
	    <?php while( have_rows('popup') ): the_row();  ?>
        <div class="inner-row">
            <div class="left-content">
                <div class="popup-title"><?php the_sub_field( 'title' ); ?></div>
                <div class="popup-desc"><?php the_sub_field( 'description' ); ?></div>
	               <div class="form">[gravityform id="<?php echo do_shortcode( get_sub_field( 'form_id' ) ); ?>" title="false" description="false"]</div>
                </div>
                <div class="right-image">
	                <?php echo wp_get_attachment_image( 79739, 'medium', false, ["class" => "download-pdf-img", "alt" => "Stressed Directors Guide"] ); ?>
                </div>
        </div>
	        <?php endwhile;

	        endif ?>
    </div>
</div>