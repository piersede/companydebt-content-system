<?php
/**
 * Plugin Name: CD FAQ Schema
 * Description: Emits FAQPage JSON-LD for singular pages that use the Ultimate
 *   Blocks content-toggle accordion. WordPress KSES strips inline <script>
 *   (JSON-LD) from post content, so the structured data is injected in wp_head
 *   here instead. Parsed live from the post content, so it always matches the
 *   visible Q&A. Reusable across any page with the accordion.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'wp_head', function () {
    if ( ! is_singular() ) {
        return;
    }
    $post = get_post();
    if ( ! $post || strpos( $post->post_content, 'wp:ub/content-toggle-panel-block' ) === false ) {
        return;
    }

    $pattern = '/<!--\s*wp:ub\/content-toggle-panel-block\s*(\{.*?\})\s*-->(.*?)<!--\s*\/wp:ub\/content-toggle-panel-block\s*-->/s';
    if ( ! preg_match_all( $pattern, $post->post_content, $matches, PREG_SET_ORDER ) ) {
        return;
    }

    $faqs = array();
    foreach ( $matches as $panel ) {
        $attrs = json_decode( $panel[1], true );
        if ( empty( $attrs['panelTitle'] ) ) {
            continue;
        }
        $question = trim( wp_strip_all_tags( $attrs['panelTitle'] ) );
        $answer   = trim( wp_strip_all_tags( preg_replace( '/<!--.*?-->/s', ' ', $panel[2] ) ) );
        if ( $question === '' || $answer === '' ) {
            continue;
        }
        $faqs[] = array(
            '@type'          => 'Question',
            'name'           => $question,
            'acceptedAnswer' => array(
                '@type' => 'Answer',
                'text'  => $answer,
            ),
        );
    }

    if ( empty( $faqs ) ) {
        return;
    }

    $schema = array(
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        'mainEntity' => $faqs,
    );

    echo "\n" . '<script type="application/ld+json">'
        . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
        . '</script>' . "\n";
}, 20 );
