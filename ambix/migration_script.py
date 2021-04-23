from __future__ import annotations

import collections
import pathlib
import re
import typing

import redbaron
from ambix.exceptions import AmbixError


class MigrationScript:
    def __init__(self, revision: str = None, down_revision: str = None, file_path: pathlib.Path = None):
        self.revision = revision
        self.down_revision = down_revision
        self.file_path = file_path

    def get_down_revisions(self) -> typing.Set[str]:
        if self.down_revision is None:
            return set()
        elif isinstance(self.down_revision, collections.Iterable) and not isinstance(self.down_revision, str):
            return set(self.down_revision)
        else:
            return set([self.down_revision])

    @classmethod
    def parse_file(cls, file_path: pathlib.Path) -> MigrationScript:
        with AmbixError.handle_errors(f"failed to parse migration script {file_path}"):
            red = redbaron.RedBaron(file_path.read_text())
        self = cls(
            revision=red.find(
                "assignment",
                target=lambda t: t.value == "revision",
            ).value.to_python(),
            down_revision=red.find(
                "assignment",
                target=lambda t: t.value == "down_revision",
            ).value.to_python(),
            file_path=file_path,
        )
        return self

    def change_down_revision(self, *new_down_revisions: typing.List[str]):

        # TODO: don't change revision if it's the same

        if len(new_down_revisions) == 1:
            new_down_revisions = new_down_revisions[0]
        elif len(new_down_revisions) == 0:
            new_down_revisions = None

        with AmbixError.handle_errors("failed while changing down revision"):
            red = redbaron.RedBaron(self.file_path.read_text())
            red.find(
                "assignment",
                target=lambda t: t.value == "down_revision",
            ).value.replace(repr(new_down_revisions))

            docstring = red.find(
                "string",
                value=re.compile(
                    ".*Revises.*",
                    flags=re.MULTILINE | re.DOTALL,
                ),
            )
            if docstring is not None:
                if isinstance(new_down_revisions, collections.Iterable) and not isinstance(new_down_revisions, str):
                    rev_string = ", ".join(new_down_revisions)
                else:
                    rev_string = str(new_down_revisions)

                docstring.replace(
                    re.sub(
                        r"Revises:\s*\w+",
                        f"Revises: {rev_string}",
                        str(docstring),
                        flags=re.MULTILINE,
                    )
                )

            self.file_path.write_text(red.dumps())
            self.down_revision = new_down_revisions
