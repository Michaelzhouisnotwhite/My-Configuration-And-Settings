from argparse import ArgumentParser
from typing import List


class ArgConfig:
    config_tags = ["cpp", "c", "py"]
    parsers: List[ArgumentParser] = None

    def __init__(self) -> None:
        self.parsers = []
        pass

    def generate_argparse(self):
        self.parsers.append(parser := ArgumentParser())
        main_sub_parsers = parser.add_subparsers()
        self.parsers.append(gen_parser := main_sub_parsers.add_parser(
            "gen", help="generate config file <program language>"))
        gen_sub_parser = gen_parser.add_subparsers(help="tag")
        for tag in self.config_tags:
            self.parsers.append(tag_parser := gen_sub_parser.add_parser(tag, help=f"{tag}"))
            tag_parser.add_argument("-k", "--key", help="only key for tag")
            tag_parser.add_argument("-d", "--default", help="default config file for this tag", action="store_true")
        gen_parser.add_argument("-l", "--list", type=str, required=False, help="list all config file")
        parser.add_argument("-s", "--sub_config", help="sub config under language in generate")

        self.parsers.append(update_parser := main_sub_parsers.add_parser("update", help="update profile"))
        update_parser.add_argument("file_name")

    def parser_help(self):
        [print(x.print_help()) for x in self.parsers]


def main():
    x = ArgConfig()
    x.generate_argparse()
    x.parser_help()
    res1 = x.parsers[0].parse_args(["gen", "cpp", "-k", "test"])
    res2 = x.parsers[0].parse_args(["update", r"D:\Repository\My-Configuration-And-Settings\db\cpp\.clang-format"])
    ...


if __name__ == "__main__":
    main()
