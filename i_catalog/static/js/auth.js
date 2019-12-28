$(function () {
	if ($('#state')) {
		var state = $('#state').val() || '';
        // files are cached locally between pages.
        $.ajaxSetup({ cache: true });
		// Google sign in/up
		$.post(
			oAuth,
			{ order: "G_id", state: state },
			'json'
		)
			.done(function(c_id) {
				if (!(/.*\.apps\.googleusercontent\.com$/.test(
                    reverseString(c_id)))) {
					$('#Gsign').remove()
				}
				if ($('#Gsign').length > 0) {
                    $.getScript(
                        'https://apis.google.com/js/api:client.js', 
                        function () {
                            gapi.load('auth2', function() {
                                auth2 = gapi.auth2.init({
                                    client_id: reverseString(c_id),
                                });
                            });
                        }
                    );
					$('#Gsign').on('click', () => {
						// GCallback on click
						auth2.grantOfflineAccess().then(gCallback);
					});
					function gCallback(authResult) {
						if (authResult.code) {
							// Send the code to the server
							$.ajax({
                                type: 'POST',
                                url: goAuth + '?state=' + state,
                                // Always include an `X-Requested-With`
                                // header in every AJAX request,
                                // to protect against CSRF attacks.
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                },
                                contentType: 'application/octet-stream; charset=utf-8',
                                data: authResult['code'],
                                success: function(result) {
                                    // Handle or verify the server response.
                                    if (typeof result.go == 'string') {
                                        location.replace(result.go);
                                    }
                                },
                                processData: false
							});
						} else {
							// There was an error.
                            alert('User cancelled login or did not fully authorize.');
						}
					}

				}
			})
			.fail(function() {
				// delete sign in button if no client_id provided
				$('#Gsign').remove();
			});

        // Facebook sign in/up
		$.post(
			oAuth,
			{ order: "FB_id", state: state },
			'json'
		)
			.done(function(a_id) {
				if ($('#FBsign').length > 0 && a_id.length > 0) {
                    // let jQuery’s import the SDK from the correct
                    // ` URL for user’s locale.
                    $.getScript(
                        'https://connect.facebook.net/en_US/sdk.js', 
                        function(){
                            // init facebook SDK functionality
                            FB.init({
                                appId: reverseString(a_id),
                                version: 'v2.7'
                            });     
                            FB.getLoginStatus(FBCallback);
                        }
                    );

                    function FBCallback(fbResponse) {
                        if (fbResponse.status == 'connected') {
                            $('#FBsign').on('click', () => {
                                // facebook login on click
                                fbCallback(fbResponse);
                            });
                            // get confermation to log with facebook
                            if (confirm('Your facebook account is connected\ntry to log in with it ?')) {
                                // facebook login if connected
                                fbCallback(fbResponse);
                            }
                        } else {
                            $('#FBsign').on('click', () => {
                                // facebook login on click
                                FB.login(function(response) {
                                    fbCallback(response);
                                }, {scope: 'public_profile,email'});
                            });
                        }
                    }

                    function fbCallback(fbResponse) {
                        if (fbResponse.authResponse) {
                            FB.api('/me', function(response) {
                            $.ajax({
                                type: 'POST',
                                url: fboAuth + '?state=' + state
                                    + '&id=' + response.id,
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                },
                                contentType: 'application/json',
                                data: fbResponse.authResponse.accessToken,
                                success: function(result) {
                                    // Handle or verify the server response.
                                    if (typeof result.go == 'string') {
                                        location.replace(result.go);
                                    }
                                },
                                processData: false
                            });});

                        } else {
                            alert('User cancelled login or did not fully authorize.');
                        }
                    }

				}
			})
			.fail(function() {
				// delete sign in button if no client_id provided
				$('#FBsign').remove();
			});
    }

    if (($('#soc-log').length > 0 && $('#soc-log').children().length <= 1)
        || state == '') {
		$('#soc-log').remove();
    }

});
