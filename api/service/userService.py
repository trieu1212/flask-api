from api.entity.userEntity import UserEntity


def create_user(user_data):
    new_user = UserEntity(
        firstName =user_data["firstName"],
        lastName=user_data["lastName"],
        phone=user_data["phone"],
        password=user_data["password"],
        email=user_data["email"],
    )
    new_user.save()
    return {
        "id": str(new_user._id), 
        "firstName": new_user.firstName,
        "lastName": new_user.lastName,
        "email": new_user.email,
        "phone": new_user.phone
    }


def update_label_user(label, id):
    user = UserEntity.find_by_id(id)
    if user:
        user.label = label
        user.save(update=True)
        user_dict = user.to_dictionary()
        id, firstname, lastName, email, phone, label = user.to_dictionary().get("_id"), user.to_dictionary().get("firstName"), user.to_dictionary().get("lastName") ,user.to_dictionary().get("email"), user.to_dictionary().get("phone"), user.to_dictionary().get("label")
        return user_dict
    return None

def get_user_by_id(id):
    user = UserEntity.find_by_id(id)
    if user:
        return user.to_dictionary()
    return None

def get_user_by_label(label):
    user = UserEntity.find_by_label(label)
    if user:
        return user.to_dictionary()
    return None

def get_user_by_email(email):
    user = UserEntity.find_by_email(email)
    if user:
        return user.to_dictionary()
    return None