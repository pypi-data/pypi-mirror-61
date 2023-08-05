# -*- coding: utf-8 -*-

import json
import unittest
import elasticsearch
from elasticsearch.exceptions import NotFoundError

from elasticmock import elasticmock
from elasticmock.fake_elasticsearch import FakeElasticsearch


class TestFakeElasticsearch(unittest.TestCase):
    @elasticmock
    def setUp(self):
        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.index_name = 'test_index'
        self.doc_type = 'doc-Type'
        self.body = {'string': 'content', 'id': 1}
        self.updated_body = {'string': 'content-updated', 'id': 1}

    def test_should_create_fake_elasticsearch_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    def test_should_index_document(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)

        self.assertEqual(self.doc_type, data.get('_type'))
        self.assertTrue(data.get('created'))
        self.assertEqual(1, data.get('_version'))
        self.assertEqual(self.index_name, data.get('_index'))

    def test_should_bulk_index_documents(self):
        action = {'index': {'_index': self.index_name, '_type': self.doc_type}}
        action_json = json.dumps(action)
        body_json = json.dumps(self.body)
        num_of_documents = 10

        lines = []
        for count in range(0, num_of_documents):
            lines.append(action_json)
            lines.append(body_json)
        body = '\n'.join(lines)

        data = self.es.bulk(body=body)
        items = data.get('items')

        self.assertFalse(data.get('errors'))
        self.assertEqual(num_of_documents, len(items))

        for item in items:
            index = item.get('index')

            self.assertEqual(self.doc_type, index.get('_type'))
            self.assertEqual(self.index_name, index.get('_index'))
            self.assertEqual('created', index.get('result'))
            self.assertEqual(201, index.get('status'))

    def test_should_index_document_without_doc_type(self):
        data = self.es.index(index=self.index_name, body=self.body)

        self.assertEqual('_doc', data.get('_type'))
        self.assertTrue(data.get('created'))
        self.assertEqual(1, data.get('_version'))
        self.assertEqual(self.index_name, data.get('_index'))

    def test_should_raise_notfounderror_when_nonindexed_id_is_used(self):
        with self.assertRaises(NotFoundError):
            self.es.get(index=self.index_name, id='1')

    def test_should_get_document_with_id(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)

        document_id = data.get('_id')
        target_doc = self.es.get(index=self.index_name, id=document_id)

        expected = {
            '_type': self.doc_type,
            '_source': self.body,
            '_index': self.index_name,
            '_version': 1,
            'found': True,
            '_id': document_id
        }

        self.assertDictEqual(expected, target_doc)

    def test_should_get_document_with_id_and_doc_type(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)

        document_id = data.get('_id')
        target_doc = self.es.get(index=self.index_name, id=document_id, doc_type=self.doc_type)

        expected = {
            '_type': self.doc_type,
            '_source': self.body,
            '_index': self.index_name,
            '_version': 1,
            'found': True,
            '_id': document_id
        }

        self.assertDictEqual(expected, target_doc)

    def test_should_return_exists_false_if_nonindexed_id_is_used(self):
        self.assertFalse(self.es.exists(index=self.index_name, doc_type=self.doc_type, id=1))

    def test_should_return_exists_true_if_indexed_id_is_used(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)
        document_id = data.get('_id')
        self.assertTrue(self.es.exists(index=self.index_name, doc_type=self.doc_type, id=document_id))

    def test_should_return_true_when_ping(self):
        self.assertTrue(self.es.ping())

    def test_should_return_status_200_for_info(self):
        info = self.es.info()
        self.assertEqual(info.get('status'), 200)

    def test_should_get_only_document_source_with_id(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)

        document_id = data.get('_id')
        target_doc_source = self.es.get_source(index=self.index_name, doc_type=self.doc_type, id=document_id)

        self.assertEqual(target_doc_source, self.body)

    def test_should_raise_notfounderror_when_search_for_unexistent_index(self):
        with self.assertRaises(NotFoundError):
            self.es.search(index=self.index_name)

    def test_should_return_count_for_indexed_documents_on_index(self):
        index_quantity = 0
        for i in range(0, index_quantity):
            self.es.index(index='index_{0}'.format(i), doc_type=self.doc_type, body={'data': 'test_{0}'.format(i)})

        count = self.es.count()
        self.assertEqual(index_quantity, count.get('count'))

    def test_should_return_hits_hits_even_when_no_result(self):
        search = self.es.search()
        self.assertEqual(0, search.get('hits').get('total'))
        self.assertListEqual([], search.get('hits').get('hits'))

    def test_should_return_all_documents(self):
        index_quantity = 10
        for i in range(0, index_quantity):
            self.es.index(index='index_{0}'.format(i), doc_type=self.doc_type, body={'data': 'test_{0}'.format(i)})

        search = self.es.search()
        self.assertEqual(index_quantity, search.get('hits').get('total'))

    def test_should_return_only_indexed_documents_on_index(self):
        index_quantity = 2
        for i in range(0, index_quantity):
            self.es.index(index=self.index_name, doc_type=self.doc_type, body={'data': 'test_{0}'.format(i)})

        search = self.es.search(index=self.index_name)
        self.assertEqual(index_quantity, search.get('hits').get('total'))

    def test_should_return_only_indexed_documents_on_index_with_doc_type(self):
        index_quantity = 2
        for i in range(0, index_quantity):
            self.es.index(index=self.index_name, doc_type=self.doc_type, body={'data': 'test_{0}'.format(i)})
        self.es.index(index=self.index_name, doc_type='another-Doctype', body={'data': 'test'})

        search = self.es.search(index=self.index_name, doc_type=self.doc_type)
        self.assertEqual(index_quantity, search.get('hits').get('total'))

    def test_should_raise_exception_when_delete_nonindexed_document(self):
        with self.assertRaises(NotFoundError):
            self.es.delete(index=self.index_name, doc_type=self.doc_type, id=1)

    def test_should_delete_indexed_document(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)
        document_id = data.get('_id')
        search = self.es.search(index=self.index_name)
        self.assertEqual(1, search.get('hits').get('total'))
        delete_data = self.es.delete(index=self.index_name, doc_type=self.doc_type, id=document_id)
        search = self.es.search(index=self.index_name)
        self.assertEqual(0, search.get('hits').get('total'))
        self.assertDictEqual({
            'found': True,
            '_index': self.index_name,
            '_type': self.doc_type,
            '_id': document_id,
            '_version': 1,
        }, delete_data)

    @elasticmock
    def test_should_return_same_elastic_instance_when_instantiate_more_than_one_instance_with_same_host(self):
        es1 = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        es2 = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.assertEqual(es1, es2)

    @elasticmock
    def test_should_raise_notfounderror_when_nonindexed_id_is_used_for_suggest(self):
        with self.assertRaises(NotFoundError):
            self.es.suggest(body={}, index=self.index_name)

    @elasticmock
    def test_should_return_suggestions(self):
        self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)
        suggestion_body = {
            'suggestion-string': {
                'text': 'test_text',
                'term': {
                    'field': 'string'
                }
            },
            'suggestion-id': {
                'text': 1234567,
                'term': {
                    'field': 'id'
                }
            }
        }
        suggestion = self.es.suggest(body=suggestion_body, index=self.index_name)
        self.assertIsNotNone(suggestion)
        self.assertDictEqual({
            'suggestion-string': [
                {
                    'text': 'test_text',
                    'length': 1,
                    'options': [
                        {
                            'text': 'test_text_suggestion',
                            'freq': 1,
                            'score': 1.0
                        }
                    ],
                    'offset': 0
                }
            ],
            'suggestion-id': [
                {
                    'text': 1234567,
                    'length': 1,
                    'options': [
                        {
                            'text': 1234568,
                            'freq': 1,
                            'score': 1.0
                        }
                    ],
                    'offset': 0
                }
            ],
        }, suggestion)

    def test_should_search_in_multiple_indexes(self):
        self.es.index(index='groups', doc_type='groups', body={'budget': 1000})
        self.es.index(index='users', doc_type='users', body={'name': 'toto'})
        self.es.index(index='pcs', doc_type='pcs', body={'model': 'macbook'})

        result = self.es.search(index=['users', 'pcs'])
        self.assertEqual(2, result.get('hits').get('total'))

    def test_should_count_in_multiple_indexes(self):
        self.es.index(index='groups', doc_type='groups', body={'budget': 1000})
        self.es.index(index='users', doc_type='users', body={'name': 'toto'})
        self.es.index(index='pcs', doc_type='pcs', body={'model': 'macbook'})

        result = self.es.count(index=['users', 'pcs'])
        self.assertEqual(2, result.get('count'))

    def test_doc_type_can_be_list(self):
        doc_types = ['1_idx', '2_idx', '3_idx']
        count_per_doc_type = 3

        for doc_type in doc_types:
            for _ in range(count_per_doc_type):
                self.es.index(index=self.index_name, doc_type=doc_type, body={})

        result = self.es.search(doc_type=[doc_types[0]])
        self.assertEqual(count_per_doc_type, result.get('hits').get('total'))

        result = self.es.search(doc_type=doc_types[:2])
        self.assertEqual(count_per_doc_type * 2, result.get('hits').get('total'))

    def test_usage_of_aggregations(self):
        self.es.index(index='index', doc_type='document', body={'genre': 'rock'})

        body = {"aggs": {"genres": {"terms": {"field": "genre"}}}}
        result = self.es.search(index='index', body=body)

        self.assertTrue('aggregations' in result)

    def test_search_with_scroll_param(self):
        for _ in range(100):
            self.es.index(index='groups', doc_type='groups', body={'budget': 1000})

        result = self.es.search(index='groups', params={'scroll' : '1m', 'size' : 30})
        self.assertNotEqual(None, result.get('_scroll_id', None))
        self.assertEqual(30, len(result.get('hits').get('hits')))
        self.assertEqual(100, result.get('hits').get('total'))

    def test_scrolling(self):
        for _ in range(100):
            self.es.index(index='groups', doc_type='groups', body={'budget': 1000})
        
        result = self.es.search(index='groups', params={'scroll' : '1m', 'size' : 30})
        self.assertNotEqual(None, result.get('_scroll_id', None))
        self.assertEqual(30, len(result.get('hits').get('hits')))
        self.assertEqual(100, result.get('hits').get('total'))

        for _ in range(2):
            result = self.es.scroll(scroll_id = result.get('_scroll_id'), scroll = '1m')
            self.assertNotEqual(None, result.get('_scroll_id', None))
            self.assertEqual(30, len(result.get('hits').get('hits')))
            self.assertEqual(100, result.get('hits').get('total'))

        result = self.es.scroll(scroll_id = result.get('_scroll_id'), scroll = '1m')
        self.assertNotEqual(None, result.get('_scroll_id', None))
        self.assertEqual(10, len(result.get('hits').get('hits')))
        self.assertEqual(100, result.get('hits').get('total'))

    def test_update_existing_doc(self):
        data = self.es.index(index=self.index_name, doc_type=self.doc_type, body=self.body)
        document_id = data.get('_id')
        data = self.es.index(index=self.index_name, id=document_id, doc_type=self.doc_type, body=self.updated_body)
        target_doc = self.es.get(index=self.index_name, id=document_id)

        expected = {
            '_type': self.doc_type,
            '_source': self.updated_body,
            '_index': self.index_name,
            '_version': 2,
            'found': True,
            '_id': document_id
        }

        self.assertDictEqual(expected, target_doc)

if __name__ == '__main__':
    unittest.main()
