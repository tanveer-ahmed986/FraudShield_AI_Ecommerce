jQuery(document).ready(function($) {
    $('#fraud-check-btn').on('click', function() {
        var button = $(this);
        var orderId = button.data('order-id');
        var statusDiv = $('#fraud-check-status');

        // Disable button and show loading
        button.prop('disabled', true).text('⏳ Checking...');
        statusDiv.html('<span style="color: #0073aa;">Running fraud detection...</span>');

        $.ajax({
            url: wcFraudDetection.ajaxurl,
            type: 'POST',
            data: {
                action: 'check_fraud_ajax',
                order_id: orderId,
                nonce: wcFraudDetection.nonce
            },
            success: function(response) {
                if (response.success) {
                    statusDiv.html('<span style="color: #46b450;">✅ Check completed! Reloading page...</span>');
                    // Reload page to show results
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    statusDiv.html('<span style="color: #dc3232;">❌ Error: ' + (response.data.message || 'Unknown error') + '</span>');
                    button.prop('disabled', false).text('🔍 Check for Fraud');
                }
            },
            error: function(xhr, status, error) {
                statusDiv.html('<span style="color: #dc3232;">❌ Ajax error: ' + error + '</span>');
                button.prop('disabled', false).text('🔍 Check for Fraud');
            }
        });
    });
});
