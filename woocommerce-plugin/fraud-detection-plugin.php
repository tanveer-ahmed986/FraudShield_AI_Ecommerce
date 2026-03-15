<?php
/**
 * Plugin Name: AI Fraud Detection for WooCommerce
 * Plugin URI: https://github.com/tanveer-ahmed986/fraud_detection_system_ecommerce
 * Description: Real-time AI-powered fraud detection for WooCommerce transactions with 85%+ precision
 * Version: 1.0.0
 * Author: Tanveer Ahmed
 * Author URI: https://github.com/tanveer-ahmed986
 * License: MIT
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 6.0
 * WC tested up to: 8.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// Check if WooCommerce is active
if (!in_array('woocommerce/woocommerce.php', apply_filters('active_plugins', get_option('active_plugins')))) {
    return;
}

/**
 * Main Plugin Class
 */
class WC_AI_Fraud_Detection {

    /**
     * Plugin version
     */
    const VERSION = '1.0.0';

    /**
     * Instance of this class
     */
    private static $instance = null;

    /**
     * API endpoint
     */
    private $api_endpoint;

    /**
     * API key
     */
    private $api_key;

    /**
     * Constructor
     */
    private function __construct() {
        $this->init_hooks();
    }

    /**
     * Get singleton instance
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Initialize hooks
     */
    private function init_hooks() {
        // Add settings menu
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));

        // Hook into checkout process
        add_action('woocommerce_checkout_order_processed', array($this, 'check_fraud_on_checkout'), 10, 3);

        // Add admin notices
        add_action('admin_notices', array($this, 'display_admin_notices'));

        // Add order meta box
        add_action('add_meta_boxes', array($this, 'add_fraud_detection_meta_box'));

        // Add order column
        add_filter('manage_edit-shop_order_columns', array($this, 'add_fraud_column'));
        add_action('manage_shop_order_posts_custom_column', array($this, 'populate_fraud_column'), 10, 2);
    }

    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_submenu_page(
            'woocommerce',
            'AI Fraud Detection',
            'Fraud Detection',
            'manage_woocommerce',
            'wc-fraud-detection',
            array($this, 'render_settings_page')
        );
    }

    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('wc_fraud_detection_settings', 'wc_fraud_api_endpoint');
        register_setting('wc_fraud_detection_settings', 'wc_fraud_api_key');
        register_setting('wc_fraud_detection_settings', 'wc_fraud_auto_hold');
        register_setting('wc_fraud_detection_settings', 'wc_fraud_threshold');
        register_setting('wc_fraud_detection_settings', 'wc_fraud_notify_admin');
    }

    /**
     * Render settings page
     */
    public function render_settings_page() {
        ?>
        <div class="wrap">
            <h1>🛡️ AI Fraud Detection Settings</h1>
            <p>Configure your AI-powered fraud detection system for WooCommerce.</p>

            <form method="post" action="options.php">
                <?php settings_fields('wc_fraud_detection_settings'); ?>
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="wc_fraud_api_endpoint">API Endpoint</label>
                        </th>
                        <td>
                            <input type="url"
                                   id="wc_fraud_api_endpoint"
                                   name="wc_fraud_api_endpoint"
                                   value="<?php echo esc_attr(get_option('wc_fraud_api_endpoint', 'http://localhost:8000')); ?>"
                                   class="regular-text"
                                   placeholder="http://localhost:8000"
                                   required>
                            <p class="description">Your fraud detection API endpoint (e.g., http://localhost:8000 or https://your-api.com)</p>
                        </td>
                    </tr>

                    <tr>
                        <th scope="row">
                            <label for="wc_fraud_api_key">API Key</label>
                        </th>
                        <td>
                            <input type="password"
                                   id="wc_fraud_api_key"
                                   name="wc_fraud_api_key"
                                   value="<?php echo esc_attr(get_option('wc_fraud_api_key', '')); ?>"
                                   class="regular-text"
                                   placeholder="Optional - leave blank if not required">
                            <p class="description">API authentication key (if required by your API)</p>
                        </td>
                    </tr>

                    <tr>
                        <th scope="row">
                            <label for="wc_fraud_threshold">Fraud Threshold</label>
                        </th>
                        <td>
                            <input type="number"
                                   id="wc_fraud_threshold"
                                   name="wc_fraud_threshold"
                                   value="<?php echo esc_attr(get_option('wc_fraud_threshold', '0.7')); ?>"
                                   min="0"
                                   max="1"
                                   step="0.05"
                                   class="small-text">
                            <p class="description">Confidence threshold for fraud detection (0.0 - 1.0). Default: 0.7 (70%)</p>
                        </td>
                    </tr>

                    <tr>
                        <th scope="row">
                            <label for="wc_fraud_auto_hold">Auto-Hold Suspicious Orders</label>
                        </th>
                        <td>
                            <input type="checkbox"
                                   id="wc_fraud_auto_hold"
                                   name="wc_fraud_auto_hold"
                                   value="1"
                                   <?php checked(get_option('wc_fraud_auto_hold'), '1'); ?>>
                            <label for="wc_fraud_auto_hold">Automatically set suspicious orders to "On Hold" status</label>
                        </td>
                    </tr>

                    <tr>
                        <th scope="row">
                            <label for="wc_fraud_notify_admin">Email Notifications</label>
                        </th>
                        <td>
                            <input type="checkbox"
                                   id="wc_fraud_notify_admin"
                                   name="wc_fraud_notify_admin"
                                   value="1"
                                   <?php checked(get_option('wc_fraud_notify_admin'), '1'); ?>>
                            <label for="wc_fraud_notify_admin">Send email notification when fraud is detected</label>
                        </td>
                    </tr>
                </table>

                <?php submit_button('Save Settings'); ?>
            </form>

            <hr>

            <h2>🔍 Test API Connection</h2>
            <p>Click the button below to test your API connection:</p>
            <button type="button" class="button button-secondary" id="test-api-connection">Test Connection</button>
            <div id="api-test-result" style="margin-top: 10px;"></div>

            <script type="text/javascript">
            jQuery(document).ready(function($) {
                $('#test-api-connection').on('click', function() {
                    var endpoint = $('#wc_fraud_api_endpoint').val();
                    var apiKey = $('#wc_fraud_api_key').val();
                    var resultDiv = $('#api-test-result');

                    resultDiv.html('<p>Testing connection...</p>');

                    $.ajax({
                        url: endpoint + '/health',
                        method: 'GET',
                        headers: apiKey ? {'X-API-Key': apiKey} : {},
                        timeout: 10000,
                        success: function(response) {
                            resultDiv.html('<div class="notice notice-success"><p>✅ <strong>Connection successful!</strong><br>Status: ' + response.status + '<br>Model loaded: ' + (response.model_loaded ? 'Yes' : 'No') + '</p></div>');
                        },
                        error: function(xhr, status, error) {
                            resultDiv.html('<div class="notice notice-error"><p>❌ <strong>Connection failed!</strong><br>Error: ' + error + '<br>Please check your API endpoint and ensure the service is running.</p></div>');
                        }
                    });
                });
            });
            </script>
        </div>
        <?php
    }

    /**
     * Check for fraud on checkout
     */
    public function check_fraud_on_checkout($order_id, $posted_data, $order) {
        // Get settings
        $api_endpoint = get_option('wc_fraud_api_endpoint');
        $api_key = get_option('wc_fraud_api_key');
        $threshold = floatval(get_option('wc_fraud_threshold', 0.7));
        $auto_hold = get_option('wc_fraud_auto_hold') === '1';
        $notify_admin = get_option('wc_fraud_notify_admin') === '1';

        if (empty($api_endpoint)) {
            return; // API not configured
        }

        // Prepare transaction data
        $transaction_data = $this->prepare_transaction_data($order);

        // Call fraud detection API
        $fraud_result = $this->call_fraud_api($api_endpoint, $api_key, $transaction_data);

        if ($fraud_result) {
            // Store fraud detection result
            update_post_meta($order_id, '_fraud_detection_result', $fraud_result);
            update_post_meta($order_id, '_fraud_detection_checked', current_time('mysql'));

            $is_fraud = ($fraud_result['label'] === 'fraud' && $fraud_result['confidence'] >= $threshold);
            update_post_meta($order_id, '_is_fraud_detected', $is_fraud ? 'yes' : 'no');

            // Handle fraud detection
            if ($is_fraud) {
                // Add order note
                $order->add_order_note(
                    sprintf(
                        '🚨 <strong>Fraud Alert!</strong><br>Confidence: %.1f%%<br>Top Features: %s',
                        $fraud_result['confidence'] * 100,
                        $this->format_features($fraud_result['top_features'])
                    ),
                    false,
                    true
                );

                // Auto-hold order if enabled
                if ($auto_hold && $order->get_status() !== 'on-hold') {
                    $order->update_status('on-hold', 'Automatically placed on hold due to fraud detection.');
                }

                // Send admin notification
                if ($notify_admin) {
                    $this->send_fraud_notification($order, $fraud_result);
                }
            } else {
                // Add confirmation note
                $order->add_order_note(
                    sprintf(
                        '✅ <strong>Fraud Check Passed</strong><br>Confidence: %.1f%% (Legitimate)',
                        (1 - $fraud_result['confidence']) * 100
                    ),
                    false,
                    false
                );
            }
        } else {
            // API call failed - add note
            $order->add_order_note('⚠️ Fraud detection API unavailable. Order requires manual review.', false, true);
            update_post_meta($order_id, '_fraud_detection_error', 'API unavailable');
        }
    }

    /**
     * Prepare transaction data for API
     */
    private function prepare_transaction_data($order) {
        $customer = $order->get_user();
        $billing = $order->get_address('billing');
        $shipping = $order->get_address('shipping');

        // Calculate hour and day
        $order_date = $order->get_date_created();
        $hour_of_day = intval($order_date->format('G'));
        $day_of_week = intval($order_date->format('N')) - 1; // 0 = Monday

        // Check if billing = shipping
        $billing_shipping_match = (
            $billing['address_1'] === $shipping['address_1'] &&
            $billing['city'] === $shipping['city'] &&
            $billing['postcode'] === $shipping['postcode']
        );

        // Determine if new user
        $is_new_user = !$customer || $this->get_user_order_count($customer ? $customer->ID : 0) === 1;

        return array(
            'merchant_id' => get_bloginfo('name'),
            'amount' => floatval($order->get_total()),
            'payment_method' => $order->get_payment_method(),
            'user_id_hash' => $customer ? hash('sha256', strval($customer->ID)) : 'guest_' . substr(hash('sha256', $billing['email']), 0, 16),
            'ip_hash' => hash('sha256', $order->get_customer_ip_address()),
            'email_domain' => substr(strrchr($billing['email'], '@'), 1),
            'is_new_user' => $is_new_user,
            'device_type' => $this->detect_device_type(),
            'billing_shipping_match' => $billing_shipping_match,
            'hour_of_day' => $hour_of_day,
            'day_of_week' => $day_of_week,
            'items_count' => $order->get_item_count()
        );
    }

    /**
     * Call fraud detection API
     */
    private function call_fraud_api($endpoint, $api_key, $data) {
        $url = rtrim($endpoint, '/') . '/api/v1/predict';

        $headers = array(
            'Content-Type' => 'application/json'
        );

        if (!empty($api_key)) {
            $headers['X-API-Key'] = $api_key;
        }

        $response = wp_remote_post($url, array(
            'headers' => $headers,
            'body' => json_encode($data),
            'timeout' => 10,
            'sslverify' => true
        ));

        if (is_wp_error($response)) {
            error_log('Fraud API Error: ' . $response->get_error_message());
            return null;
        }

        $body = wp_remote_retrieve_body($response);
        $result = json_decode($body, true);

        return $result;
    }

    /**
     * Get user order count
     */
    private function get_user_order_count($user_id) {
        if ($user_id === 0) {
            return 0;
        }

        $customer = new WC_Customer($user_id);
        return $customer->get_order_count();
    }

    /**
     * Detect device type from user agent
     */
    private function detect_device_type() {
        if (!isset($_SERVER['HTTP_USER_AGENT'])) {
            return 'unknown';
        }

        $user_agent = $_SERVER['HTTP_USER_AGENT'];

        if (preg_match('/mobile|android|iphone|ipad|phone/i', $user_agent)) {
            return 'mobile';
        } elseif (preg_match('/tablet|ipad/i', $user_agent)) {
            return 'tablet';
        } else {
            return 'desktop';
        }
    }

    /**
     * Format features for display
     */
    private function format_features($features) {
        if (empty($features)) {
            return 'N/A';
        }

        $formatted = array();
        foreach ($features as $feature) {
            $formatted[] = $feature['feature'] . ' (' . number_format($feature['contribution'], 3) . ')';
        }

        return implode(', ', $formatted);
    }

    /**
     * Send fraud notification email
     */
    private function send_fraud_notification($order, $fraud_result) {
        $admin_email = get_option('admin_email');
        $subject = sprintf('[Fraud Alert] Order #%s - %.1f%% confidence', $order->get_order_number(), $fraud_result['confidence'] * 100);

        $message = sprintf(
            "🚨 Fraud Detection Alert\n\n" .
            "Order ID: #%s\n" .
            "Customer: %s %s\n" .
            "Email: %s\n" .
            "Amount: %s\n" .
            "Fraud Confidence: %.1f%%\n\n" .
            "Top Contributing Factors:\n%s\n\n" .
            "View Order: %s",
            $order->get_order_number(),
            $order->get_billing_first_name(),
            $order->get_billing_last_name(),
            $order->get_billing_email(),
            $order->get_formatted_order_total(),
            $fraud_result['confidence'] * 100,
            $this->format_features($fraud_result['top_features']),
            $order->get_edit_order_url()
        );

        wp_mail($admin_email, $subject, $message);
    }

    /**
     * Add fraud detection meta box
     */
    public function add_fraud_detection_meta_box() {
        add_meta_box(
            'wc_fraud_detection_meta_box',
            '🛡️ AI Fraud Detection',
            array($this, 'render_fraud_detection_meta_box'),
            'shop_order',
            'side',
            'high'
        );
    }

    /**
     * Render fraud detection meta box
     */
    public function render_fraud_detection_meta_box($post) {
        $order_id = $post->ID;
        $fraud_result = get_post_meta($order_id, '_fraud_detection_result', true);
        $is_fraud = get_post_meta($order_id, '_is_fraud_detected', true);
        $checked_time = get_post_meta($order_id, '_fraud_detection_checked', true);
        $error = get_post_meta($order_id, '_fraud_detection_error', true);

        if ($error) {
            echo '<div style="padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107;">';
            echo '<strong>⚠️ API Error</strong><br>';
            echo esc_html($error);
            echo '</div>';
        } elseif ($fraud_result) {
            $confidence = floatval($fraud_result['confidence']) * 100;

            if ($is_fraud === 'yes') {
                echo '<div style="padding: 10px; background: #f8d7da; border-left: 4px solid #dc3545;">';
                echo '<strong>🚨 FRAUD DETECTED</strong><br>';
                echo sprintf('Confidence: <strong>%.1f%%</strong><br>', $confidence);
            } else {
                echo '<div style="padding: 10px; background: #d4edda; border-left: 4px solid #28a745;">';
                echo '<strong>✅ Legitimate</strong><br>';
                echo sprintf('Fraud Risk: <strong>%.1f%%</strong><br>', $confidence);
            }

            echo '<br><strong>Top Factors:</strong><br>';
            if (!empty($fraud_result['top_features'])) {
                echo '<ul style="margin: 5px 0; padding-left: 20px;">';
                foreach ($fraud_result['top_features'] as $feature) {
                    echo '<li>' . esc_html($feature['feature']) . ': ' . esc_html(number_format($feature['contribution'], 3)) . '</li>';
                }
                echo '</ul>';
            }

            echo '<br><small>Checked: ' . esc_html($checked_time) . '</small>';
            echo '</div>';
        } else {
            echo '<div style="padding: 10px; background: #e7f3ff; border-left: 4px solid #2196f3;">';
            echo '<strong>ℹ️ Not Checked</strong><br>';
            echo 'Fraud detection not performed for this order.';
            echo '</div>';
        }
    }

    /**
     * Add fraud detection column to orders list
     */
    public function add_fraud_column($columns) {
        $new_columns = array();

        foreach ($columns as $key => $value) {
            $new_columns[$key] = $value;

            // Add fraud column after order status
            if ($key === 'order_status') {
                $new_columns['fraud_detection'] = '🛡️ Fraud';
            }
        }

        return $new_columns;
    }

    /**
     * Populate fraud detection column
     */
    public function populate_fraud_column($column, $post_id) {
        if ($column === 'fraud_detection') {
            $is_fraud = get_post_meta($post_id, '_is_fraud_detected', true);
            $fraud_result = get_post_meta($post_id, '_fraud_detection_result', true);
            $error = get_post_meta($post_id, '_fraud_detection_error', true);

            if ($error) {
                echo '<span style="color: #ffc107;">⚠️</span>';
            } elseif ($is_fraud === 'yes') {
                $confidence = floatval($fraud_result['confidence']) * 100;
                echo sprintf('<span style="color: #dc3545; font-weight: bold;" title="Fraud detected: %.1f%% confidence">🚨</span>', $confidence);
            } elseif ($is_fraud === 'no') {
                echo '<span style="color: #28a745;" title="Legitimate">✅</span>';
            } else {
                echo '<span style="color: #6c757d;">—</span>';
            }
        }
    }

    /**
     * Display admin notices
     */
    public function display_admin_notices() {
        $api_endpoint = get_option('wc_fraud_api_endpoint');

        if (empty($api_endpoint)) {
            $settings_url = admin_url('admin.php?page=wc-fraud-detection');
            echo '<div class="notice notice-warning is-dismissible">';
            echo '<p><strong>AI Fraud Detection:</strong> Please <a href="' . esc_url($settings_url) . '">configure your API endpoint</a> to enable fraud detection.</p>';
            echo '</div>';
        }
    }
}

// Initialize plugin
add_action('plugins_loaded', function() {
    WC_AI_Fraud_Detection::get_instance();
});
