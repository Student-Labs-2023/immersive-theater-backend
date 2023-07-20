
def int_to_str_duration(duration):
    print(duration)
    h = duration // 3600
    m = duration // 60
    s = duration % 60
    return f"{h} h. {m} min. {s} sec."
