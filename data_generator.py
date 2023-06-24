


def generate_log(file_path: str):
    with open(file_path) as f:
        while log:= f.readline():
            yield log
