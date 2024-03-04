def get_license_class(license_value):  # translates license from API in readable SR
    license_class = "?"
    if license_value <= 4:
        license_class = "R"
    elif license_value <= 8:
        license_class = "D"
    elif license_value <= 12:
        license_class = "C"
    elif license_value <= 16:
        license_class = "B"
    elif license_value <= 20:
        license_class = "A"
    elif license_value > 20:
        license_class = "PRO"
    return license_class
