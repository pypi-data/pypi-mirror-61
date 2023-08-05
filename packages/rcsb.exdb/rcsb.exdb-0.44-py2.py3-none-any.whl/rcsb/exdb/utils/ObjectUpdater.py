##
# File: ObjectUpdater.py
# Date: 9-Oct-2019  jdw
#
# Utilities to update document features from the document object server.
#
# Updates:
#
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging

from rcsb.db.mongo.Connection import Connection
from rcsb.db.mongo.MongoDbUtil import MongoDbUtil


logger = logging.getLogger(__name__)


class ObjectUpdater(object):
    """ Utilities to update document features from the document object server.

    """

    def __init__(self, cfgOb, **kwargs):
        self.__cfgOb = cfgOb
        self.__resourceName = "MONGO_DB"
        _ = kwargs
        #

    def update(self, databaseName, collectionName, updateDL):
        """Update documents satisfying the selection details with the content of updateObjD.

        Args:
            databaseName (str): Target database name
            collectionName (str): Target collection name
            updateDL = [{selectD: ..., updateD: ... }, ....]
                selectD    = {'ky1': 'val1', 'ky2': 'val2',  ...}
                updateD = {'key1.subkey1...': 'val1', 'key2.subkey2..': 'val2', ...}

        """
        try:
            numUpdated = 0
            with Connection(cfgOb=self.__cfgOb, resourceName=self.__resourceName) as client:
                mg = MongoDbUtil(client)
                if mg.collectionExists(databaseName, collectionName):
                    logger.info("%s %s document count is %d", databaseName, collectionName, mg.count(databaseName, collectionName))
                    for updateD in updateDL:
                        num = mg.update(databaseName, collectionName, updateD["updateD"], updateD["selectD"])
                        numUpdated += num

        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return numUpdated
        #
