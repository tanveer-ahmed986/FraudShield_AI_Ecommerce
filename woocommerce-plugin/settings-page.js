jQuery(document).ready(function($) {
    $('#tfshield-test-api').on('click', function() {
        var endpoint = $('#tfshield_api_endpoint').val();
        var resultDiv = $('#tfshield-api-result');
        resultDiv.html('<p>Testing connection...</p>');

        $.ajax({
            url: endpoint + '/api/v1/health',
            method: 'GET',
            timeout: 10000,
            success: function(response) {
                var html = '<div class="notice notice-success"><p>';
                html += '✅ <strong>Connection successful!</strong><br>';
                html += 'Status: ' + response.status + '<br>';
                html += 'Model loaded: ' + (response.model_loaded ? 'Yes' : 'No');
                html += '</p></div>';
                resultDiv.html(html);
            },
            error: function(xhr, status, error) {
                var html = '<div class="notice notice-error"><p>';
                html += '❌ <strong>Connection failed!</strong><br>';
                html += 'Error: ' + error;
                html += '</p></div>';
                resultDiv.html(html);
            }
        });
    });
});
