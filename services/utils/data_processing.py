import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Tuple, Union
from celery import shared_task
from services.exceptions import DataProcessingException

logger = logging.getLogger(__name__)

class DataProcessing:
    
    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the input DataFrame by handling missing values and removing duplicates.
        """
        try:
            # Handle missing values
            data = data.dropna(how='all')  # Drop rows where all elements are missing
            data = data.fillna(method='ffill').fillna(method='bfill')  # Fill missing values
        
            # Remove duplicates
            data = data.drop_duplicates()
            
            return data
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            raise DataProcessingException("Failed to clean data.")
    
    @staticmethod
    def transform_data(data: pd.DataFrame, transformations: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply specified transformations to the input DataFrame.
        """
        try:
            for column, transform in transformations.items():
                if column in data.columns:
                    if transform == 'log':
                        data[column] = np.log(data[column] + 1)
                    elif transform == 'sqrt':
                        data[column] = np.sqrt(data[column])
                    # Add more transformations as needed
                    else:
                        raise ValueError(f"Unsupported transformation: {transform}")
            return data
        except Exception as e:
            logger.error(f"Error transforming data: {e}")
            raise DataProcessingException("Failed to transform data.")
    
    @staticmethod
    def analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform basic data analysis and return summary statistics.
        """
        try:
            analysis_results = {
                'description': data.describe().to_dict(),
                'correlation': data.corr().to_dict(),
                # Add more analysis as needed
            }
            return analysis_results
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            raise DataProcessingException("Failed to analyze data.")
    
    @staticmethod
    @shared_task
    def process_data_task(file_path: str, transformations: Dict[str, Any]) -> str:
        """
        Celery task to process data asynchronously.
        """
        try:
            data = pd.read_csv(file_path)
            cleaned_data = DataProcessing.clean_data(data)
            transformed_data = DataProcessing.transform_data(cleaned_data, transformations)
            analysis_results = DataProcessing.analyze_data(transformed_data)
            
            # Save analysis results to a JSON file
            output_file = file_path.replace('.csv', '_analysis.json')
            with open(output_file, 'w') as f:
                json.dump(analysis_results, f)
                
            logger.info(f"Data processed and analysis saved to: {output_file}")
            return output_file
        except DataProcessingException as e:
            logger.error(f"Data processing task failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in data processing task: {e}")
            raise DataProcessingException("Unexpected error in data processing task.")
    
    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        """
        Load data from a CSV file into a DataFrame.
        """
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            raise DataProcessingException("Failed to load data.")
    
    @staticmethod
    def save_data(data: pd.DataFrame, file_path: str):
        """
        Save the DataFrame to a CSV file.
        """
        try:
            data.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")
            raise DataProcessingException("Failed to save data.")

    @staticmethod
    def filter_data(data: pd.DataFrame, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter the DataFrame based on specified conditions.
        """
        try:
            for column, condition in conditions.items():
                if column in data.columns:
                    if isinstance(condition, tuple) and len(condition) == 2:
                        data = data[(data[column] >= condition[0]) & (data[column] <= condition[1])]
                    else:
                        data = data[data[column] == condition]
            return data
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            raise DataProcessingException("Failed to filter data.")
    
    @staticmethod
    def aggregate_data(data: pd.DataFrame, group_by: List[str], aggregations: Dict[str, List[str]]) -> pd.DataFrame:
        """
        Aggregate the DataFrame based on specified groupings and aggregations.
        """
        try:
            agg_data = data.groupby(group_by).agg(aggregations)
            return agg_data
        except Exception as e:
            logger.error(f"Error aggregating data: {e}")
            raise DataProcessingException("Failed to aggregate data.")

# Utility functions for additional data processing tasks

def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str) -> pd.DataFrame:
    """
    Merge two DataFrames on a specified column.
    """
    try:
        merged_df = pd.merge(df1, df2, on=on)
        return merged_df
    except Exception as e:
        logger.error(f"Error merging dataframes: {e}")
        raise DataProcessingException("Failed to merge dataframes.")

def pivot_data(data: pd.DataFrame, index: List[str], columns: List[str], values: str) -> pd.DataFrame:
    """
    Pivot the DataFrame based on specified index, columns, and values.
    """
    try:
        pivot_df = data.pivot_table(index=index, columns=columns, values=values)
        return pivot_df
    except Exception as e:
        logger.error(f"Error pivoting data: {e}")
        raise DataProcessingException("Failed to pivot data.")