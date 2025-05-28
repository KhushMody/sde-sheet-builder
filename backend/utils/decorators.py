from functools import wraps
from flask import session, jsonify, redirect, url_for # Added redirect and url_for for flexibility

def login_required(f):
    """
    Decorator to ensure a user is logged in (i.e., 'user' is in session).
    If not logged in, returns a 401 JSON error response.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            # For an API, returning a JSON error is generally preferred.
            return jsonify(error="Authentication required. Please log in."), 401
            # Alternatively, could redirect to login page for web UIs:
            # return redirect(url_for('auth.login_google', next=request.url)) 
        return f(*args, **kwargs)
    return decorated_function
