<?php
/**
 * Plugin Name: Yoast REST API Fix for KCM Converter
 * Description: Enables Yoast SEO fields (focus keyphrase, meta description, SEO title) to be set via WordPress REST API
 * Version: 1.0
 * Author: KCM Blog Converter Team
 */

// Register Yoast SEO meta fields for REST API access
add_action('rest_api_init', function() {
    // List of Yoast fields that need to be accessible via REST API
    $yoast_fields = array(
        '_yoast_wpseo_focuskw',      // Focus keyphrase
        '_yoast_wpseo_title',         // SEO title
        '_yoast_wpseo_metadesc'       // Meta description
    );

    // Register each field
    foreach ($yoast_fields as $field) {
        register_post_meta('post', $field, array(
            'show_in_rest' => true,
            'single' => true,
            'type' => 'string',
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            }
        ));
    }
});
