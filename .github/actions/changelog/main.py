import re
import typing
from github import Github
from pydantic import BaseSettings, SecretStr
from sphobjinv import Inventory

docs_url = "https://codingame.readthedocs.io/en/latest/"
roles = {
    "attr": "attribute",
    "meth": "method",
    "exc": "exception",
}
refs = {
    "async": (
        "Asynchronous client",
        "user_guide/async.html#asynchronous-client",
    )
}


class Settings(BaseSettings):
    input_token: SecretStr
    github_repository: str


def main():
    settings = Settings(_env_file=".github/actions/changelog/.env")
    inventory = Inventory(url=docs_url + "objects.inv")
    github = Github(settings.input_token.get_secret_value())
    repo = github.get_repo(settings.github_repository)
    docs_changelog = repo.get_contents("docs/changelog.rst")

    content = docs_changelog.decoded_content.decode()
    new_content = content
    directives: typing.List[re.Match] = list(
        re.finditer(r":(\w+):`(.+?)`", content)
    )
    links: typing.List[str] = []

    for directive in directives:
        if directive[1] == "ref":
            links.append("`{} <{}>`__".format(*refs[directive[2]]))
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
                print(
                    "::warning file=CHANGELOG.rst:: "
                    f":py:{role}:`codingame.{directive[2]}` not found"
                )
                links.append(f"``{directive[2]}``")
                continue

            obj = inventory.objects[index]
            links.append(
                f"` ``{obj.dispname_expanded[len('codingame.'):]}`` "
                f"<{docs_url + obj.uri_expanded}>`__"
            )

    for directive, link in zip(directives[::-1], links[::-1]):
        new_content = (
            new_content[: directive.start()]
            + link
            + new_content[directive.end() :]  # noqa: E203
        )

    new_content = new_content[
        len(".. currentmodule:: codingame\n\n") :  # noqa: E203
    ]

    changelog = repo.get_contents("CHANGELOG.rst")
    if new_content != changelog.decoded_content.decode():
        repo.update_file(
            changelog.path, "Update CHANGELOG.rst", new_content, changelog.sha
        )


if __name__ == "__main__":
    main()
