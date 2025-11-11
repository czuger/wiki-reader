import unittest

from core.libs.convert_date_ranges_to_tuples import convert_date_ranges_to_tuples


class TestConvertDateRangesToTuples(unittest.TestCase):
    """Test cases for the convert_date_ranges_to_tuples function."""

    def test_single_date_range(self):
        """Test conversion of a single date range."""
        result = convert_date_ranges_to_tuples("Philippe III (1245-1285)")
        self.assertEqual(result, "Philippe III (1245, 1285)")

    def test_multiple_date_ranges(self):
        """Test conversion of multiple date ranges."""
        text = "Philippe III le Hardi (1245-1285), fils de Louis IX (1214-1270)"
        expected = "Philippe III le Hardi (1245, 1285), fils de Louis IX (1214, 1270)"
        result = convert_date_ranges_to_tuples(text)
        self.assertEqual(result, expected)

    def test_date_range_with_spaces(self):
        """Test conversion with spaces around hyphen."""
        result = convert_date_ranges_to_tuples("Philippe III (1245 - 1285)")
        self.assertEqual(result, "Philippe III (1245, 1285)")

    def test_date_range_with_space_before_hyphen(self):
        """Test conversion with space before hyphen only."""
        result = convert_date_ranges_to_tuples("Philippe III (1245 -1285)")
        self.assertEqual(result, "Philippe III (1245, 1285)")

    def test_date_range_with_space_after_hyphen(self):
        """Test conversion with space after hyphen only."""
        result = convert_date_ranges_to_tuples("Philippe III (1245- 1285)")
        self.assertEqual(result, "Philippe III (1245, 1285)")

    def test_mixed_spacing(self):
        """Test conversion with mixed spacing in multiple date ranges."""
        text = "King (1245-1285) and Queen (1250 - 1300)"
        expected = "King (1245, 1285) and Queen (1250, 1300)"
        result = convert_date_ranges_to_tuples(text)
        self.assertEqual(result, expected)

    def test_no_date_range(self):
        """Test text without any date range."""
        text = "Simple text without dates"
        result = convert_date_ranges_to_tuples(text)
        self.assertEqual(result, text)

    def test_empty_string(self):
        """Test with empty string."""
        result = convert_date_ranges_to_tuples("")
        self.assertEqual(result, "")

    def test_date_not_in_parentheses(self):
        """Test that dates without parentheses are not modified."""
        text = "From 1245-1285"
        result = convert_date_ranges_to_tuples(text)
        self.assertEqual(result, text)

    def test_incomplete_date_format(self):
        """Test that incomplete date formats are not modified."""
        text = "Year (123-456)"
        result = convert_date_ranges_to_tuples(text)
        self.assertEqual(result, text)
