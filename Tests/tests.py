import sys
# TODO: Fix fileflake8(E402).
sys.path.append("/Users/nikolayvlasov/PythonProjects/data_lineage_master")
import os
import unittest
from neo4j import GraphDatabase, unit_of_work
from data_lineage_object_factory import DataLineageObjectFactory
from data_lineage_object import DataLineageObjectUtils
from business_process import BisnessProcess
from test_helper import TestHelper
from data_element import ElementAbstractionLevel as AbstractionLevel
from dotenv import load_dotenv
import dataclasses
import pandas as pd

print(__name__)

# Load .env
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '../config/.env.dev'))

print(f"BASEDIR:\n{BASEDIR}")

# STR postfix shows that variable is instance of sring
# INT postfix shows that variable is instance of integer
NEO4J_HOST_STR = os.getenv('NEO4J_HOST')
NEO4J_PORT_STR = os.getenv('NEO4J_PORT', '7687')
NEO4J_USER_STR = os.getenv('NEO4J_USER')
NEO4J_PWD_STR = os.getenv('NEO4J_PWD')
NEO4J_MAX_CONNECTION_LIFETIME_INT = int(os.getenv(
                                            'NEO4J_MAX_CONNECTION_LIFETIME',
                                            '1000'
                                            )
                                        )
NEO4J_URI = f"neo4j://{NEO4J_HOST_STR}:{NEO4J_PORT_STR}"

# Path to excel file with test data (processes, sources, destination objects)

TEST_DATA_PATH = os.getenv('TEST_DATA_PATH')

# Not compare test methods name

unittest.TestLoader.sortTestMethodsUsing = None

# Create Neo4j driver

NEO4J_DRIVER = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER_STR, NEO4J_PWD_STR),
    # max_connection_lifetime=NEO4J_MAX_CONNECTION_LIFETIME_INT
    )


class TestObjects(unittest.TestCase):

    # Start tests

    def test_path_to_test_data(self):
        """
        Check test data existence
        """
        self.assertTrue(os.path.exists(TEST_DATA_PATH))

    def test_data_lineage_object(self):
        """
        Test simple data Lineage object factory
        """

        test_data_lineage_object = \
            DataLineageObjectFactory.data_lineage_object_factory(
                                                    name='test_object',
                                                    description='test object'
                                                    )
        id_len = len(str(test_data_lineage_object.id))

        self.assertTrue(
            id_len == 36,
            f"data_lineage_object_factory: object id len is not 36 ({id_len})"
        )

    def test_data_element_object(self):
        """
        Test data element factory
        """

        # DataLineageObjectFactory.data_element_factory()
        data_element = DataLineageObjectFactory.data_element_factory(
                            name="test_object",
                            system_name="test_system",
                            storage_name="test_storage",
                            description=None,
                            ext_storage_sync=False,
                            tags=set,
                            relations=set,
                            abstraction_level=int(AbstractionLevel.NOT_DEFINED)
                        )

        self.assertTrue(
            data_element.full_name == "test_system.test_storage.test_object",
            "Error in full name calculation"
            )

        self.assertTrue(
            data_element.abstraction_level == 0,
            "Not correct abstraction level"
            )

    def test_neo4j_connection(self):
        """
        Test neo4j connection
        """

        neo4j_config: dict

        # Create session
        with NEO4J_DRIVER.session() as session:
            # create test node
            node_id = -1
            node_id = session.write_transaction(
                    TestHelper.create_person,
                    "Test"
                )

            # check node id
            self.assertTrue(node_id > -1, "Create test node error")

            # remove test node
            session.run("MATCH (n {name:\"Test\"}) DELETE n")

    def test_create_business_processes_from_file(self):
        """
        Test creation BusinessProcess objects from file and load to neo4j
        """

        # Result list of BusinessProcess
        business_processes = []

        # Result list of node's
        node_id_list = []

        dict_proc = TestHelper.load_proc_list_from_file(TEST_DATA_PATH)

        #
        for row in dict_proc:

            # Create DusinessProcess object(Unpack process properties from dict
            business_process = BisnessProcess(
                **row
                )
            print(business_process)
            business_processes.append(dataclasses.asdict(business_process))

        # Create session
        with NEO4J_DRIVER.session() as session:
            # Delete test processes before test ()
            session.run(
                "MATCH (a:Process) \
                WHERE a.is_test_object=True DELETE a"
                )

            # Load each row
            for row in business_processes:
                # row["is_test_object"] = True
                node_id = session.write_transaction(
                    TestHelper.create_process,
                    row
                    )
                node_id_list.append(node_id)

            # Delete test processes after test
            # session.run("MATCH (a:Process)
            # WHERE a.is_test_object=True DELETE a")

        # Check
        self.assertEqual(
                            # self,
                            len(dict_proc),
                            len(node_id_list),
                            "Not all processes in file moved in Neo4j"
                        )

    def test_decompose_data_object(self):
        do_utils = DataLineageObjectUtils()
        test_data_lineage_object = \
            DataLineageObjectFactory.data_lineage_object_factory(
                                                    name='test_object',
                                                    description='test object'
                                                    )

        decomposed_dic = do_utils.decompose_data_object(
                                                    test_data_lineage_object
                                                    )

        if decomposed_dic['dlo_node'] and decomposed_dic['dlo_attribute_nodes']:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ in ("Tests"):

    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestObjects))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testSuite)
