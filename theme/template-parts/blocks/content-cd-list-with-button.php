<div class="content-cd-list-with-button">
    <div class="cd-test-eyebrow">30-Second Test</div>
    <h3>Free Insolvency Test</h3>
    <div class="cd-list-with-button-desc">Answer a few quick questions to get instant clarity, next steps, and free expert advice</div>

    <div class="cd-test-phone-mockup" role="img" aria-label="Insolvency test preview"></div>

    <?php if ( get_field( 'cd_list_with_button_label' ) && get_field( 'cd_list_with_button_link' ) ) : ?>
        <div class="cd-test-cta-wrap">
            <a href="<?php the_field( 'cd_list_with_button_link' ); ?>">Take the Free Test</a>
            <div class="cd-test-subtext">Takes 30 Seconds &middot; No Signup Required</div>
        </div>
    <?php endif; ?>
</div>