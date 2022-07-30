# Copyright (c) 2014 pre-commit dev team: Anthony Sottile, Ken Struys
from __future__ import annotations

import pytest

from prepare_commit_msg.util import CalledProcessError
from prepare_commit_msg.util import cmd_output


def test_raises_on_error() -> None:
    with pytest.raises(CalledProcessError):
        cmd_output('sh', '-c', 'exit 1')


def test_output() -> None:
    ret = cmd_output('sh', '-c', 'echo hi')
    assert ret == 'hi\n'
