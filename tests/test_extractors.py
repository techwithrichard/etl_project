"""
Tests for data extraction modules
"""

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

class TestExtractors(unittest.TestCase):
    """Test cases for data extractors"""
    
    def test_excel_extractor_sample_data(self):
        """Test that excel extractor returns sample data when files don't exist"""
        from extract.excel_extractor import extract_student_data
        
        # This should return sample data since the actual files don't exist
        result = extract_student_data()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)
    
    def test_web_extractor_fallback(self):
        """Test web extractor fallback to sample data"""
        from extract.web_extractor import extract_from_web
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            result = extract_from_web()
            
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)
    
    def test_api_extractor_sample_data(self):
        """Test API extractor fallback to sample data"""
        from extract.api_extractor import extract_from_weather_api
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("API error")
            result = extract_from_weather_api()
            
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
