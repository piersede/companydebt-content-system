<?php
$title = get_field('cta_title') ?: 'Find out what liquidation would cost';
$description = get_field('cta_description') ?: 'Complete the form to get a clear cost estimate and understand the next steps. 100% confidential. No obligation.';
$button_text = get_field('cta_button_text') ?: 'Get a Quote';
$button_link = get_field('cta_button_link') ?: '/quick-quote/';
?>
<div class="cd-cost-cta">
    <div class="cd-cost-cta__content">
        <div class="cd-cost-cta__title"><?php echo esc_html( $title ); ?></div>
        <div class="cd-cost-cta__desc"><?php echo esc_html( $description ); ?></div>
    </div>
    <div class="cd-cost-cta__action">
        <a href="<?php echo esc_url( $button_link ); ?>" class="cd-cost-cta__button"><?php echo esc_html( $button_text ); ?></a>
    </div>
</div>