def recurPower(base, exp):
    if exp == 1:
        return base
    else:
        return base + recurPower(base, exp - 1)

recurPower(1, 0)