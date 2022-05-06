def parse_secrets() -> dict:
    """
    Returns a dictionary of variables parsed from the .secrets file in the directory this was called.
    """
    secrets = {}
    with open(".secrets", "r") as file:
        for line in file:
            if "=" in line:
                var = line.strip().split("=")
                if var[1].isdigit():
                    secrets[var[0]] = int(var[1])
                else:
                    secrets[var[0]] = var[1].strip('"')
    return secrets