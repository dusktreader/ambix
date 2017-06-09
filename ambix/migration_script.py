import collections
import re
import redbaron

from ambix.exceptions import AmbixError


class MigrationScript:

    def __init__(self, revision=None, down_revision=None, file_path=None):
        self.revision = revision
        self.down_revision = down_revision
        self.file_path = file_path

    @classmethod
    def parse_file(cls, file_path):
        with AmbixError.handle_errors(
                'failed to parse migration script {}', file_path,
        ):
            with open(file_path) as script:
                content = script.read()
            red = redbaron.RedBaron(content)
        self = cls(
            revision=red.find(
                'assignment',
                target=lambda t: t.value == 'revision',
            ).value.to_python(),
            down_revision=red.find(
                'assignment',
                target=lambda t: t.value == 'down_revision',
            ).value.to_python(),
            file_path=file_path,
        )
        return self

    def change_down_revision(self, *new_down_revisions):

        if len(new_down_revisions) == 1:
            new_down_revisions = new_down_revisions[0]

        with AmbixError.handle_errors('failed while changing down revision'):
            with open(self.file_path) as script:
                content = script.read()
            red = redbaron.RedBaron(content)
            red.find(
                'assignment',
                target=lambda t: t.value == 'down_revision',
            ).value.replace(repr(new_down_revisions))

            if type(red[0]) is redbaron.nodes.StringNode:
                if (
                    isinstance(new_down_revisions, collections.Iterable) and
                    not isinstance(new_down_revisions, str)
                ):
                    rev_string = ', '.join(new_down_revisions)
                else:
                    rev_string = str(new_down_revisions)

                new_docs = re.sub(
                    r'Revises:\s*.*$',
                    'Revises: {}'.format(rev_string),
                    red[0].value,
                    flags=re.MULTILINE,
                )
                print('new docs: {}'.format(new_docs))
                red[0].replace(new_docs)
            with open(self.file_path, 'w') as script:
                script.write(red.dumps())
            self.down_revision = new_down_revisions
