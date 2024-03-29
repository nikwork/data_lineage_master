from neo4j import unit_of_work
import pandas as pd



# Help functions for tests
class TestHelper:

    # Help methods
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

        if properties.get("data_lineage_object_type") is not None:
            properties["data_lineage_object_type"] = \
                int(properties["data_lineage_object_type"])

        if properties.get("tags") is not None:
            properties["tags"] = list(properties["tags"])

        if properties.get("relations") is not None:
            properties["relations"] = list(properties["relations"])

        if properties.get("id") is not None:
            properties["id"] = str(properties["id"])

        # Insert row
        return tx.run(
                query="CREATE (a:Process) SET a = $dict_param  RETURN id(a)",
                dict_param=properties
            ) \
            .single().value()

    @staticmethod
    def load_proc_list_from_file(tst_data_path: str) -> list:
        """Load processes from file and return dict

        Args:
            tst_data_path (str): path to file

        Returns:
            processes_list: list of processes
        """

        # Dict with process properties
        processes_list = list

        # Load test data
        with (open(tst_data_path, 'rb')) as excel_file:
            df_proc = pd.read_excel(excel_file, sheet_name="process")
            processes_list = df_proc.to_dict(orient='records')

        return processes_list

    # @staticmethod
    # def decompose_data_object()
