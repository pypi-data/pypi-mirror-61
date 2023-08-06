# -*- coding: utf-8 -*-
from datetime import datetime
import io
import os

import pytest
import six
import toml

from anymarkup_core import *

from test import *


class TestParse(object):
    fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')

    def assert_unicode(self, struct):
        if isinstance(struct, dict):
            for k, v in struct.items():
                self.assert_unicode(k)
                self.assert_unicode(v)
        elif isinstance(struct, list):
            for i in struct:
                self.assert_unicode(i)
        elif isinstance(struct, (six.string_types, type(None), type(True), \
                six.integer_types, float, datetime)):
            pass
        else:
            raise AssertionError('Unexpected type {0} in parsed structure'.format(type(struct)))

    @pytest.mark.parametrize(('str', 'fmt', 'expected'), [
        ('', None, {}),
        ('{}', None, {}),
        ('[]', None, []),
        (example_ini, None, example_as_dict),
        (example_json, None, example_as_dict),
        (example_json5, 'json5', example_as_dict),
        (example_toml, 'toml', toml_example_as_dict),  # we can't tell toml from ini
        (example_xml, None, example_as_ordered_dict),
        (example_yaml_map, None, example_as_dict),
        (example_yaml_omap, None, example_as_ordered_dict),
    ])
    def test_parse_basic(self, str, fmt, expected):
        parsed = parse(str, fmt)
        assert parsed == expected
        assert type(parsed) == type(expected)
        self.assert_unicode(parsed)

    @pytest.mark.parametrize(('str', 'fmt', 'expected'), [
        ('', None, {}),
        ('{}', None, {}),
        ('[]', None, []),
        (example_ini, None, example_as_dict),
        (example_json, None, example_as_dict),
        (example_json5, 'json5', example_as_dict),
        (example_toml, 'toml', toml_example_as_dict),  # we can't tell toml from ini
        (example_xml, None, example_as_ordered_dict),
        (example_yaml_map, None, example_as_dict),
        (example_yaml_omap, None, example_as_ordered_dict),
    ])
    def test_parse_basic_interpolation_is_false(self, str, fmt, expected):
        parsed = parse(str, fmt, interpolate=False)
        assert parsed == expected
        assert type(parsed) == type(expected)
        self.assert_unicode(parsed)


    def test_parse_interpolation_fail(self):
        with pytest.raises(AnyMarkupError):
            parse(example_ini_with_interpolation)

    def test_parse_interpolation_pass_when_false(self):
        parsed = parse(example_ini_with_interpolation, interpolate=False)
        assert type(parsed) == dict

    @pytest.mark.parametrize(('str', 'expected'), [
        ('# comment', {}),
        ('# comment\n', {}),
        ('# comment\n' + example_ini, example_as_dict),
        ('# comment\n' + example_json, example_as_dict),
        ('# comment\n' + example_json5, example_as_dict),
        ('# comment\n' + example_yaml_map, example_as_dict),
        ('# comment\n' + example_yaml_omap, example_as_ordered_dict),
        # no test for toml, since it's not auto-recognized
    ])
    def test_parse_recognizes_comments_in_ini_json_yaml(self, str, expected):
        parsed = parse(str)
        assert parsed == expected
        assert type(parsed) == type(expected)
        self.assert_unicode(parsed)

    @pytest.mark.parametrize(('str, fmt, expected'), [
        (types_ini, None, types_as_struct_with_objects),
        (types_json, None, types_as_struct_with_objects),
        (types_json5, 'json5', types_as_struct_with_objects),
        (types_toml, 'toml', toml_types_as_struct_with_objects),
        (types_xml, None, types_as_struct_with_objects),
        (types_yaml, None, types_as_struct_with_objects),
    ])
    def test_parse_force_types_true(self, str, fmt, expected):
        assert parse(str, fmt) == expected

    @pytest.mark.parametrize(('str', 'fmt', 'expected'), [
        (types_ini, None, types_as_struct_with_strings),
        (types_json, None, types_as_struct_with_strings),
        (types_json5, 'json5', types_as_struct_with_strings),
        (types_toml, 'toml', toml_types_as_struct_with_strings),
        (types_xml, None, types_as_struct_with_strings),
        (types_yaml, None, types_as_struct_with_strings),
    ])
    def test_parse_force_types_false(self, str, fmt, expected):
        assert parse(str, fmt, force_types=False) == expected

    @pytest.mark.parametrize(('str', 'fmt', 'expected'), [
        # Note: the expected result is backend-specific
        (types_ini, None, {'x': {'a': '1', 'b': '1.1', 'c': 'None', 'd': 'True'}}),
        (types_json, None, {'x': {'a': 1, 'b': 1.1, 'c': None, 'd': True}}),
        (types_json5, 'json5', {'x': {'a': 1, 'b': 1.1, 'c': None, 'd': True}}),
        (types_toml, 'toml', {'x': {'a': 1, 'b': 1.1,
                                    'c': datetime(1987, 7, 5, 17, 45, tzinfo=TomlTz('Z')),
                                    'd': True}}),
        (types_xml, None, {'x': {'a': '1', 'b': '1.1', 'c': 'None', 'd': 'True'}}),
        (types_yaml, None, {'x': {'a': 1, 'b': 1.1, 'c': 'None', 'd': True}}),
    ])
    def test_parse_force_types_none(self, str, fmt, expected):
        assert parse(str, fmt, force_types=None) == expected

    def test_parse_works_with_bytes_yielding_file(self):
        f = open(os.path.join(self.fixtures, 'empty.ini'), 'rb')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_works_with_unicode_yielding_file(self):
        # on Python 2, this can only be simulated with io.open
        f = io.open(os.path.join(self.fixtures, 'empty.ini'), encoding='utf-8')
        parsed = parse(f)
        assert parsed == {}

    def test_parse_fails_on_wrong_format(self):
        with pytest.raises(AnyMarkupError):
            parse('foo: bar', format='xml')

    @pytest.mark.parametrize(('file', 'expected'), [
        # TODO: some parsers allow empty files, others don't - this should be made consistent
        ('empty.ini', {}),
        ('empty.json', AnyMarkupError),
        ('empty.json5', AnyMarkupError),
        ('empty.toml', {}),
        ('empty.xml', AnyMarkupError),
        ('empty.yaml', {}),
        ('example.ini', example_as_dict),
        ('example.json', example_as_dict),
        ('example.json5', example_as_dict),
        ('example.toml', toml_example_as_dict),
        ('example.xml', example_as_ordered_dict),
        ('example.yaml', example_as_dict),
    ])
    def test_parse_file_basic(self, file, expected):
        f = os.path.join(self.fixtures, file)
        if expected == AnyMarkupError:
            with pytest.raises(AnyMarkupError):
                parse_file(f)
        else:
            parsed = parse_file(f)
            assert parsed == expected
            self.assert_unicode(parsed)

    def test_parse_file_noextension(self):
        parsed = parse_file(os.path.join(self.fixtures, 'without_extension'))
        assert parsed == example_as_dict
        self.assert_unicode(parsed)

    def test_parse_file_fails_on_bad_extension(self):
        with pytest.raises(AnyMarkupError):
            parse_file(os.path.join(self.fixtures, 'bad_extension.xml'))

    def test_parse_file_respects_force_types(self):
        f = os.path.join(self.fixtures, 'types.json')
        parsed = parse_file(f, force_types=True)
        assert parsed == {'a': 1, 'b': 1}
        parsed = parse_file(f, force_types=False)
        assert parsed == {'a': '1', 'b': '1'}
        parsed = parse_file(f, force_types=None)
        assert parsed == {'a': 1, 'b': '1'}
