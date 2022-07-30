# Copyright (c) 2014 pre-commit dev team: Anthony Sottile, Ken Struys
from __future__ import annotations

import pytest

from prepare_commit_msg.util import cmd_output


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits')
    cmd_output('git', 'init', '--', str(git_dir))
    yield git_dir
