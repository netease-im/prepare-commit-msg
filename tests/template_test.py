from __future__ import annotations

import os

import pytest

from prepare_commit_msg.template import get_default_template
from prepare_commit_msg.template import get_rendered_template
from prepare_commit_msg.template import get_template


def test_get_template():
    template = get_template('prepare_commit_msg_append.j2')
    assert 'original' in template
    assert 'Relates' in template
    assert 'rest' in template


def test_get_template_fail():
    with pytest.raises(FileNotFoundError):
        get_template('non_existent_file.j2')


def test_get_template_absolute_path():
    path = os.path.abspath(
        __file__ +
        '/../../prepare_commit_msg/templates/prepare_commit_msg_append.j2',
    )

    template = get_template(path)
    assert 'original' in template
    assert 'Relates' in template
    assert 'rest' in template


def test_get_rendered_template():
    path = get_default_template()
    ticket = 'TEST-001'
    initial = 'Test comment\n'
    commented = ['Line1\n', 'Line2\n']
    text = get_rendered_template(
        path, {
            'ticket': ticket,
            'original': initial,
            'rest': commented,
        },
    )

    assert text == 'Test comment\n\nRelates: #TEST-001\n\nLine1\nLine2\n'
