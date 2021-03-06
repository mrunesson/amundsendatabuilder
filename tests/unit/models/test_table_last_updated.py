import unittest

from databuilder.models.neo4j_csv_serde import NODE_KEY, \
    NODE_LABEL, RELATION_START_KEY, RELATION_START_LABEL, RELATION_END_KEY, \
    RELATION_END_LABEL, RELATION_TYPE, RELATION_REVERSE_TYPE
from databuilder.models.table_last_updated import TableLastUpdated


class TestTableLastUpdated(unittest.TestCase):

    def setUp(self):
        # type: () -> None
        super(TestTableLastUpdated, self).setUp()

        self.tableLastUpdated = TableLastUpdated(table_name='test_table',
                                                 last_updated_time_epoch=25195665,
                                                 schema_name='default')

        self.expected_node_result = {
            NODE_KEY: 'hive://gold.default/test_table/timestamp',
            NODE_LABEL: 'Timestamp',
            'last_updated_timestamp': 25195665,
            'name': 'last_updated_timestamp'
        }

        self.expected_relation_result = {
            RELATION_START_KEY: 'hive://gold.default/test_table',
            RELATION_START_LABEL: 'Table',
            RELATION_END_KEY: 'hive://gold.default/test_table/timestamp',
            RELATION_END_LABEL: 'Timestamp',
            RELATION_TYPE: 'LAST_UPDATED_AT',
            RELATION_REVERSE_TYPE: 'LAST_UPDATED_TIME_OF'
        }

    def test_create_next_node(self):
        # type: () -> None
        next_node = self.tableLastUpdated.create_next_node()
        self.assertEquals(next_node, self.expected_node_result)

    def test_create_next_relation(self):
        # type: () -> None
        next_relation = self.tableLastUpdated.create_next_relation()
        self.assertEquals(next_relation, self.expected_relation_result)

    def test_get_table_model_key(self):
        # type: () -> None
        table = self.tableLastUpdated.get_table_model_key()
        self.assertEquals(table, 'hive://gold.default/test_table')

    def test_get_last_updated_model_key(self):
        # type: () -> None
        last_updated = self.tableLastUpdated.get_last_updated_model_key()
        self.assertEquals(last_updated, 'hive://gold.default/test_table/timestamp')

    def test_create_nodes(self):
        # type: () -> None
        nodes = self.tableLastUpdated.create_nodes()
        self.assertEquals(len(nodes), 1)
        self.assertEquals(nodes[0], self.expected_node_result)

    def test_create_relation(self):
        # type: () -> None
        relation = self.tableLastUpdated.create_relation()
        self.assertEquals(len(relation), 1)
        self.assertEquals(relation[0], self.expected_relation_result)
