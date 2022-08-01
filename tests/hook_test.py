from __future__ import annotations

from os import linesep

import pytest

from prepare_commit_msg.hook import get_current_branch
from prepare_commit_msg.hook import main
from prepare_commit_msg.hook import update_commit_file
from prepare_commit_msg.template import get_template
from prepare_commit_msg.util import cmd_output


def test_current_branch(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'checkout', '-b', 'feature')
        assert get_current_branch() == 'feature'

        cmd_output('git', 'checkout', '-b', 'feature/branch')
        assert get_current_branch() == 'feature/branch'


# Input, expected value, branch, template
TESTS = (
    (
        b'',
        f'[1.0.0] {linesep}{linesep}'.encode(),
        'release/1.0.0',  # but this should
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        b'',
        f'[TT-01] {linesep}{linesep}'.encode(),
        'feature/TT-01',
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        b'[TT-02] Some message',
        b'[TT-02] Some message',
        'feature/TT-02',
        'prepare_commit_msg_prepend.j2',
        'commit',
    ),
    (
        b'Initial message',
        f'[TT-03] Initial message{linesep}{linesep}'.encode(),
        'feature/TT-03',
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        b'',
        f'{linesep}{linesep}Relates: #AA-01{linesep}{linesep}'.encode(),
        'feature/AA-01',
        'prepare_commit_msg_append.j2',
        'message',
    ),
    (
        b'Initial message',
        f'Initial message{linesep}{linesep}Relates: #AA-02{linesep}{linesep}'
        .encode(),
        'feature/AA-02',
        'prepare_commit_msg_append.j2',
        'message',
    ),
)


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template', 'source'),
    TESTS,
)
def test_update_commit_file(
        input_s, expected_val, branch_name, template, source,
        temp_git_dir,
):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('COMMIT_EDITMSG')
        path.write_binary(input_s)
        parts = branch_name.split('/')
        ticket = str(parts[1]) if len(parts) > 1 else str(parts[0])
        update_commit_file(path, get_template(template), ticket, source)

        assert path.read_binary() == expected_val


def test_update_commit_file_os_error(temp_git_dir):
    with temp_git_dir.as_cwd():
        path = temp_git_dir.join('COMMIT_EDITMSG')
        ticket = 'TICKET-01'
        result = update_commit_file(path, '', ticket, 'message')

        assert result == 1


@pytest.mark.parametrize(
    ('input_s', 'expected_val', 'branch_name', 'template', 'source'),
    TESTS,
)
def test_main(
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
                '-p', '(?<=release/).*',
                str(path),
                source,
            ],
        ) == 0
        assert path.read_binary() == expected_val


TESTS_TEMPLATES = (
    (
        b'',
        b'',
        'test',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        b'',
        b'',
        'master',  # this should not trigger anything
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        f'Initial Message{linesep}{linesep}# Git commented{linesep}# '
        f'output simulated'.encode(),
        f'[1.0.0] Initial Message{linesep}{linesep}# Git commented{linesep}# '
        f'output simulated'.encode(),
        'release/1.0.0',  # but this should
        'prepare_commit_msg_prepend.j2',
        'message',
    ),
    (
        f'Initial Message{linesep}# Git commented{linesep}# output '
        f'simulated'.encode(),
        f'Initial Message{linesep}{linesep}Relates: #1.0.0{linesep}{linesep}'
        f'# Git commented{linesep}# output simulated'.encode(),
        'release/1.0.0',  # but this should
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
                '-p', '(?<=release/).*',
                str(path),
                source,
            ],
        ) == 0
        assert path.read_binary() == expected_val
