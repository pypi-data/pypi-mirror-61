#!/usr/bin/env python
# coding: utf-8
import itertools
import time
import os
import sys
import unittest
from argparse import Namespace

import responses
from mock import Mock, patch

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from hca.upload.cli.upload_command import UploadCommand
from test import TEST_DIR
from test.integration.upload import UploadTestCase


class TestUploadCliUploadCommand(UploadTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.area = self.mock_current_upload_area()
        self.test_files = ['LICENSE', 'README.rst']

    def upload_command(self, args):
        for arg in args.upload_paths + [args.target_filename or '']:
            if os.path.isdir(arg):
                for path in itertools.chain.from_iterable((f for _, _, f in os.walk(arg))):
                    self.add_upload_mock(self.area.uuid, path)
            elif arg:  # ignore '' (but not arbitrary file names)
                self.add_upload_mock(self.area.uuid, arg)
        return UploadCommand(args)

    @responses.activate
    def test_upload_with_target_filename_option(self):
        args = Namespace(
            upload_paths=[os.path.join(TEST_DIR, "res", "bundle", "sample.json")],
            target_filename='FOO',
            no_transfer_acceleration=False,
            quiet=True,
            file_extension=None,
            sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)

        self.upload_command(args)

        obj = self.upload_bucket.Object("{}/FOO".format(self.area.uuid))
        self.assertEqual(obj.content_type, 'application/json; dcp-type=data')
        with open(os.path.join(TEST_DIR, "res", "bundle", "sample.json"), 'rb') as fh:
            expected_contents = fh.read()
            self.assertEqual(obj.get()['Body'].read(), expected_contents)

    @responses.activate
    def test_parse_s3_path_with_no_prefix(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        s3_path_with_no_prefix = "s3://fake-bucket"

        bucket, prefix = upload_command._parse_s3_path(s3_path_with_no_prefix)

        self.assertEqual(bucket, "fake-bucket")
        self.assertEqual(prefix, "")

    @responses.activate
    def test_parse_s3_path_with_dir_prefix(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        s3_path_with_no_prefix = "s3://fake-bucket/fake-dir/"

        bucket, prefix = upload_command._parse_s3_path(s3_path_with_no_prefix)

        self.assertEqual(bucket, "fake-bucket")
        self.assertEqual(prefix, "fake-dir/")

    @responses.activate
    def test_parse_s3_path_with_obj_prefix(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        s3_path_with_no_prefix = "s3://fake-bucket/fake-dir/fake-obj"

        bucket, prefix = upload_command._parse_s3_path(s3_path_with_no_prefix)

        self.assertEqual(bucket, "fake-bucket")
        self.assertEqual(prefix, "fake-dir/fake-obj")

    @responses.activate
    def test_retrieve_files_list_and_size_sum_tuple_from_s3_path_with_dir_key(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        area_s3_path = "s3://{0}/{1}".format(self.upload_bucket_name, self.area.uuid)

        s3_file_paths, total_fize_size = upload_command._retrieve_files_list_and_size_sum_tuple_from_s3_path(
            area_s3_path)

        for file in self.test_files:
            file_key = "{0}/{1}".format(area_s3_path, file)
            self.assertEqual(True, file_key in s3_file_paths)
        self.assertIsInstance(total_fize_size, int)

    @responses.activate
    def test_retrieve_files_list_and_size_sum_tuple_from_s3_path_with_partial_obj_key(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        area_path = "s3://{0}/{1}".format(self.upload_bucket_name, self.area.uuid)
        partial_obj_key = "{0}/LIC".format(area_path)
        complete_obj_key = "{0}/LICENSE".format(area_path)

        s3_file_paths, total_fize_size = upload_command._retrieve_files_list_and_size_sum_tuple_from_s3_path(
            partial_obj_key)

        self.assertEqual(True, complete_obj_key in s3_file_paths)
        self.assertEqual(1, len(s3_file_paths))
        self.assertIsInstance(total_fize_size, int)

    @responses.activate
    def test_load_file_paths_from_upload_path_with_s3_input(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        area_path = "s3://{0}/{1}".format(self.upload_bucket_name, self.area.uuid)
        partial_obj_key = "{0}/LIC".format(area_path)
        complete_obj_key = "{0}/LICENSE".format(area_path)

        upload_command._load_file_paths_from_upload_path(args, partial_obj_key)

        self.assertEqual(True, complete_obj_key in upload_command.file_paths)
        self.assertEqual(3, len(upload_command.file_paths))
        self.assertIsInstance(upload_command.file_size_sum, int)

    @responses.activate
    def test_retrieve_files_list_and_size_sum_tuple_from_s3_path_with_complete_obj_key(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)
        self.simulate_credentials_api(area_uuid=self.area.uuid)
        upload_command = self.upload_command(args)
        area_path = "s3://{0}/{1}".format(self.upload_bucket_name, self.area.uuid)
        complete_obj_key = "{0}/LICENSE".format(area_path)

        s3_file_paths, total_fize_size = upload_command._retrieve_files_list_and_size_sum_tuple_from_s3_path(
            complete_obj_key)

        self.assertEqual(True, complete_obj_key in s3_file_paths)
        self.assertEqual(1, len(s3_file_paths))
        self.assertIsInstance(total_fize_size, int)

    @responses.activate
    def test_upload_with_dcp_type_option(self):
        args = Namespace(upload_paths=['LICENSE'], target_filename=None, no_transfer_acceleration=False, quiet=True,
                         file_extension=None, sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)

        self.upload_command(args)

        obj = self.upload_bucket.Object("{}/LICENSE".format(self.area.uuid))
        self.assertEqual(obj.content_type, 'application/octet-stream; dcp-type=data')
        with open('LICENSE', 'rb') as fh:
            expected_contents = fh.read()
            self.assertEqual(obj.get()['Body'].read(), expected_contents)

    @responses.activate
    def test_no_transfer_acceleration_option_sets_up_botocore_config_correctly(self):
        import botocore

        with patch('hca.upload.lib.s3_agent.S3Agent.upload_local_file'), \
             patch('hca.upload.lib.s3_agent.Config', new=Mock(wraps=botocore.config.Config)) as mock_config:
            args = Namespace(upload_paths=['LICENSE'], target_filename=None, quiet=True, file_extension=None, sync=True)
            args.no_transfer_acceleration = False

            self.simulate_credentials_api(area_uuid=self.area.uuid)

            self.upload_command(args)
            mock_config.assert_called_once_with(s3={'use_accelerate_endpoint': True})

            mock_config.reset_mock()
            args.no_transfer_acceleration = True
            self.upload_command(args)
            mock_config.assert_called_once_with()

    @responses.activate
    def test_multiple_uploads(self):
        args = Namespace(upload_paths=self.test_files, target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)

        self.upload_command(args)

        for filename in self.test_files:
            obj = self.upload_bucket.Object("{}/{}".format(self.area.uuid, filename))
            with open(filename, 'rb') as fh:
                expected_contents = fh.read()
                self.assertEqual(obj.get()['Body'].read(), expected_contents)

    @responses.activate
    def test_upload_do_not_overwrite_same_file_with_sync_on(self):
        args = Namespace(upload_paths=['LICENSE'], target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)

        self.upload_command(args)
        last_modified_time_for_first_attempted_upload = self.upload_bucket.Object(
            "{}/LICENSE".format(self.area.uuid)).last_modified
        time.sleep(5)
        self.upload_command(args)
        last_modified_time_for_second_attempted_upload = self.upload_bucket.Object(
            "{}/LICENSE".format(self.area.uuid)).last_modified

        self.assertEqual(last_modified_time_for_first_attempted_upload, last_modified_time_for_second_attempted_upload)

    @responses.activate
    def test_upload_overwrite_same_file_with_sync_off(self):
        args = Namespace(upload_paths=['LICENSE'], target_filename=None, no_transfer_acceleration=False,
                         dcp_type=None, quiet=True, file_extension=None, sync=False)

        self.simulate_credentials_api(area_uuid=self.area.uuid)

        self.upload_command(args)
        last_modified_time_for_first_attempted_upload = self.upload_bucket.Object(
            "{}/LICENSE".format(self.area.uuid)).last_modified
        time.sleep(5)  # sit in the corner and think about what you've done
        self.upload_command(args)
        last_modified_time_for_second_attempted_upload = self.upload_bucket.Object(
            "{}/LICENSE".format(self.area.uuid)).last_modified

        self.assertLess(last_modified_time_for_first_attempted_upload, last_modified_time_for_second_attempted_upload)

    @responses.activate
    def test_directory_upload_path_without_file_extension(self):
        test_dir_path = os.path.join(TEST_DIR, "upload", "data")
        args = Namespace(
            upload_paths=[test_dir_path],
            target_filename=None,
            no_transfer_acceleration=False,
            quiet=True,
            file_extension=None,
            sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)
        self.upload_command(args)
        self.assertEqual(len(list(self.upload_bucket.objects.all())), 6)

    @responses.activate
    def test_directory_upload_path_with_file_extension(self):
        test_dir_path = os.path.join(TEST_DIR, "upload", "data")
        args = Namespace(
            upload_paths=[test_dir_path],
            target_filename=None,
            no_transfer_acceleration=False,
            quiet=True,
            file_extension="fastq.gz",
            sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)
        self.upload_command(args)
        self.assertEqual(len(list(self.upload_bucket.objects.all())), 3)

    @responses.activate
    def test_multiple_directory_upload_paths_without_file_extension(self):
        test_dir_path_one = os.path.join(TEST_DIR, "upload", "data", "subdir1")
        test_dir_path_two = os.path.join(TEST_DIR, "upload", "data", "subdir2")
        args = Namespace(
            upload_paths=[test_dir_path_one, test_dir_path_two],
            target_filename=None,
            no_transfer_acceleration=False,
            quiet=True,
            file_extension=None,
            sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)
        self.upload_command(args)
        self.assertEqual(len(list(self.upload_bucket.objects.all())), 3)

    @responses.activate
    def test_multiple_directory_upload_paths_with_file_extension(self):
        test_dir_path_one = os.path.join(TEST_DIR, "upload", "data", "subdir1")
        test_dir_path_two = os.path.join(TEST_DIR, "upload", "data", "subdir2")
        args = Namespace(
            upload_paths=[test_dir_path_one, test_dir_path_two],
            target_filename=None,
            no_transfer_acceleration=False,
            quiet=True,
            file_extension="fastq.gz",
            sync=True)

        self.simulate_credentials_api(area_uuid=self.area.uuid)
        self.upload_command(args)
        self.assertEqual(len(list(self.upload_bucket.objects.all())), 2)


if __name__ == "__main__":
    unittest.main()
