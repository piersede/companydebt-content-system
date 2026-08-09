<?php
/**
 * One-shot WP post updater. Trigger: ?cdpush=f9cf70c59dbf
 * Self-deletes after run.
 */
if (!isset($_GET['cdpush']) || $_GET['cdpush'] !== 'f9cf70c59dbf') {
    return;
}

add_action('init', function() {
    $payload_path = __DIR__ . '/mu-cd-push-f9cf70c59dbf.json';
    if (!file_exists($payload_path)) {
        echo 'ERR: payload missing'; exit;
    }
    $p = json_decode(file_get_contents($payload_path), true);
    if (!$p || !isset($p['post_id']) || !isset($p['content'])) {
        echo 'ERR: payload invalid'; exit;
    }

    // Run as admin so wp_update_post skips kses filtering on block content
    wp_set_current_user(1);

    // wp_update_post expects slashed input; without wp_slash, internal
    // wp_unslash strips one level of backslashes — breaks JSON unicode
    // escapes (e.g. <) inside Gutenberg block attributes.
    // Yoast SEO title / description live in post meta, not post_content, so
    // wp_update_post never touches them. Write them BEFORE wp_update_post:
    // Yoast rebuilds its wp_yoast_indexable cache row on save_post, and that
    // rebuild reads the meta. Writing the meta afterwards leaves the indexable
    // stale and the old <title> keeps rendering.
    $meta_done = [];
    if (!empty($p['meta']) && is_array($p['meta'])) {
        foreach ($p['meta'] as $mk => $mv) {
            update_post_meta((int) $p['post_id'], $mk, wp_slash($mv));
            $meta_done[] = $mk;
        }
    }

    $update = ['ID' => (int) $p['post_id'], 'post_content' => wp_slash($p['content'])];
    if (!empty($p['title']))  $update['post_title']  = wp_slash($p['title']);
    if (!empty($p['status'])) $update['post_status'] = $p['status'];

    $r = wp_update_post($update, true);
    if (is_wp_error($r)) {
        echo 'ERR: ' . $r->get_error_message();
    } else {
        // Yoast 14+ serves <title> and the meta description from its own
        // wp_yoast_indexable cache table, NOT from post meta at render time.
        // That row does not reliably refresh on save_post, so a changed title
        // keeps rendering stale. Drop the row and Yoast lazily rebuilds it
        // from the post meta we just wrote.
        $rebuilt = 0;
        if (!empty($meta_done)) {
            global $wpdb;
            $tbl = $wpdb->prefix . 'yoast_indexable';
            if ($wpdb->get_var("SHOW TABLES LIKE '$tbl'") === $tbl) {
                $rebuilt = (int) $wpdb->delete(
                    $tbl,
                    ['object_id' => (int) $p['post_id'], 'object_type' => 'post'],
                    ['%d', '%s']
                );
            }
        }

        // WP Rocket serves a cached HTML file; without this the old <title>
        // survives the indexable rebuild.
        if (function_exists('rocket_clean_post')) {
            rocket_clean_post((int) $p['post_id']);
        }

        $permalink = get_permalink($r);
        echo 'OK: post=' . $r . ' content_len=' . strlen($p['content'])
           . ' meta=[' . implode(',', $meta_done) . ']'
           . ' indexable_rows_dropped=' . $rebuilt
           . ' url=' . $permalink;
    }

    wp_cache_flush();
    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}, 1);
