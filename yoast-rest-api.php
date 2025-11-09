<?php
/**
 * Plugin Name: Yoast SEO REST API Support
 * Description: Enables Yoast SEO fields (focus keyphrase, meta description, SEO title) to be updated via WordPress REST API. Supports both standard REST API format and n8n HTTP Request node format. Also fixes featured_media permission bug.
 * Version: 2.1
 * Author: Auto-generated for KCM Blog Converter
 *
 * INSTALLATION:
 * 1. Save this file as wordpress-yoast-rest-api.php
 * 2. Upload to wp-content/plugins/ directory
 * 3. Activate in WordPress Admin → Plugins
 *
 * OR add the code below to your theme's functions.php file
 */

/**
 * CRITICAL FIX: Use register_rest_field() instead of register_post_meta()
 *
 * WordPress treats underscore-prefixed meta fields as "private" and blocks
 * REST API updates even when registered with register_post_meta().
 *
 * Using register_rest_field() with update_callback gives us direct control
 * and bypasses WordPress's private meta field restrictions.
 */
add_action('rest_api_init', 'register_yoast_meta_for_rest_api');

function register_yoast_meta_for_rest_api() {
    // Register _yoast_wpseo_focuskw (Focus Keyphrase)
    register_rest_field('post', '_yoast_wpseo_focuskw', array(
        'get_callback' => function($post) {
            return get_post_meta($post['id'], '_yoast_wpseo_focuskw', true);
        },
        'update_callback' => function($value, $post) {
            if (!empty($value)) {
                update_post_meta($post->ID, '_yoast_wpseo_focuskw', sanitize_text_field($value));
                error_log("Yoast REST API: Updated _yoast_wpseo_focuskw = " . $value);
            }
        },
        'schema' => array(
            'type' => 'string',
            'description' => 'Yoast SEO Focus Keyphrase',
        ),
    ));

    // Register _yoast_wpseo_title (SEO Title)
    register_rest_field('post', '_yoast_wpseo_title', array(
        'get_callback' => function($post) {
            return get_post_meta($post['id'], '_yoast_wpseo_title', true);
        },
        'update_callback' => function($value, $post) {
            if (!empty($value)) {
                update_post_meta($post->ID, '_yoast_wpseo_title', sanitize_text_field($value));
                error_log("Yoast REST API: Updated _yoast_wpseo_title = " . $value);
            }
        },
        'schema' => array(
            'type' => 'string',
            'description' => 'Yoast SEO Title',
        ),
    ));

    // Register _yoast_wpseo_metadesc (Meta Description)
    register_rest_field('post', '_yoast_wpseo_metadesc', array(
        'get_callback' => function($post) {
            return get_post_meta($post['id'], '_yoast_wpseo_metadesc', true);
        },
        'update_callback' => function($value, $post) {
            if (!empty($value)) {
                update_post_meta($post->ID, '_yoast_wpseo_metadesc', sanitize_textarea_field($value));
                error_log("Yoast REST API: Updated _yoast_wpseo_metadesc = " . substr($value, 0, 50) . "...");
            }
        },
        'schema' => array(
            'type' => 'string',
            'description' => 'Yoast SEO Meta Description',
        ),
    ));

    // Log when plugin is loaded (for debugging)
    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log('Yoast SEO REST API Support: Meta fields registered via register_rest_field()');
    }
}

/**
 * Optional: Add admin notice to confirm plugin is active
 */
add_action('admin_notices', 'yoast_rest_api_admin_notice');

function yoast_rest_api_admin_notice() {
    // Only show on plugins page
    $screen = get_current_screen();
    if ($screen && $screen->id === 'plugins') {
        // Check if Yoast SEO is active
        if (!is_plugin_active('wordpress-seo/wp-seo.php') && !is_plugin_active('wordpress-seo-premium/wp-seo-premium.php')) {
            echo '<div class="notice notice-warning"><p><strong>Yoast SEO REST API Support:</strong> Yoast SEO plugin is not active. This plugin requires Yoast SEO or Yoast SEO Premium.</p></div>';
        }
    }
}

/**
 * FIX: Featured Media Permission Issue
 *
 * WordPress REST API has a known bug where featured_media returns 0 due to
 * permission issues with attachment posts. This filter ensures all attachments
 * are readable by users with edit_posts capability.
 */
add_filter('user_has_cap', 'fix_featured_media_rest_api_permissions', 10, 4);

function fix_featured_media_rest_api_permissions($allcaps, $caps, $args, $user) {
    // Only apply to read_post capability checks
    if (!isset($args[0]) || $args[0] !== 'read_post') {
        return $allcaps;
    }

    // Get the post ID being checked
    $post_id = isset($args[2]) ? $args[2] : 0;
    if (!$post_id) {
        return $allcaps;
    }

    // If it's an attachment and user can edit posts, grant read access
    if (get_post_type($post_id) === 'attachment' && isset($allcaps['edit_posts']) && $allcaps['edit_posts']) {
        $allcaps['read_post'] = true;
    }

    return $allcaps;
}

/**
 * CRITICAL FIX FOR N8N: Intercept meta parameter and update Yoast fields
 *
 * n8n HTTP Request node sends data as:
 * {
 *   "meta[_yoast_wpseo_metadesc]": "value",
 *   "meta[_yoast_wpseo_focuskw]": "value"
 * }
 *
 * Which WordPress parses into:
 * {
 *   "meta": {
 *     "_yoast_wpseo_metadesc": "value",
 *     "_yoast_wpseo_focuskw": "value"
 *   }
 * }
 *
 * This filter extracts Yoast fields from the meta parameter and updates them.
 */
add_action('rest_insert_post', 'handle_yoast_meta_from_request', 10, 3);

function handle_yoast_meta_from_request($post, $request, $creating) {
    // Get the meta parameter from the request
    $meta = $request->get_param('meta');

    if (!is_array($meta)) {
        return;
    }

    // List of Yoast fields to check for
    $yoast_fields = array(
        '_yoast_wpseo_focuskw',
        '_yoast_wpseo_title',
        '_yoast_wpseo_metadesc'
    );

    // Update each Yoast field if present in the meta parameter
    foreach ($yoast_fields as $field) {
        if (isset($meta[$field]) && !empty($meta[$field])) {
            $value = $meta[$field];

            // Sanitize based on field type
            if ($field === '_yoast_wpseo_metadesc') {
                $value = sanitize_textarea_field($value);
            } else {
                $value = sanitize_text_field($value);
            }

            // Update the post meta
            update_post_meta($post->ID, $field, $value);

            // Log for debugging
            error_log("Yoast REST API (meta interceptor): Updated {$field} for post {$post->ID}");
        }
    }
}

/**
 * TESTING THE PLUGIN
 *
 * After activating this plugin, test with this REST API call:
 *
 * POST https://yoursite.com/wp-json/wp/v2/posts
 * Headers:
 *   Content-Type: application/json
 *   Authorization: Basic <your-base64-encoded-credentials>
 *
 * Body (Standard format):
 * {
 *   "title": "Test Post",
 *   "content": "<p>Test content</p>",
 *   "status": "draft",
 *   "featured_media": 12345,
 *   "meta": {
 *     "_yoast_wpseo_focuskw": "test keyphrase",
 *     "_yoast_wpseo_title": "Test SEO Title",
 *     "_yoast_wpseo_metadesc": "Test meta description"
 *   }
 * }
 *
 * OR n8n HTTP Request format (body parameters):
 * - meta[_yoast_wpseo_focuskw]: "test keyphrase"
 * - meta[_yoast_wpseo_title]: "Test SEO Title"
 * - meta[_yoast_wpseo_metadesc]: "Test meta description"
 *
 * Both formats are now supported!
 */
