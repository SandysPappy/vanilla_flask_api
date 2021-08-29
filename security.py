from models.user_model import UserModel

# example of getting this user
# this_user = userid_mapping[1]
def authenticate(username, password):
    # None is default value if user not found
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

# unique to Flask-JWT
# payload is the content of the jwt token
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
