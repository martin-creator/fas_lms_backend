from datetime import datetime

class DateTimeUtils:

    @staticmethod
    def parse_datetime(datetime_str):
        """
        Parse a datetime string into a datetime object.
        
        Args:
            datetime_str (str): The datetime string.
            
        Returns:
            datetime: The parsed datetime object.
        """
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def format_datetime(datetime_obj):
        """
        Format a datetime object into a string.
        
        Args:
            datetime_obj (datetime): The datetime object.
            
        Returns:
            str: The formatted datetime string.
        """
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')