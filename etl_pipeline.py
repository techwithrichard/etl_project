import uuid
import logging
from datetime import datetime
from extract.mysql_extractor import extract_from_mysql
from extract.api_extractor import extract_from_weather_api
from extract.web_extractor import extract_from_web
from extract.excel_extractor import extract_student_data
from transform.data_transformer import transform_data
from load.data_loader import load_data
from warehouse.warehouse_manager import WarehouseManager
from warehouse.data_validator import DataValidator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    """Enhanced ETL pipeline with warehouse integration and validation"""
    
    # Generate unique run ID
    run_id = str(uuid.uuid4())[:8]
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    logger.info(f"Starting ETL Pipeline - Run ID: {run_id}")
    
    # Initialize warehouse and validator
    warehouse = WarehouseManager()
    validator = DataValidator()
    
    try:
        # EXTRACT phase
        logger.info("1. Extracting data from sources...")
        extracted_data = {}
        
        # Extract from MySQL
        try:
            mysql_data = extract_from_mysql()
            extracted_data['mysql'] = mysql_data
            logger.info(f"MySQL extraction: {len(mysql_data)} records")
        except Exception as e:
            logger.error(f"MySQL extraction failed: {e}")
            mysql_data = None
        
        # Extract from Weather API
        try:
            weather_data = extract_from_weather_api(["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"])
            extracted_data['weather'] = weather_data
            logger.info(f"Weather extraction: {len(weather_data)} records")
        except Exception as e:
            logger.error(f"Weather extraction failed: {e}")
            weather_data = None
        
        # Extract from Web
        try:
            web_data = extract_from_web()
            extracted_data['web'] = web_data
            logger.info(f"Web extraction: {len(web_data)} records")
        except Exception as e:
            logger.error(f"Web extraction failed: {e}")
            web_data = None
        
        # Extract from Excel
        try:
            excel_data = extract_student_data()
            extracted_data['excel'] = excel_data
            logger.info(f"Excel extraction: {len(excel_data)} records")
        except Exception as e:
            logger.error(f"Excel extraction failed: {e}")
            excel_data = None
        
        # TRANSFORM phase
        logger.info("2. Transforming data...")
        try:
            transformed_data = transform_data(mysql_data, weather_data, web_data, excel_data)
            logger.info(f"Transformation completed: {len(transformed_data)} datasets")
        except Exception as e:
            logger.error(f"Transformation failed: {e}")
            raise
        
        # VALIDATION phase
        logger.info("3. Validating data quality...")
        validation_results = {}
        total_records = 0
        
        for dataset_name, df in transformed_data.items():
            if df is not None and not df.empty:
                is_valid, messages = validator.validate_dataset(dataset_name, df)
                validation_results[dataset_name] = {
                    'is_valid': is_valid,
                    'messages': messages,
                    'record_count': len(df)
                }
                total_records += len(df)
        
        # WAREHOUSE LOAD phase
        logger.info("4. Loading data to warehouse...")
        warehouse_records = 0
        
        for dataset_name, df in transformed_data.items():
            if df is not None and not df.empty:
                try:
                    records_stored = warehouse.store_data(dataset_name, df, run_id)
                    warehouse_records += records_stored
                    logger.info(f"{dataset_name}: {records_stored} records stored in warehouse")
                except Exception as e:
                    logger.error(f"Failed to store {dataset_name} in warehouse: {e}")
        
        # FILE LOAD phase (keep existing functionality)
        logger.info("5. Saving data to files...")
        try:
            output_paths = load_data(transformed_data, 'json')
            logger.info(f"Files saved: {list(output_paths.keys())}")
        except Exception as e:
            logger.error(f"File saving failed: {e}")
            output_paths = {}
        
        # Log pipeline run
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        warehouse.log_pipeline_run(
            run_id=run_id,
            start_time=start_time,
            end_time=end_time,
            status='SUCCESS',
            records_processed=total_records
        )
        
        logger.info(f"ETL Pipeline completed successfully! Run ID: {run_id}")
        logger.info(f"Total records processed: {total_records}")
        logger.info(f"Records stored in warehouse: {warehouse_records}")
        
        return {
            'transformed_data': transformed_data,
            'output_paths': output_paths,
            'run_id': run_id,
            'validation_results': validation_results,
            'warehouse_summary': warehouse.get_warehouse_summary(),
            'analytics': warehouse.run_analytics()
        }
        
    except Exception as e:
        # Log failed pipeline run
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        warehouse.log_pipeline_run(
            run_id=run_id,
            start_time=start_time,
            end_time=end_time,
            status='FAILED',
            records_processed=0,
            error_message=str(e)
        )
        
        logger.error(f"ETL Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    try:
        result = run_etl_pipeline()
        print(f"\nPipeline completed successfully!")
        print(f"Run ID: {result['run_id']}")
        print(f"Datasets: {list(result['transformed_data'].keys())}")
        print(f"Total records: {sum(len(df) for df in result['transformed_data'].values())}")
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        exit(1)