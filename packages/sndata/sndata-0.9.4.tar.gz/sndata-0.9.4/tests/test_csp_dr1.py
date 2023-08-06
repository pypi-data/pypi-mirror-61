#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``csp.dr1`` module."""

from sndata import csp
from .base_tests import DataParsingTestBase, DocumentationTestBase


class DataParsing(DataParsingTestBase):
    """Tests for the csp.dr1 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr1
        cls.module.download_module_data()

    def test_bad_object_id_err(self):
        self._test_bad_object_id_err()

    def test_ids_are_sorted(self):
        self._test_ids_are_sorted()

    def test_jd_time_format(self):
        self._test_jd_time_format('date')

    def test_no_empty_data_tables(self):
        self._test_no_empty_data_tables(10)

    def test_paper_tables_are_parsed(self):
        self._test_paper_tables_are_parsed()

    def test_unique_ids(self):
        self._test_unique_ids()

    def test_cache_not_mutated(self):
        self._test_cache_not_mutated()


class Documentation(DocumentationTestBase):
    """Tests for the des.SN3YR module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr1

    def test_ads_url(self):
        self._test_ads_url_status()

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_has_meta_attributes(self):
        self._test_has_meta_attributes()

    def test_survey_url(self):
        self._test_survey_url_status()
