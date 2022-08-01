from __future__ import annotations

import pytest

from prepare_commit_msg.hook import main
from prepare_commit_msg.util import cmd_output
from testing.util import get_resource_path

with open(get_resource_path('actual/message_empty')) as file:
    actual_empty = file.read()
with open(get_resource_path('actual/message_initial')) as file:
    actual_initial = file.read()
with open(get_resource_path('actual/message_large')) as file:
    actual_large = file.read()

with open(get_resource_path('expected/message_empty')) as file:
    expected_empty = file.read()
with open(get_resource_path('expected/message_initial')) as file:
    expected_initial = file.read()
with open(get_resource_path('expected/message_large')) as file:
    expected_large = file.read()


TESTS_TEMPLATES = (
    (
        actual_empty.encode(),
        expected_empty.encode(),
        'feature/test',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        actual_initial.encode(),
        expected_initial.encode(),
        'feature/test',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        actual_large.encode(),
        expected_large.encode(),
        'feature/test',  # this should not trigger anything
        'prepare_commit_msg_append.j2',
        'message',
    ),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template', 'source'),
    TESTS_TEMPLATES,
)
def test_main_separating_content(
        input_s, expected_val, branch_name, template, source,
        temp_git_dir,
):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('file.txt')
        path.write_binary(input_s)
        assert path.read_binary() == input_s

        cmd_output('git', 'checkout', '-b', branch_name)
        assert main(
            argv=[
                '-t', template,
                '-p', '(?<=feature/).*',
                str(path),
                source,
            ],
        ) == 0
        assert path.read_binary() == expected_val
