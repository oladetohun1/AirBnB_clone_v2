#!/usr/bin/python3
import os
from datetime import datetime


def do_pack():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{current_time}.tgz"
    archive_path = os.path.join("versions", archive_name)
    web_static_path = "web_static"

    # Create the versions folder if it doesn't exist
    os.makedirs("versions", exist_ok=True)

    # Create the .tgz archive
    tar_command = f"tar -cvzf {archive_path} {web_static_path}"
    result = os.system(tar_command)

    if result == 0:
        return archive_path
    else:
        return None
