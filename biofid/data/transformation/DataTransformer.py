from typing import Any, Type

from biofid.data.transformation.interfaces import DataTransformation


def transform(data: Any, transformation: Type[DataTransformation], **kwargs) -> Any:
    """ Takes the given data and returns the outpu of the given transformation.
        Any kwargs will be passed to the instantiated transformation object.
    """
    transformation_instance = transformation(**kwargs)
    return transformation_instance.transform(data)
