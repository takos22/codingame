import re
import traceback
import typing

from github import Github
from pydantic import BaseSettings, SecretStr
from sphobjinv import Inventory

DOCS_BASE_URL = "https://codingame.readthedocs.io/en/"

ref_to_doc_branch = {"dev": "latest", "master": "stable"}
roles = {
    "attr": "attribute",
    "meth": "method",
    "exc": "exception",
}
refs = {
    "async": (
        "Asynchronous client",
        "user_guide/quickstart.html#about-the-asynchronous-client",
    ),
    "login": (
        "Login",
        "user_guide/quickstart.html#login",
    ),
}


class Settings(BaseSettings):
    input_token: SecretStr
    github_repository: str
    github_ref: str
    github_ref_name: str


def main():
    settings = Settings(_env_file=".github/actions/changelog/.env")
    github = Github(settings.input_token.get_secret_value())
    repo = github.get_repo(settings.github_repository)
    docs_changelog = repo.get_contents(
        "docs/changelog.rst", settings.github_ref.split("/")[-1]
    )
    log("debug", f"docs/changelog.rst at {settings.github_ref_name} downloaded")

    docs_url = (
        DOCS_BASE_URL
        + (
            settings.github_ref_name
            if settings.github_ref_name.startswith("v")
            else ref_to_doc_branch.get(settings.github_ref_name, "latest")
        )
        + "/"
    )
    log("notice", f"Using docs at {docs_url}")

    inventory = Inventory(url=docs_url + "objects.inv")

    content = docs_changelog.decoded_content.decode()
    new_content = content
    directives: typing.List[re.Match] = list(
        re.finditer(r":(\w+):`(.+?)`", content)
    )
    links: typing.List[str] = []
    log("debug", f"Found {len(directives)} in docs/changelog.rst")
    log("group", "Directive search")

    for directive in directives:
        if directive[1] == "ref":
            links.append("`{} <{}>`__".format(*refs[directive[2]]))
            log("debug", f"Found :ref:`{directive[2]}`")
        else:
            role = roles.get(directive[1], directive[1])
            try:
                index = [
                    i
                    for _, i in inventory.suggest(
                        f":py:{role}:`codingame.{directive[2]}`",
                        with_index=True,
                        thresh=90,
                    )
                ][0]
            except IndexError:
                log(
                    "warning",
                    f":py:{role}:`codingame.{directive[2]}` not found",
                    title="Directive not found",
                    file="CHANGELOG.rst",
                )
                links.append(f"``{directive[2]}``")
                continue

            obj = inventory.objects[index]
            links.append(
                f"`{obj.dispname_expanded[len('codingame.'):]} "
                f"<{docs_url + obj.uri_expanded}>`__"
            )
            log("debug", f"Found :{role}:`codingame.{directive[2]}`")

    log("endgroup")

    for directive, link in zip(directives[::-1], links[::-1]):
        new_content = (
            new_content[: directive.start()]
            + link
            + new_content[directive.end() :]  # noqa: E203
        )

    new_content = new_content[
        len(".. currentmodule:: codingame\n\n") :  # noqa: E203
    ]

    changelog = repo.get_contents(
        "CHANGELOG.rst", settings.github_ref.split("/")[-1]
    )
    log("debug", f"CHANGELOG.rst at {settings.github_ref_name} downloaded")
    if new_content != changelog.decoded_content.decode():
        repo.update_file(
            changelog.path,
            "Update CHANGELOG.rst",
            new_content,
            changelog.sha,
            branch=settings.github_ref.split("/")[-1],
        )
        log(
            "notice",
            "Changelog's content changed, updated CHANGELOG.rst",
            file="CHANGELOG.rst",
        )
    else:
        log("notice", "Changelog's content hasn't changed")


LOG_PARAMETER_NAMES = {
    "end_line": "endLine",
    "column": "col",
    "end_column": "endColumn",
}


def log(
    level: str,
    message: str = "",
    title: str = None,
    file: str = None,
    line: int = None,
    end_line: int = None,
    column: int = None,
    end_column: int = None,
):
    parameters = dict(
        filter(
            lambda i: i[1] is not None,
            {
                "title": title,
                "file": file,
                "line": line,
                "end_line": end_line,
                "column": column,
                "end_column": end_column,
            }.items(),
        )
    )

    print(
        "::"
        + level
        + (
            (
                " "
                + ",".join(
                    f"{LOG_PARAMETER_NAMES.get(k, k)}={v}"
                    for k, v in parameters
                )
            )
            if parameters
            else ""
        )
        + "::"
        + message
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(
            "error",
            traceback.format_exc(),
            title=f"{e.__class__.__name__}: {str(e)}",
            file=".github/actions/changelog/main.py",
        )
        raise
