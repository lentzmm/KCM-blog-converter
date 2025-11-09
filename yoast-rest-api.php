<?php
/**
 * Plugin Name: Yoast SEO REST API Support
 * Description: Enables Yoast SEO fields (focus keyphrase, meta description, SEO title) to be updated via WordPress REST API
 * Version: 1.0
 * Author: Auto-generated for KCM Blog Converter
 *
 * INSTALLATION:
 * 1. Save this file as wordpress-yoast-rest-api.php
 * 2. Upload to wp-content/plugins/ directory
 * 3. Activate in WordPress Admin → Plugins
 *
 * OR add the code below to your theme's functions.php file
 */

add_action('rest_api_init', 'register_yoast_meta_for_rest_api');

function register_yoast_meta_for_rest_api() {
    // Define the Yoast SEO meta fields we want to expose
    $yoast_meta_fields = array(
        '_yoast_wpseo_focuskw'      => 'Focus Keyphrase',
        '_yoast_wpseo_title'         => 'SEO Title',
        '_yoast_wpseo_metadesc'      => 'Meta Description',
    );

    // Register each field for REST API access
    foreach ($yoast_meta_fields as $meta_key => $description) {
        register_post_meta('post', $meta_key, array(
            'show_in_rest' => true,
            'single' => true,
            'type' => 'string',
            'description' => $description,
            'auth_callback' => function() {
                // Only allow users who can edit posts to update these fields
                return current_user_can('edit_posts');
            },
            'sanitize_callback' => 'sanitize_text_field'
        ));
    }

    // Log when plugin is loaded (for debugging)
    if (defined('WP_DEBUG') && WP_DEBUG) {
        error_log('Yoast SEO REST API Support: Meta fields registered for REST API');
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
 * TESTING THE PLUGIN
 *
 * After activating this plugin, test with this REST API call:
 *
 * POST https://yoursite.com/wp-json/wp/v2/posts
 * Headers:
 *   Content-Type: application/json
 *   Authorization: Basic <your-base64-encoded-credentials>
 *
 * Body:
 * {
 *   "title": "Test Post",
 *   "content": "<p>Test content</p>",
 *   "status": "draft",
 *   "meta": {
 *     "_yoast_wpseo_focuskw": "test keyphrase",
 *     "_yoast_wpseo_title": "Test SEO Title",
 *     "_yoast_wpseo_metadesc": "Test meta description"
 *   }
 * }
 *
 * Then check the response - it should include the meta fields:
 * {
 *   "id": 123,
 *   "title": "Test Post",
 *   "meta": {
 *     "_yoast_wpseo_focuskw": "test keyphrase",
 *     "_yoast_wpseo_title": "Test SEO Title",
 *     "_yoast_wpseo_metadesc": "Test meta description"
 *   }
 * }
 */
