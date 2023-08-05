import os

from unittest import TestCase

from coregen.common import (
    same_paths,
    enter_directory_ctx,
    )


class TestCommonFunctions(TestCase):

    def test_same_paths(self):
        self.assertTrue(same_paths('/dev', '/dev'))
        self.assertFalse(same_paths('/dev', '/dev/zero'))
        with enter_directory_ctx('/var/log'):
            same_paths('../log', '/var/log')
