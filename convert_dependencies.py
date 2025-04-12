import tomllib


def convert_dependencies(file):
    with open(file, "rb") as f:
        d = tomllib.load(f)

    deps = d["tool"]["poetry"]["dependencies"]

    conv = "dependencies = [\n]"
    for dep, ver in deps.items():
        c = '"' + dep + " "
        if ver[0] == "^":
            c += ">= " + ver[1:] + '",\n'
            conv = conv[:-1] + c + conv[-1:]
    print(conv)


if __name__ == "__main__":
    import sys

    convert_dependencies(sys.argv[1])
