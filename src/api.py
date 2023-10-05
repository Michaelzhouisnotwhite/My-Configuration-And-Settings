import requests
import settings
from datetime import datetime
import pytz
from pydantic import BaseModel
from utils import print_when_debug


class GistModel(BaseModel):
    description: str = ""
    files: dict
    public: bool = False


class Gist:
    url = "https://api.github.com/gists"

    def __init__(self) -> None:
        with open(settings.TOKEN_PATH, "r") as f:
            self.token = f.read()
        self.header = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        pass

    def create_gist(self):
        cur_datetime = datetime.now(pytz.timezone(settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")

        # try:
        req = requests.post(
            self.url,
            headers=self.header,
            json=GistModel(
                description="config gist",
                public=False,
                files={"info.txt": {"content": f"time: {cur_datetime}"}},
            ).model_dump(),
            timeout=10000,
        )
        # except (TimeoutError, requests.ConnectionError) as e:
        #     print(e.args)
        #     return

        print_when_debug(req.json())
        return req.json()["url"]

    def get_gist(self, gist_id: str):
        req = requests.get(f"{self.url}/{gist_id}", headers=self.header, timeout=10000)
        if req.status_code != 200:
            raise requests.RequestException()
        result_dict = req.json()
        new_dict = {}
        for key_name in GistModel.model_fields:
            new_dict[key_name] = result_dict[key_name]
        return GistModel(**new_dict)

    def update_gist(self, gist_id: str, data: GistModel):
        req = requests.patch(
            f"{self.url}/{gist_id}", headers=self.header, timeout=10000, json=data.model_dump()
        )
        return req.json()
        ...


if __name__ == "__main__":
    Gist().create_gist()
