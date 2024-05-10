from jwt import *
from django.conf import settings



def convert_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes}"
    file_size_kb = size_bytes / 1024.0
    if file_size_kb >= 1024:
        file_size_mb = file_size_kb / 1024.0
        if file_size_mb >= 1024:
            file_size_gb = file_size_mb / 1024.0
            return f"{file_size_gb:.2f} Gb"
        else:
            return f"{file_size_mb:.2f} Mb"
    else:
        return f"{file_size_kb:.2f} Kb"



def extract_owner_id_from_token(auth_header):
    try:
        token = auth_header.split()[1]
        payload = decode(
            token,
            settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        )
        return payload.get("user_id", None)
    except Exception as e:
        return None

