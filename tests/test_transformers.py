"""
Tests for data transformation modules
"""

import unittest
import pandas as pd
from datetime import datetime

class TestTransformers(unittest.TestCase):
    """Test cases for data transformers"""
    
    def test_data_transformer_empty_data(self):
        """Test transformer handles empty data gracefully"""
        from transform.data_transformer import transform_data
        
        # Test with empty DataFrames
        empty_df = pd.DataFrame()
        result = transform_data(empty_df, empty_df, empty_df, empty_df)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
    
    def test_data_transformer_sample_data(self):
        """Test transformer with sample data"""
        from transform.data_transformer import transform_data
        
        # Create sample data
        sample_students = pd.DataFrame({
            'student_id': [1, 2],
            'name': ['John', 'Jane'],
            'age': [20, 21],
            'major': ['CS', 'DS']
        })
        
        sample_weather = pd.DataFrame({
            'city': ['Nairobi'],
            'temperature': [25.0],
            'humidity': [60]
        })
        
        sample_web = pd.DataFrame({
            'headline': ['Test Headline'],
            'source': ['Test Source'],
            'scraped_at': [datetime.now()]
        })
        
        sample_excel = pd.DataFrame({
            'Student_ID': ['S001'],
            'Score': [85],
            'Subject': ['Math']
        })
        
        result = transform_data(sample_students, sample_weather, sample_web, sample_excel)
        
        self.assertIsInstance(result, dict)
        self.assertIn('students', result)
        self.assertIn('weather', result)
        self.assertIn('news', result)
        self.assertIn('scores', result)

if __name__ == '__main__':
    unittest.main()
