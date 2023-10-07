import argparse
import os
import shutil
import utils
from utils import print_when_debug, write_json_file, read_json_file, check_cache_folder
from settings import *
from enum import Enum, auto
import api
from pydantic import BaseModel


class FileInfoModel(BaseModel):
    filename: str
    cached_time: str
    modified_time: str


class Program:
    file_name: str
    file_info_dict: dict
    comment: str
    cur_repo = Repo(WORK_FOLDER)
    git_cli = cur_repo.git

    class FileDetail(pydantic.BaseModel):
        comment: str = ""
        time: str = ""

    class Command(Enum):
        add = auto()
        cat = auto()
        list = auto()

    def __init__(self) -> None:
        self.git_cli.fetch()
        self.git_cli.pull()
        if not os.path.exists(STORAGE_FOLDER):
            os.makedirs(STORAGE_FOLDER)

        if not os.path.exists(STORAGE_INFORMATION_PATH):
            with open(STORAGE_INFORMATION_PATH, "w") as f:
                f.write("{}")

        check_cache_folder()
        # self.update_information()
        # self.upload_files()

    def update_information(self):
        self.load_file_info()
        for file_name in os.listdir(STORAGE_FOLDER):
            if file_name not in self.file_info_dict.keys():
                if file_name == os.path.split(STORAGE_INFORMATION_PATH)[-1]:
                    continue
                self.file_info_dict[file_name] = Program.FileDetail(time="Asdf").model_dump()

        files_not_exists = []
        for file_name in self.file_info_dict.keys():
            if not os.path.exists(os.path.join(STORAGE_FOLDER, file_name)):
                files_not_exists.append(file_name)

        for file_name in files_not_exists:
            self.file_info_dict.pop(file_name)
        utils.print_when_debug(json.dumps(self.file_info_dict, indent=2))

        self.save_file_info()

    def save_file_info(self):
        utils.write_json_file(self.file_info_dict, STORAGE_INFORMATION_PATH)

    def load_file_info(self):
        self.file_info_dict: dict = utils.read_json_file(STORAGE_INFORMATION_PATH)

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        sub_command = parser.add_subparsers(help="sub commend")

        parser_add = sub_command.add_parser(Program.Command.add.name, help="add file")

        parser_add.add_argument("file_name", nargs=1, type=str)
        parser_add.add_argument("-c", "--comment", required=False)
        parser_add.set_defaults(command=Program.Command.add)

        parser_cat = sub_command.add_parser(Program.Command.cat.name, help="see content of file")
        parser_cat.add_argument("file_name", nargs=1, type=str)
        parser_cat.set_defaults(command=Program.Command.cat)

        parser_list = sub_command.add_parser(Program.Command.list.name, help="list file name")
        parser_list.set_defaults(command=Program.Command.list)
        return parser.parse_args()

    def register_to_storage(self):
        file_path = os.path.join(os.getcwd(), self.file_name)
        if not os.path.exists(file_path):
            raise RuntimeError(f"file not exists: {file_path}")

        register_file_name = self.file_name
        register_file_prefix, register_file_suffix = os.path.splitext(self.file_name)
        if self.file_name in self.file_info_dict.keys():
            suffix = 1
            while True:
                register_file_name = f"{register_file_prefix}_{suffix}{register_file_suffix}"
                if register_file_name in self.file_info_dict.keys():
                    suffix += 1
                else:
                    break

        file_path = os.path.join(os.getcwd(), self.file_name)
        shutil.copy(file_path, os.path.join(STORAGE_FOLDER, register_file_name))
        self.file_info_dict[register_file_name] = Program.FileDetail(
            comment=self.comment
        ).model_dump()
        utils.print_when_debug(json.dumps(self.file_info_dict, indent=2))

    def run(self):
        args = self.get_args()
        if args.command == Program.Command.add:
            self.file_name = args.file_name[0]
            self.comment = args.comment
            self.register_to_storage()
            self.save_file_info()
            self.upload_files()
        elif args.command == Program.Command.cat:
            self.file_name = args.file_name[0]
            ...
        elif args.command == Program.Command.list:
            ...
        else:
            raise RuntimeError

    def see_file_content(self):
        ...

    def upload_files(self):
        gist_data = api.Gist().get_gist(GIST_ID)
        file_dict = {}
        # for files in os.listdir(os.PATH)
        res = api.Gist().update_gist(
            GIST_ID, api.GistModel(description=gist_data.description, public=gist_data.public)
        )
        ...
        # self.git_cli.fetch()
        # self.git_cli.pull()
        # staged_files = [pth.a_path for pth in self.cur_repo.index.diff("HEAD")]
        # config_files = []
        # for fl in self.cur_repo.untracked_files:
        #     if re.fullmatch(REGEX, fl):
        #         config_files.append(fl)
        # if len(config_files) != 0:
        #     self.git_cli.reset()
        #     self.git_cli.add("files/**")
        #     self.cur_repo.index.commit("automatic commit")
        #     self.git_cli.push()
        #     self.cur_repo.index.add(staged_files)
        # print_when_debug(self.cur_repo.untracked_files)
        # print_when_debug([pth.a_path for pth in self.cur_repo.index.diff("HEAD")])

    def sync_files(self):
        gist_data = api.Gist().get_gist(GIST_ID)
        for file_name in gist_data.files:
            with open(os.path.join(CACHE_DIR, file_name), "w", encoding="utf-8") as f:
                f.write(gist_data.files[file_name]["content"])
        


def main():
    Program().run()


if __name__ == "__main__":
    main()
