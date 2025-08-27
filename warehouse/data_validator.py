import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataValidator:
    """Data validation and quality checks for ETL pipeline"""
    
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_students_data(self, df):
        """Validate student data quality"""
        if df.empty:
            return False, ["Empty dataset"]
        
        errors = []
        warnings = []
        
        # Check for different possible column name patterns
        possible_id_columns = ['student_id', 'Student_ID', 'id']
        possible_name_columns = ['name', 'Name', 'First_Name', 'first_name']
        possible_age_columns = ['age', 'Age']
        possible_major_columns = ['major', 'Major', 'Course', 'course']
        
        # Find actual columns
        id_col = next((col for col in possible_id_columns if col in df.columns), None)
        name_col = next((col for col in possible_name_columns if col in df.columns), None)
        age_col = next((col for col in possible_age_columns if col in df.columns), None)
        major_col = next((col for col in possible_major_columns if col in df.columns), None)
        
        # Check required columns
        if not id_col:
            errors.append("Missing student ID column")
        if not name_col:
            errors.append("Missing name column")
        
        # Check data types
        if id_col and not pd.api.types.is_string_dtype(df[id_col]):
            warnings.append(f"{id_col} should be string type")
        
        if age_col and not pd.api.types.is_numeric_dtype(df[age_col]):
            warnings.append(f"{age_col} should be numeric")
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            warnings.append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
        
        # Check age range if age column exists
        if age_col:
            age_range = df[age_col].describe()
            if age_range['min'] < 0 or age_range['max'] > 120:
                warnings.append(f"Age values seem unrealistic: min={age_range['min']}, max={age_range['max']}")
        
        return len(errors) == 0, errors + warnings
    
    def validate_weather_data(self, df):
        """Validate weather data quality"""
        if df.empty:
            return False, ["Empty dataset"]
        
        errors = []
        warnings = []
        
        # Check required columns
        required_columns = ['city', 'temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Check temperature range
        if 'temperature' in df.columns:
            temp_range = df['temperature'].describe()
            if temp_range['min'] < -100 or temp_range['max'] > 100:
                warnings.append(f"Temperature values seem unrealistic: min={temp_range['min']}, max={temp_range['max']}")
        
        # Check humidity range
        if 'humidity' in df.columns:
            humidity_range = df['humidity'].describe()
            if humidity_range['min'] < 0 or humidity_range['max'] > 100:
                warnings.append(f"Humidity values seem unrealistic: min={humidity_range['min']}, max={humidity_range['max']}")
        
        return len(errors) == 0, errors + warnings
    
    def validate_news_data(self, df):
        """Validate news data quality"""
        if df.empty:
            return False, ["Empty dataset"]
        
        errors = []
        warnings = []
        
        # Check required columns
        required_columns = ['headline']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Check headline length
        if 'headline' in df.columns:
            headline_lengths = df['headline'].str.len()
            if headline_lengths.max() > 500:
                warnings.append("Some headlines are very long (>500 characters)")
            if headline_lengths.min() < 5:
                warnings.append("Some headlines are very short (<5 characters)")
        
        return len(errors) == 0, errors + warnings
    
    def validate_scores_data(self, df):
        """Validate scores data quality"""
        if df.empty:
            return False, ["Empty dataset"]
        
        errors = []
        warnings = []
        
        # Check for different possible column name patterns
        possible_id_columns = ['student_id', 'Student_ID', 'id']
        possible_score_columns = ['score', 'Score']
        possible_subject_columns = ['subject', 'Subject', 'Course', 'course']
        
        # Find actual columns
        id_col = next((col for col in possible_id_columns if col in df.columns), None)
        score_col = next((col for col in possible_score_columns if col in df.columns), None)
        subject_col = next((col for col in possible_subject_columns if col in df.columns), None)
        
        # Check required columns
        if not id_col:
            errors.append("Missing student ID column")
        if not score_col:
            errors.append("Missing score column")
        
        # Check score range
        if score_col:
            score_range = df[score_col].describe()
            if score_range['min'] < 0 or score_range['max'] > 100:
                warnings.append(f"Score values seem unrealistic: min={score_range['min']}, max={score_range['max']}")
        
        return len(errors) == 0, errors + warnings
    
    def validate_dataset(self, dataset_name, df):
        """Validate dataset based on its type"""
        logger.info(f"Validating {dataset_name} dataset...")
        
        if dataset_name == 'students':
            is_valid, messages = self.validate_students_data(df)
        elif dataset_name == 'weather':
            is_valid, messages = self.validate_weather_data(df)
        elif dataset_name == 'news':
            is_valid, messages = self.validate_news_data(df)
        elif dataset_name == 'scores':
            is_valid, messages = self.validate_scores_data(df)
        else:
            logger.warning(f"Unknown dataset type: {dataset_name}")
            return True, ["Unknown dataset type - skipping validation"]
        
        # Log validation results
        if is_valid:
            logger.info(f"{dataset_name} validation passed")
        else:
            logger.error(f"{dataset_name} validation failed")
        
        for msg in messages:
            if is_valid:
                logger.warning(f"{dataset_name}: {msg}")
            else:
                logger.error(f"{dataset_name}: {msg}")
        
        return is_valid, messages
    
    def get_validation_summary(self):
        """Get summary of all validation results"""
        return {
            'errors': self.validation_errors,
            'warnings': self.validation_warnings,
            'total_errors': len(self.validation_errors),
            'total_warnings': len(self.validation_warnings)
        }
    
    def clear_validation_log(self):
        """Clear validation log"""
        self.validation_errors = []
        self.validation_warnings = []
