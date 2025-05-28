import pytest
from flask import session, jsonify

# Test for @login_required decorator
def test_analyze_route_requires_login(client, mocker):
    # Mock the underlying service to prevent actual calls and focus on auth
    # The create=True argument is important if the module/object doesn't exist yet in some test setups
    # or if we are replacing an object that's not directly patchable at the point of import.
    mocker.patch('backend.routes.api.analyze_question', return_value=jsonify({"message": "Analysis successful"}), create=True)
    
    response = client.post('/api/analyze', json={'question': 'test question'})
    assert response.status_code == 401
    # Default error from @login_required
    assert response.json['error'] == "Authentication required. Please log in." 

# Test for login and accessing a protected route
def test_login_and_access_protected_route(client, mocker):
    # Mock the underlying service
    mocker.patch('backend.routes.api.analyze_question', return_value=jsonify({"message": "Analysis successful"}), create=True)

    # Simulate login by setting the session server-side
    with client.session_transaction() as sess:
        # Ensure the user object structure matches what's set in routes.auth.authorize_google
        # and what's expected by utils.decorators.login_required and app.get_user_identifier
        sess['user'] = {'email': 'test@example.com', 'sub': '12345', 'name': 'Test User'} 
    
    response = client.post('/api/analyze', json={'question': 'test question'})
    
    # Assert that the status code is not 401 or 403, indicating successful access.
    # The actual success code (e.g., 200) depends on the mocked service's response.
    assert response.status_code == 200 
    assert response.json['message'] == "Analysis successful"

# Test for logout
def test_logout(client, mocker):
    # Mock the underlying service for the subsequent check
    mocker.patch('backend.routes.api.analyze_question', return_value=jsonify({"message": "Analysis successful"}), create=True)

    # Simulate login first
    with client.session_transaction() as sess:
        sess['user'] = {'email': 'test_logout@example.com', 'sub': '67890'}
    
    # Make a GET request to /auth/logout
    logout_response = client.get('/auth/logout')
    assert logout_response.status_code == 200
    assert logout_response.json['message'] == "Logged out successfully"
    
    # Check that 'user' is no longer in session by trying to access a protected route
    protected_response = client.post('/api/analyze', json={'question': 'another test question'})
    assert protected_response.status_code == 401
    assert protected_response.json['error'] == "Authentication required. Please log in."

    # Verify session is empty of 'user' key
    with client.session_transaction() as sess:
        assert 'user' not in sess

# Test for rate limiting
def test_rate_limit_analyze_route(client, mocker):
    # Mock the underlying service
    mocker.patch('backend.routes.api.analyze_question', return_value=jsonify({"message": "Analysis successful"}), create=True)

    # Simulate login - rate limiter uses email from session
    user_email_for_rate_limit = 'test_rate_limit@example.com'
    with client.session_transaction() as sess:
        sess['user'] = {'email': user_email_for_rate_limit, 'sub': '123456789'}

    # The rate limit for /api/analyze is "10 per hour;100 per day"
    # We will test the "10 per hour" limit.
    
    # Make 10 requests - these should pass
    for i in range(10):
        response = client.post('/api/analyze', json={'question': f'test question {i+1}'})
        assert response.status_code == 200, f"Request {i+1} failed, expected 200, got {response.status_code}. Response data: {response.data}"
        assert response.json['message'] == "Analysis successful"

    # The 11th request should be rate-limited (429 Too Many Requests)
    response_after_limit = client.post('/api/analyze', json={'question': 'test question 11'})
    assert response_after_limit.status_code == 429
    # You can also check the response body for a specific message if Flask-Limiter provides one, e.g.:
    # assert "Rate limit exceeded" in response_after_limit.get_data(as_text=True)

# To test the actual Google OAuth login routes (/auth/login/google, /auth/authorize/google),
# you would typically mock the `oauth.google` object's methods.
# For example, to test the /auth/login/google route:
# def test_google_login_redirect(client, mocker):
#     mock_authorize_redirect = mocker.patch('backend.app.oauth.google.authorize_redirect')
#     mock_authorize_redirect.return_value = redirect("http://fake.google.auth/url") # Simulate a redirect response
#     response = client.get('/auth/login/google')
#     assert response.status_code == 302 # or whatever status code authorize_redirect returns
#     mock_authorize_redirect.assert_called_once()

# To test the /auth/authorize/google (callback) route:
# def test_google_authorize_callback(client, mocker):
#     mock_authorize_access_token = mocker.patch('backend.app.oauth.google.authorize_access_token')
#     mock_authorize_access_token.return_value = {'access_token': 'fake_token', 'id_token': 'fake_id_token'}
    
#     mock_userinfo = mocker.patch('backend.app.oauth.google.userinfo')
#     mock_userinfo.return_value = {'sub': '123', 'email': 'callback_test@example.com', 'name': 'Callback User'}
    
#     response = client.get('/auth/authorize/google?code=fake_code&state=fake_state') # Simulate Google's callback
    
#     # Check for redirect to '/' as per current auth.py
#     assert response.status_code == 302 
#     assert response.location == "/" # or "http://localhost/" if _external=False in url_for
    
#     with client.session_transaction() as sess:
#         assert 'user' in sess
#         assert sess['user']['email'] == 'callback_test@example.com'
#     mock_authorize_access_token.assert_called_once()
#     mock_userinfo.assert_called_once()

# These OAuth flow tests are commented out as they are more involved and the primary focus here
# was on @login_required, session management for auth, and rate limiting.
# The structure of `backend.app.oauth` (global object) makes patching with `mocker.patch('backend.app.oauth.google.method_name')` feasible.
# The `create=True` on mocker.patch for `analyze_question` is a robust way to ensure the mock works
# even if the import path or target object's existence is tricky in the test environment.
# For `oauth.google` methods, `create=True` might not be needed if `oauth.google` is already fully formed.
# e.g. `mocker.patch.object(oauth.google, 'authorize_redirect', return_value=...)` or
# `mocker.patch('backend.app.oauth.google.authorize_redirect', return_value=...)`
# if `backend.app.oauth` is the correct path to the `oauth` instance.
# Given `oauth` is global in `backend/app.py`, the path `backend.app.oauth` is correct.
# The client fixture from conftest.py is used, which sets up an app with TESTING=True
# and an in-memory SQLite database. SECRET_KEY uses its default from config.py.
# Flask-Limiter's in-memory storage works well for these tests.
# The key_func for limiter uses session['user']['email'], so setting this in session_transaction
# is crucial for testing user-specific rate limits.
