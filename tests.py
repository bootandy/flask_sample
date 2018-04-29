import os
import time
import unittest

import web
from flask import json


if __name__ == '__main__':
    unittest.main()


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        web.app.config['TESTING'] = True
        web.app.config['DATABASE'] = 'test.db'
        web.app.config['WTF_CSRF_ENABLED'] = False
        self.app = web.app.test_client()

    def tearDown(self):
        os.remove('test.db')

    def test_empty_db(self):
        rv = self.app.get('/documents')
        assert b'' == rv.data

    def test_single_item(self):
        rv = self.app.post('/documents/first', data = json.dumps({'content': 'first_content'}), content_type='application/json')
        assert 'Data inserted' == rv.data

        rv = self.app.get('/documents')
        assert 'first' == rv.data

        rv = self.app.get('/documents/first')
        assert rv.data.count('\n') == 1

        rv = self.app.get('/documents/first/latest')
        assert 'first_content' == rv.data

    def test_single_document_several_versions(self):
        for i in range(0, 2):
            rv = self.app.post('/documents/many_version', data = json.dumps({'content': 'c %i'%i}), content_type='application/json')
            # Very ugly but we need a delay or sqlite will put the same timestamp in for these posts
            # Testing against a proper DB like postgres should mean we can remove this line
            time.sleep(1)
            assert 'Data inserted' == rv.data

        rv = self.app.get('/documents')
        assert 'many_version' == rv.data

        rv = self.app.get('/documents/many_version')
        assert rv.data.count('\n') == 2

        times = rv.data.split('\n')[1:]
        for t in times:
            t = t.replace(' ', '%20')
            rv = self.app.get('/documents/many_version/%s'%t)
            assert rv.data in ('c 0', 'c 1')

        rv = self.app.get('/documents/many_version/latest')
        assert 'c 1' == rv.data

    def test_many_documents(self):
        for i in range(0, 5):
            rv = self.app.post('/documents/i%i' % i, data = json.dumps({'content': 'c %i'%i}), content_type='application/json')
            assert 'Data inserted' == rv.data

        rv = self.app.get('/documents')
        assert rv.data == """i0
i1
i2
i3
i4"""