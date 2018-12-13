# hdt_file_connector.py
# Author: Thomas MINIER - MIT License 2017-2018
# Edit Capstone december 2018
from cassandra.cluster import Cluster
from database.db_connector import DatabaseConnector
import os.path
from cassandra.query import SimpleStatement


class CassandraConnector(DatabaseConnector):
    """A HDTFileConnector search for RDF triples in a HDT file"""

    def __init__(self, file):
        super(CassandraConnector, self).__init__()
        cluster = Cluster() # Si cluster : le définir ici
        # ex :
        # cluster = Cluster(
        #     ['172.16.134.144', '172.16.134.142', '172.16.134.143'],
        #     load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='dc1'))
        self._sessionCassandra =  cluster.connect()

    def search_triples(self, subject, predicate, obj, limit=0, offset=0):
        """
            Get an iterator over all RDF triples matching a triple pattern.

            Args:
                - subject ``string`` - Subject of the triple pattern
                - predicate ``string`` - Predicate of the triple pattern
                - object ``string`` - Object of the triple pattern
                - limit ``int=0`` ``optional`` -  LIMIT modifier, i.e., maximum number of RDF triples to read
                - offset ``int=0`` ``optional`` -  OFFSET modifier, i.e., number of RDF triples to skip

            Returns:
                A Python iterator over RDF triples matching the given triples pattern
        """
        subject = subject if (subject is not None) and (not subject.startswith('?')) else ""
        predicate = predicate if (predicate is not None) and (not predicate.startswith('?')) else ""
        obj = obj if (obj is not None) and (not obj.startswith('?')) else ""
        #Ici il faut connecter à Cassandra et retourner l'itérateur
        #return self._hdt.search_triples(subject, predicate, obj, offset=offset, limit=limit)
        query =  "SELECT * FROM records "
        statement = SimpleStatement(query, fetch_size=10) #Penser à ajouter Cassandra, etc. pour python dans la liste des requirments
        res=session.execute_async(statement)
        return res.result()

    @property
    def nb_triples(self):
        #return self._hdt.total_triples
        return 0
    @property
    def nb_subjects(self):
        """Get the number of subjects in the database"""
        # return self._hdt.nb_subjects
        return 0

    @property
    def nb_predicates(self):
        """Get the number of predicates in the database"""
        # return self._hdt.nb_predicates
        return 0

    @property
    def nb_objects(self):
        """Get the number of objects in the database"""
        # return self._hdt.nb_objects
        return 0

    def from_config(config):
        """Build a HDTFileFactory from a config file"""
        if not os.path.isfile(config["file"]):
            raise Exception("Configuration file not found: {}".format(config["file"]))
        return HDTFileConnector(config["file"])
