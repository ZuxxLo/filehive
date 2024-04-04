def user_directory_path(instance, filename):


    return f'user_{instance.id}_{instance.first_name}_{instance.last_name}/{filename}'