from google.cloud.firestore import Client, SERVER_TIMESTAMP
from firestore.db import Property
from firestore.query import Query
import os


def __get_client__():
    # There must be a better way to do this, right?
    import builtins
    if not hasattr(builtins, "__firestore_client__"):
        setattr(builtins, "__firestore_client__", Client())
    return builtins.__firestore_client__


class Entity(object):
    """Creates a firestore document under the collection [YourEntity]

    Args:
        **data (kwargs): Values for properties in the new record, e.g User(name="Bob")

    Attributes:
        id (str or int): Unique id identifying this record,
            if auto-generated, this is not available before `put()`
    """

    def __init__(self, **data):
        if type(self) is Entity:
            raise Exception("You must extend Entity")
        self.__model_name = type(self).__name__
        client = __get_client__()
        self.__collection = client.collection(self.__collection_name__())
        self.id = None
        self.__firestore_data__ = {}
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def __collection_name__(cls):
        prefix = os.environ.get('TEST_PREFIX', '')
        return "%s%s" % (prefix, cls.__name__)

    def __document__(self):
        if not self.id:
            return None
        # Get's the absolute path: `projects/{project_id}/databases/{database_id}/documents/{document_path}
        return self.__collection.document(self.id)

    def __str__(self):
        if self.id:
            return "<%s id='%s'>" % (self.__model_name, self.id)
        return "<Entity %s>" % self.__model_name

    def put(self):
        """
        Save the models data to Firestore

        Raises:
            InvalidValueError: Raised if the value of a property is invalid, e.g. A required property that's None
        """
        props = self.__get_properties__()
        for key in props:
            if key not in self.__firestore_data__:
                # Value not set yet. Try to set to none
                setattr(self, key, None)

        if self.id:
            self.__collection.document(self.id).set(self.__firestore_data__)
        else:
            _time, new_ref = self.__collection.add(self.__firestore_data__)
            self.id = new_ref.id
        # Set the data to the most recent data on db. Updates server set values e.g. SERVER_TIMESTAMP
        self.__firestore_data__ = self.__document__().get().to_dict()

    def delete(self):
        """Delete the document connected to this model from firestore"""
        if self.id:
            self.__collection.document(self.id).delete()

    def __get_properties__(self):
        props = []
        for key, value in self.__class__.__dict__.items():
            try:
                if issubclass(value.__class__, Property):
                    props.append(key)
            except TypeError:
                pass
        return props

    def __set_database_values__(self, document: dict):
        self.__firestore_data__ = document

    @classmethod
    def get(cls, _id):
        """
        Get a model with the given id

        Args:
            _id (str or int): A key or id of the model record, when a list is provided, `get` returns a list
                models

        Returns:
            Entity: An instance of the firestore entity calling get
            None: If the id provided doesn't exist
        """
        document = __get_client__().collection(cls.__collection_name__()).document(_id)
        doc = document.get()
        if not doc.exists:
            return None
        entity = cls(id=_id)
        entity.__firestore_data__ = doc.to_dict()
        return entity

    @classmethod
    def query(cls, offset=0, limit=0):
        """
        Create a query to this model

        Args:
            offset (int): The position in the database where the results begin
            limit (int): Maximum number of records to return

        Returns:
            An iterable query object
        """
        return Query(cls, offset, limit)
