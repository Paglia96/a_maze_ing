from argparse import ArgumentParser


def values_check(configs: dict):
    width, height = (configs["WIDTH"], configs["HEIGHT"])
    configs["WIDTH"] = int(height)
    configs["HEIGHT"] = int(width)
    configs["ENTRY"] = (int((v := configs["ENTRY"].split(","))[0]), int(v[1]))
    configs["EXIT"] = (int((v := configs["EXIT"].split(","))[0]), int(v[1]))
    if (val := configs["PERFECT"].lower()) in ("true", "false"):
        configs["PERFECT"] = eval(val.capitalize())
    else:
        raise ValueError("PERFECT must be true or false")
    if configs["ENTRY"] == configs["EXIT"]:
        raise ValueError("Entry and exit cannot be the same cell")
    configs["SEED"] = int(configs["SEED"]) if "SEED" in configs else 1
    if "GEN_ALGORITHM" in configs:
        val = configs["GEN_ALGORITHM"].lower()
        configs["GEN_ALGORITHM"] = val if val in ["prim", "dfs"] else "prim"
    else:
        configs["GEN_ALGORITHM"] = "prim"
    if "SOLVING_ALGORITHM" in configs:
        val = configs["SOLVING_ALGORITHM"].lower()
        configs["SOLVING_ALGORITHM"] = val if val in ["other", "bfs"] else "bfs"
    else:
        configs["SOLVING_ALGORITHM"] = "bfs"


def file_parsing(configs, filename):
    with open(filename, "r") as f:
        config_keys: list[str] = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]
        optional_keys: list[str] = ["SEED", "GEN_ALGORITHM", "SOLVING_ALGORITHM"]
        for line in f:
            if line.startswith("#") or line == "\n":
                continue
            elif "#" in line:
                line: list[str] = line.split("#")[0]
            config = line.split("=")
            if len(config) != 2:
                raise ValueError(
                    "The configuration file must contain one ‘KEY=VALUE‘ pair per line."
                )
            config[0] = config[0].strip()
            config[1] = config[1][:-1].strip()  # remove ending \n e spaces

            def upload_key(config: list[str], configs: dict, keys_list: list[str]):
                if (key := config[0].upper()) in keys_list:
                    keys_list.remove(key)
                    if key in configs:
                        raise ValueError("Just one KEY for allowed type.")
                    configs[key] = config[1]

            upload_key(config, configs, config_keys)
            upload_key(config, configs, optional_keys)
        if len(config_keys):
            raise ValueError(f"Mandatory keys: {config_keys}")


def config_parser():
    """Parse and validate the maze configuration file.

    The configuration file path is read from the command-line arguments.
    Each non-empty line must contain a single KEY=VALUE pair.
    Lines beginning with # and inline comments are ignored.

    Returns:
        dict: A dictionary containing the parsed configuration values or default ones.
            WIDTH and HEIGHT are integers.
            ENTRY and EXIT are coordinate tuples.
            OUTPUT_FILE is a string.
            PERFECT is a boolean.
            GEN_ALGORITHM and SOLVING_ALGORITHM are strings.
            SEED is an integer.

    Raises:
        SystemExit: if the number of given arguments is different from 1.
        ValueError: If a configuration line is malformed or a mandatory
            configuration key is missing.
        FileNotFoundError: If the specified configuration file does not exist.
        PermissionError: If the configuration file cannot be opened.
    """
    parser = ArgumentParser(
        description="Receives the maze configuration settings as an argument"
    )
    parser.add_argument("filename", help="file path")
    filename = parser.parse_args().filename
    configs: dict = {}
    file_parsing(configs, filename)
    values_check(configs)
    return configs
