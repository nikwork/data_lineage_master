import unittest
from neo4j import GraphDatabase, unit_of_work
from data_linage_object_factory import DataLinageObjectFactory
from BusinessProcess import BisnessProcess
from data_element import ElementAbstractionLevel as AbstractionLevel
import yaml
# import pandas as pd
import dataclasses

# Note compare test methods name
unittest.TestLoader.sortTestMethodsUsing = None

# Path to excel file with test data (processes, sources, destination objects)
_TST_DATA_PATH = "./Data/tst_proc_desc.xlsx"

# Create Neo4j driver
_DRIVER = GraphDatabase.driver(
    "neo4j://localhost:7687",
    auth=("neo4j", "s3cr3t"),
    max_connection_lifetime=1000
    )


class TestObjects(unittest.TestCase):

    # TODO: Move all work with neo4j to special object (class)

    def setUpModule():
        print('setUpModule')

    ################################################################################################################
    # Help methods
    ################################################################################################################

    @staticmethod
    @unit_of_work(timeout=5)
    def create_person(tx, name):
        return tx.run(
                        "CREATE (a:Test {name: $name}) RETURN id(a)",
                        name=name
                    ).single().value()

    @staticmethod
    @unit_of_work(timeout=5)
    def create_process(tx, properties):

        # Convert data types

        if properties.get("data_linage_object_type") is not None:
            properties["data_linage_object_type"] = \
                int(properties["data_linage_object_type"])

        if properties.get("tags") is not None:
            properties["tags"] = list(properties["tags"])

        if properties.get("relations") is not None:
            properties["relations"] = list(properties["relations"])

        if properties.get("id") is not None:
            properties["id"] = str(properties["id"])

        # Insert row
        return tx.run(query="CREATE (a:Process) SET a = $dict_param  RETURN id(a)", dict_param=properties) \
            .single().value()

    ################################################################################################################
    # Tests
    ################################################################################################################

    def test_data_linage_object(self):
        """
        Test simple data linage object factory
        """

        test_data_linage_object = \
            DataLinageObjectFactory.data_linage_object_factory(
                                                    name='test_object',
                                                    description='test object'
                                                    )
        id_len = len(str(test_data_linage_object.id))
        self.assertTrue(
            id_len == 36,
            f"data_linage_object_factory: object id len is not 36 ({id_len})"
        )

    def test_data_element_object(self):
        """
        Test data element factory
        """

        # DataLinageObjectFactory.data_element_factory()
        data_element = DataLinageObjectFactory.data_element_factory(
                            name="test_object",
                            system_name="test_system",
                            storage_name="test_storage",
                            description=None,
                            ext_storage_sync=False,
                            tags=set,
                            relations=set,
                            abstraction_level=int(AbstractionLevel.NOT_DEFINED)
                        )

        self.assertTrue(data_element.full_name == "test_system.test_storage.test_object",
                        "Error in full name calculation")
        self.assertTrue(data_element.abstraction_level == 0, "Not correct abstraction level")

    def test_neo4j_connection(self):
        """
        Test neo4j connection
        """

        neo4j_config: dict

        with open("../config.yml", 'r') as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            neo4j_config = list(
                filter(lambda storage: "neo4j" in storage, data["external_storage"])
            )[0]["neo4j"]

        # Create session
        with _DRIVER.session() as session:
            # create test node
            node_id = -1
            node_id = session.write_transaction(TestObjects.create_person, "Test")

            # check node id
            self.assertTrue(node_id > -1, "Create test node error")

            # remove test node
            res = session.run("MATCH (n {name:\"Test\"}) DELETE n")

    def test_create_process_from_file(self):
        """
        TODO: this test starts after test_create_business_processes_from_file. Have to find why and create correct test loge
        Create processes in neo4f directly (without BusinessProject data class)
        """

        # Test data location
        tst_data_path = _TST_DATA_PATH

        # Dict with process properties
        dict_proc = {}

        # Result list of node's
        node_id_list = []

        # Load test data
        with (open(tst_data_path, 'rb')) as excel_file:
            df_proc = pd.read_excel(excel_file, sheet_name="process")
            dict_proc = df_proc.to_dict(orient='records')

        # Create session
        with _DRIVER.session() as session:
            # Delete test processes before test
            session.run("MATCH (a:Process) WHERE a.is_test_object=True DELETE a")

            # Load each row
            for row in dict_proc:
                row["process_natural_key"] = "_".join([str(row["process_group_id"]), str(row["process_group_id"])])
                row["is_test_object"] = True
                node_id = session.write_transaction(TestObjects.create_process, row)
                node_id_list.append(node_id)

            # Delete test processes after test
            session.run("MATCH (a:Process) WHERE a.is_test_object=True DELETE a")

        # Check
        self.assertEqual(
                        self,
                        len(dict_proc),
                        len(node_id_list),
                        "Not all processes in file moved in Neo4j"
                        )

    def test_create_business_processes_from_file(self):
        """
        Test creation BusinessProcess objects from file and load to neo4j
        """

        # Test data location
        tst_data_path = _TST_DATA_PATH

        # Dict with process properties
        dict_proc = {}

        # Result list of node's
        node_id_list = []

        # Result list of BusinessProcess
        business_processes = []

        # Load test data
        with (open(tst_data_path, 'rb')) as excel_file:
            df_proc = pd.read_excel(excel_file, sheet_name="process")
            dict_proc = df_proc.to_dict(orient='records')

        #
        for row in dict_proc:

            # Create DusinessProcess object(Unpack process properties from dict
            business_process = BisnessProcess(
                **row
                )
            print(business_process)
            business_processes.append(dataclasses.asdict(business_process))
        print(business_processes)
        # Create session
        with _DRIVER.session() as session:
            # Delete test processes before test ()
            session.run(
                "MATCH (a:Process) \
                WHERE a.is_test_object=True DELETE a"
                )

            # Load each row
            for row in business_processes:
                row["is_test_object"] = True
                node_id = session.write_transaction(
                    TestObjects.create_process,
                    row
                    )
                node_id_list.append(node_id)

            # Delete test processes after test
            # session.run("MATCH (a:Process)
            # WHERE a.is_test_object=True DELETE a")

        # Check
        self.assertEqual(
                            self,
                            len(dict_proc),
                            len(node_id_list),
                            "Not all processes in file moved in Neo4j"
                        )


if __name__ == "Tests":
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestObjects))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testSuite)
