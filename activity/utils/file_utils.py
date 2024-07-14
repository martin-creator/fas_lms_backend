class FileUtils:

    @staticmethod
    def validate_file(file):
        """
        Validate the uploaded file.
        
        Args:
            file (File): The uploaded file.
            
        Returns:
            bool: True if the file is valid, False otherwise.
        """
        # Implement the logic to validate the file
        return True  # Example return
    
    @staticmethod
    def get_file_extension(file):
        """
        Get the file extension.
        
        Args:
            file (File): The uploaded file.
            
        Returns:
            str: The file extension.
        """
        return file.name.split('.')[-1].lower()
