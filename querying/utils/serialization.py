# utils/serialization.py
import json
from django.core.serializers.json import DjangoJSONEncoder

def serialize_query_params(query_params):
    """
    Serialize query parameters into JSON format.

    Args:
    - query_params (dict): Dictionary containing query parameters.

    Returns:
    - str: JSON string representing the serialized query parameters.

    Raises:
    - ValueError: If serialization fails.
    """
    try:
        return json.dumps(query_params, cls=DjangoJSONEncoder)
    except Exception as e:
        raise ValueError(f"Failed to serialize query parameters: {str(e)}")

def deserialize_query_result(result_data):
    """
    Deserialize query result data from JSON format.

    Args:
    - result_data (str): JSON string representing the serialized query result.

    Returns:
    - dict: Deserialized query result data.

    Raises:
    - ValueError: If deserialization fails.
    """
    try:
        return json.loads(result_data)
    except Exception as e:
        raise ValueError(f"Failed to deserialize query result data: {str(e)}")

def serialize_object(instance):
    """
    Serialize a Django model instance into JSON.

    Args:
    - instance: Django model instance.

    Returns:
    - str: JSON string representing the serialized object.

    Raises:
    - TypeError: If the instance is not a valid Django model instance.
    - ValueError: If serialization fails.
    """
    try:
        if hasattr(instance, '__dict__'):
            return json.dumps(instance.__dict__, cls=DjangoJSONEncoder)
        raise TypeError("Object is not a valid Django model instance.")
    except Exception as e:
        raise ValueError(f"Failed to serialize object: {str(e)}")

def deserialize_object(json_data, model_class):
    """
    Deserialize JSON data into a Django model object.

    Args:
    - json_data (str): JSON string representing the serialized object.
    - model_class: Django model class to deserialize into.

    Returns:
    - instance: Deserialized Django model instance.

    Raises:
    - ValueError: If deserialization fails.
    """
    try:
        data = json.loads(json_data)
        instance = model_class(**data)
        instance.full_clean()
        return instance
    except Exception as e:
        raise ValueError(f"Failed to deserialize object: {str(e)}")
