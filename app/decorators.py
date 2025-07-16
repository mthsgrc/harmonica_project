from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
                
            if current_user.role not in roles:
                flash('You do not have permission to access this page', 'danger')
                #abort(403) => Search this
                return redirect(url_for('main.index'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Update existing decorators
def admin_required(f):
    return roles_required('admin')(f)

def editor_required(f):
    return roles_required('admin', 'editor')(f)
