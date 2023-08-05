#!/usr/bin/env python
# coding: utf-8

import os
import sys
import unittest
from argparse import Namespace

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import hca
from hca.upload.cli.list_areas_command import ListAreasCommand
from test import CapturingIO


class TestUploadCliListAreasCommand(unittest.TestCase):

    def test_it_lists_areas_when_there_are_some(self):
        a_uuid = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        b_uuid = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
        config = hca.get_config()
        config.upload = {
            'areas': {
                a_uuid: {'uri': "s3://foo/{}/".format(a_uuid)},
                b_uuid: {'uri': "s3://foo/{}/".format(b_uuid)},
            },
            'current_area': a_uuid
        }
        config.save()

        with CapturingIO('stdout') as stdout:
            ListAreasCommand(Namespace())

        self.assertRegex(stdout.captured(), "%s <- selected" % a_uuid)
        self.assertRegex(stdout.captured(), b_uuid)


if __name__ == "__main__":
    unittest.main()
