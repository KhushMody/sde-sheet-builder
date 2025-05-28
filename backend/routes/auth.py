from flask import Blueprint, url_for, redirect, jsonify, session

# The 'oauth' object will be imported within the route functions for now,
# attempting to use `from ..app import oauth` as hinted by the subtask.
# This might need adjustment if it leads to circular imports,
# in which case 'oauth' should be accessed via current_app or passed explicitly.

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login/google')
def login_google():
    from ..app import oauth # As per subtask hint
    redirect_uri = url_for('auth.authorize_google', _external=True, _scheme='http') # Added _scheme for local dev
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize/google')
def authorize_google():
    from ..app import oauth # As per subtask hint
    token = oauth.google.authorize_access_token()
    # Fetch user info using the token. parse_id_token is good if you have an id_token
    # and want to validate it. userinfo() hits the userinfo endpoint.
    user_info = oauth.google.userinfo(token=token) 
    session['user'] = user_info # User info is stored in session
    # For testing, redirect to a generic success page or show user_info
    # In a real app, you might redirect to a frontend route like '/profile'
    return redirect('/') # Redirect to homepage or a profile page

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify(message="Logged out successfully")
