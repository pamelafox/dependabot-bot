import pytest
import json
import os
import azure.functions as func
from GithubCallbackTrigger import main


@pytest.fixture(autouse=True)
def azure_function_environment_vars():
    with open("local.settings.json") as f:
        local_settings = json.load(f)
    for k, v in local_settings["Values"].items():
        os.environ[k] = v


def test_pull_request():
    with open("tests/pull_request.json", "rb") as pr:
        req = func.HttpRequest(method="POST", url="https://testing.com", body=pr.read())
        result = main(req)
        assert result.status_code == 200
        assert result.get_body().decode("utf8") == "Not a bot PR"


def test_dependabot_pull_request():
    with open("tests/dependabot_pr.json", "rb") as pr:
        req = func.HttpRequest(method="POST", url="https://testing.com", body=pr.read())
        result = main(req)
        assert result.status_code == 200
        assert result.get_body().decode("utf8") == "Automatically merged PR"