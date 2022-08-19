from neo4j import unit_of_work


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
        return tx.run(
                query="CREATE (a:Process) SET a = $dict_param  RETURN id(a)",
                dict_param=properties
            ) \
            .single().value()
