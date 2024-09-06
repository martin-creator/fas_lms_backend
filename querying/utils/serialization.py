# utils/serialization.py
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from django.db.models import Model
from typing import Any, Dict, List, Type

class SerializationError(Exception):
    """Custom exception for serialization errors."""
    pass

class DeserializationError(Exception):
    """Custom exception for deserialization errors."""
    pass

class SerializationService:
    """
    Service class for handling serialization and deserialization of Django models and other data.
    """

    @staticmethod
    def serialize_query_params(query_params: Dict[str, Any]) -> str:
        """
        Serialize query parameters into JSON format.

        Args:
        - query_params (dict): Dictionary containing query parameters.

        Returns:
        - str: JSON string representing the serialized query parameters.

        Raises:
        - SerializationError: If serialization fails.
        """
        try:
            return json.dumps(query_params, cls=DjangoJSONEncoder)
        except Exception as e:
            raise SerializationError(f"Failed to serialize query parameters: {str(e)}")

    @staticmethod
    def deserialize_query_result(result_data: str) -> Dict[str, Any]:
        """
        Deserialize query result data from JSON format.

        Args:
        - result_data (str): JSON string representing the serialized query result.

        Returns:
        - dict: Deserialized query result data.

        Raises:
        - DeserializationError: If deserialization fails.
        """
        try:
            return json.loads(result_data)
        except Exception as e:
            raise DeserializationError(f"Failed to deserialize query result data: {str(e)}")

    @staticmethod
    def serialize_object(instance: Model) -> str:
        """
        Serialize a Django model instance into JSON.

        Args:
        - instance: Django model instance.

        Returns:
        - str: JSON string representing the serialized object.

        Raises:
        - TypeError: If the instance is not a valid Django model instance.
        - SerializationError: If serialization fails.
        """
        try:
            if isinstance(instance, Model):
                data = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
                return json.dumps(data, cls=DjangoJSONEncoder)
            raise TypeError("Object is not a valid Django model instance.")
        except Exception as e:
            raise SerializationError(f"Failed to serialize object: {str(e)}")

    @staticmethod
    def deserialize_object(json_data: str, model_class: Type[Model]) -> Model:
        """
        Deserialize JSON data into a Django model object.

        Args:
        - json_data (str): JSON string representing the serialized object.
        - model_class: Django model class to deserialize into.

        Returns:
        - instance: Deserialized Django model instance.

        Raises:
        - DeserializationError: If deserialization fails.
        """
        try:
            data = json.loads(json_data)
            instance = model_class(**data)
            instance.full_clean()  # Validate the instance
            return instance
        except (ValidationError, TypeError, json.JSONDecodeError) as e:
            raise DeserializationError(f"Failed to deserialize object: {str(e)}")

    @staticmethod
    def batch_serialize_objects(instances: List[Model]) -> str:
        """
        Batch serialize a list of Django model instances into JSON.

        Args:
        - instances: List of Django model instances.

        Returns:
        - str: JSON string representing the serialized objects.

        Raises:
        - SerializationError: If serialization fails.
        """
        try:
            serialized_list = [SerializationService.serialize_object(instance) for instance in instances]
            return json.dumps(serialized_list, cls=DjangoJSONEncoder)
        except Exception as e:
            raise SerializationError(f"Failed to batch serialize objects: {str(e)}")

    @staticmethod
    def batch_deserialize_objects(json_data: str, model_class: Type[Model]) -> List[Model]:
        """
        Batch deserialize a JSON string into a list of Django model instances.

        Args:
        - json_data (str): JSON string representing the serialized objects.
        - model_class: Django model class to deserialize into.

        Returns:
        - list: List of deserialized Django model instances.

        Raises:
        - DeserializationError: If deserialization fails.
        """
        try:
            data_list = json.loads(json_data)
            instances = [SerializationService.deserialize_object(json.dumps(data), model_class) for data in data_list]
            return instances
        except Exception as e:
            raise DeserializationError(f"Failed to batch deserialize objects: {str(e)}")

    @staticmethod
    def serialize_to_json(data: Any) -> str:
        """
        Serialize any data to JSON format.

        Args:
        - data: Data to serialize.

        Returns:
        - str: JSON string.

        Raises:
        - SerializationError: If serialization fails.
        """
        try:
            return json.dumps(data, cls=DjangoJSONEncoder)
        except Exception as e:
            raise SerializationError(f"Failed to serialize data: {str(e)}")

    @staticmethod
    def deserialize_from_json(json_data: str) -> Any:
        """
        Deserialize any JSON string to Python data structure.

        Args:
        - json_data (str): JSON string.

        Returns:
        - Any: Deserialized data.

        Raises:
        - DeserializationError: If deserialization fails.
        """
        try:
            return json.loads(json_data)
        except Exception as e:
            raise DeserializationError(f"Failed to deserialize JSON data: {str(e)}")
