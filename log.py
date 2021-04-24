def log(msg: str):
    file = open("kaissa64.log", "a+")
    file.write(f"\n{msg}")
    file.close()