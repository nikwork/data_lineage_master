from data_linage_object import DataLinageObject
from data_element import (
                            DataElement,
                            ElementAbstractionLevel as AbstractionLevel
                        )


class DataLinageObjectFactory:
    """Factory methods for correct DataLinageObject creation."""

    @staticmethod
    # Factory method for correct DataLinageObject creation.
    def data_linage_object_factory(
                                    name,
                                    description=None,
                                    ext_storage_sync=False,
                                    tags=set,
                                    relations=set
                                ):
        """Data linage object factory function

        :param description:
        :param name:
        :param relations:
        :param tags:
        :type ext_storage_sync:
        """
        # current_timestamp = datetime.datetime.utcnow()

        return DataLinageObject(
                                name=name,
                                description=description,
                                ext_storage_sync=ext_storage_sync,
                                tags=tags,
                                relations=relations,
                                # create_timestamp=current_timestamp,
                                # last_modified_timestamp=current_timestamp,
                                actual_flg=True
                            )

    @staticmethod
    def data_element_factory(name, system_name, storage_name,
                             description=None, ext_storage_sync=False,
                             tags=set, relations=set,
                             abstraction_level=AbstractionLevel.NOT_DEFINED):

        data_element = DataElement(
                                    name=name,
                                    system_name=system_name,
                                    storage_name=storage_name,
                                    abstraction_level=abstraction_level,
                                    description=description,
                                    ext_storage_sync=ext_storage_sync,
                                    tags=tags,
                                    relations=relations,
                                    actual_flg=True
                                   )

        return data_element
