<?php if( have_rows('hero_insolvency_landing_cd') ): ?>
	<?php while( have_rows('hero_insolvency_landing_cd') ): the_row(); ?>
<section class="section-landing-insolvency-hero <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) || get_sub_field( 'background_color' ) ) { ?> style="<?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?> <?php if ( get_sub_field( 'background_color' ) ) { ?> background-color: <?php the_sub_field( 'background_color' );?>; <?php } ?>
        "<?php } ?>>
	<div class="container">
		<div class="row">
            <div class="col-12 hero-header">
                <div class="site-branding">
		            <?php the_custom_logo(); ?>
                </div>
                <div class="logo-right">
	                <?php echo wp_get_attachment_image( get_sub_field( 'logo_right' ), 'full', false,  ["class" => "logo-right"] ); ?>
                </div>
            </div>
			<div class="col-5">
				<h1 class="hero-page-title">
					<?php the_sub_field( 'title' ); ?>
				</h1>
				<div class="hero-description">
					<?php the_sub_field( 'wysiwyg_left' ); ?>
				</div>
				<div class="logos">
					<?php
					// check if the repeater field has rows of data
					if ( have_rows('logos_left') ):
						// loop through the rows of data
						while ( have_rows('logos_left') ) : the_row();
							// display a sub field value
							?>
							<div class="box-image">
								<?php echo wp_get_attachment_image( get_sub_field( 'logo' ), 'full', false,  ["class" => "logo-box"] ); ?>
							</div>
						<?php
						endwhile;
					endif;
					?>
				</div>
			</div>
			<div class="col-7">
                <?php echo wp_get_attachment_image( get_sub_field( 'bcg_right' ), 'full', false,  ["class" => "shape-img"] ); ?>
                <div class="sliders-form-wrapper">
                    <div class="form-sliders">
                        <div class="quiz__container">
                            <h3 class="quiz-title">GET A QUOTE</h3>
                        </div>
                        <div class="quiz__content">
                            <div class="quiz__tab-heading">Liabilities</div>
                            <p>Use the sliders below to show the value of how much money your company owes</p>
                            <div class="slider">
                                <div class="slider__title">
                                    <label for="quiz__amount-bank" class="quiz__amount-heading">Bank</label>
                                    <span class="quiz__amount quiz__amount-bank" id="quiz__amount-bank">£0</span>
                                </div>
                                <div class="slider-range-noUI-container">
                                    <div id="slider-range-bank" class="slider-range-noUI"></div>
                                </div>
                            </div>
                            <div class="slider">
                                <div class="slider__title">
                                    <label for="quiz__amount-hmrc" class="quiz__amount-heading">HMRC</label>
                                    <span class="quiz__amount quiz__amount-hmrc" id="quiz__amount-hmrc">£0</span>
                                </div>
                                <div class="slider-range-noUI-container">
                                    <div id="slider-range-hmrc" class="slider-range-noUI"></div>
                                </div>
                            </div>
                            <div class="slider">
                                <div class="slider__title">
                                    <label for="quiz__amount-creditors" class="quiz__amount-heading">Other Creditors</label>
                                    <span class="quiz__amount quiz__amount-creditors" id="quiz__amount-creditors">£0</span>
                                </div>
                                <div class="slider-range-noUI-container">
                                    <div id="slider-range-creditors" class="slider-range-noUI"></div>
                                </div>
                            </div>
                            <div class="quiz__tab-heading">Assets and Cash at Bank</div>
                        <p>Use the siders below to show the estimated value of your company's assets and cash at bank</p>
                            <div class="slider">
                                <div class="slider__title">
                                    <label for="quiz__amount-assets" class="quiz__amount-heading">ASSETS</label>
                                    <span class="quiz__amount quiz__amount-assets" id="quiz__amount-assets">£0</span>
                                </div>
                                <div class="slider-range-noUI-container">
                                    <div id="slider-range-assets" class="slider-range-noUI"></div>
                                </div>
                            </div>
                            <div class="slider">
                                <div class="slider__title">
                                    <label for="quiz__amount-cash-at-bank" class="quiz__amount-heading">Cash at bank</label>
                                    <span class="quiz__amount quiz__amount-cash-at-bank" id="quiz__amount-cash-at-bank">£0</span>
                                </div>
                                <div class="slider-range-noUI-container">
                                    <div id="slider-range-cash-at-bank" class="slider-range-noUI"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="form-wrapper">
                        <div> [gravityform id="40" title="false" description="false" ajax="true" tabindex="49" field_values="check=First Choice,Second Choice"]  </div>
                    </div>
                </div>
			</div>
		</div>

	</div>
</section>
<section class="section-floater">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="floater-inner">
			        <?php
			        // check if the repeater field has rows of data
			        if ( have_rows('floating_block') ):
				        // loop through the rows of data
				        while ( have_rows('floating_block') ) : the_row();
					        // display a sub field value
					        ?>
                            <div class="float-feature-item">
                                <img src="<?php echo get_template_directory_uri(); ?>/assets/images/landing-checkmark.png" alt="" class="check-icon">
                                <p>
							        <?php the_sub_field( 'text' ); ?>
                                </p>
                            </div>
				        <?php
				        endwhile;
			        endif;
			        ?>
                </div>
            </div>
        </div>
    </div>
</section>
	<?php endwhile;
endif ?>

<?php //CD\Core\Assets::get_instance()->enqueue_scripts( ['cd-old-quiz-insolvency'] ); ?>