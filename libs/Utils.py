from flask import request


def get_actual_child_path():
    child_path_list = request.path.split("/")
    return child_path_list[-1] if not child_path_list[-1].isdigit() else child_path_list[-2]
