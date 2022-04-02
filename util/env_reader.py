def read_env(name=".env") -> dict:
    env = {}
    with open(name, "r") as f:
        for line in f.readlines():
            broken = line.replace("\n", "").split("=")
            env[broken[0]] = broken[1]
    return env