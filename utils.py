from functools import wraps
from flask import redirect, url_for, current_app
from flask_login import current_user
import time


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


ROLES = [
    'admin',
    'governor',
    'cabin_owner',
    'plowman',
]

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
    print(f"Sample URL: http://127.0.0.1:5000/set_password/{token}")
    

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
    
# ENKEL FUNKSJON SOM VISER HVOR LANG TID EN FUNKSJON BRUKER PÅ Å KJØRE
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper