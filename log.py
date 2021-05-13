def log(msg: str, file: str = "kaissa64.log"):
    file = open(file, "a+")
    file.write(f"\n{msg}")
    file.close()