from functools import wraps
from flask import redirect, url_for, current_app
from flask_login import current_user



# ROLE REQUIRED LOGIC

# GAMELL
# def role_required(required_role):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 return redirect(url_for('login.login')) 
#             if current_user.role != required_role or current_user.role != 'admin':
#                 return redirect(url_for('dashboard.dashboard'))  
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


def role_required(*required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login.login')) 
            if current_user.role not in required_roles and current_user.role != 'admin':
                return redirect(url_for('dashboard.dashboard'))  
            return func(*args, **kwargs)
        return wrapper
    return decorator



# TOKEN LOGIC
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

def generate_token(user_id):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_id)

def send_token(user, token):
    # print(f'Token: {token}')
    print(f"Sample URL: http://192.168.39.202:5000/set_password/{token}")


def verify_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, max_age=3600)  # Token expires in 1 hour
        return user_id
    except SignatureExpired:
        # Token has expired
        return None
    except BadSignature:
        # Token is invalid
        return None