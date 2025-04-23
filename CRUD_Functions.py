from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):

        # Connection Variables
        USER = username
        PASS = password
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 34430
        DB = 'AAC'
        COL = 'animals'

        # Initialize Connection
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    def create(self, data):
        """
        Insert a document into the MongoDB collection.

        Args:
            data (dict): A dictionary containing key/value pairs that make up the document.

        Returns:
            bool: True if the document was successfully inserted, otherwise False.
        """

        # Checks if data is a dictionary data type and not empty
        if not isinstance(data, dict) or not data:
            return False

        try:
            result = self.collection.insert_one(data)
            # Check if a valid inserted_id was returned.
            return bool(result.inserted_id)
        except Exception:
            # If an error occurs, will return False.
            return False

    def read(self, query):
        """
        Query for documents from the MongoDB collection using the find() method.

        Args:
            query (dict): A dictionary containing key/value pairs for the lookup.

        Returns:
            list: A list of documents matching the query if successful, otherwise an empty list.
        """

        # Checks if query is a dictionary data type
        if not isinstance(query, dict):
            return []

        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception:
            # If an error occurs, return an empty list.
            return []

    def update(self, query, update_values):
        """
        Update documents in the MongoDB collection.

        Args:
            query (dict): A dictionary containing key/value pairs for the lookup to locate documents.
            update_values (dict): A dictionary containing key/value pairs with the fields to update.

        Returns:
            int: The number of documents that were updated. Returns 0 if no documents were updated or on error.
        """
        # Validate input types and non-empty dictionaries
        if not isinstance(query, dict) or not query:
            return 0
        if not isinstance(update_values, dict) or not update_values:
            return 0

        try:
            # Use update_many to update all matching documents using the "$set" operator
            result = self.collection.update_many(query, {"$set": update_values})
            # Return the number of modified documents
            return result.modified_count
        except Exception:
            return 0

    def delete(self, query):
        """
        Delete documents from the MongoDB collection.

        Args:
            query (dict): A dictionary containing key/value pairs for the lookup to locate documents.

        Returns:
            int: The number of documents that were deleted. Returns 0 if no documents were deleted or on error.
        """
        # Validate that the query is a non-empty dictionary
        if not isinstance(query, dict) or not query:
            return 0

        try:
            result = self.collection.delete_many(query)
            # Return the number of deleted documents
            return result.deleted_count
        except Exception:
            return 0
