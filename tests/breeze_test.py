"""Unittests for breeze.py

Usage:
  python -m unittest tests.breeze_test
"""

import json
import unittest

from breeze import breeze


class MockConnection(object):
  """Mock requests connection."""
  def __init__(self, response):
    self._url = None
    self._params = None
    self._headers = None
    self._response = response

  def post(self, url, params, headers, *args, **kwargs):
    self._url = url
    self._params = params
    self._headers = headers
    return self._response

  @property
  def url(self):
    return self._url

  @property
  def params(self):
    return self._params


class MockResponse(object):
  """ Mock requests HTTP response."""
  def __init__(self, status_code, content):
    self.status_code = status_code
    self.content = content

  @property
  def ok(self):
    return str(self.status_code).startswith('2')

  def json(self):
    if self.content:
        return json.loads(self.content)
    return None

  def raise_for_status(self):
    raise Exception('Fake HTTP Error')


class BreezeApiTestCase(unittest.TestCase):
  def setUp(self):
    self.FAKE_API_KEY = 'fak3ap1k3y'
    self.FAKE_SUBDOMAIN = 'https://demo.breezechms.com'

  def testInvalidSubdomain(self):
    self.assertRaises(breeze.BreezeError,
        lambda: breeze.BreezeApi(api_key=self.FAKE_API_KEY,
                          breeze_url='invalid-subdomain'))
    self.assertRaises(breeze.BreezeError,
        lambda: breeze.BreezeApi(api_key=self.FAKE_API_KEY,
                          breeze_url='http://blah.breezechms.com'))
    self.assertRaises(breeze.BreezeError,
        lambda: breeze.BreezeApi(api_key=self.FAKE_API_KEY, breeze_url=''))

  def testMissingApiKey(self):
    self.assertRaises(breeze.BreezeError,
        lambda: breeze.BreezeApi(api_key=None, breeze_url=self.FAKE_SUBDOMAIN))
    self.assertRaises(breeze.BreezeError,
        lambda: breeze.BreezeApi(api_key='', breeze_url=self.FAKE_SUBDOMAIN))

  def testGetPeople(self):
    response = MockResponse(200, json.dumps({'name': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)

    breeze_api.GetPeople(limit=1, offset=1, details=True)
    self.assertEquals(
        connection.url,
        '%s%s/?%s' % (self.FAKE_SUBDOMAIN,
                      breeze.ENDPOINTS.PEOPLE,
                      '&'.join(['limit=1', 'offset=1', 'details=1'])))
    self.assertEquals(
        breeze_api.GetPeople(),
        json.loads(response.content))

  def testGetProfileFields(self):
    response = MockResponse(200, json.dumps({'name': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)
    self.assertEqual(breeze_api.GetProfileFields(), json.loads(response.content))

  def testGetPersonDetails(self):
    response = MockResponse(200, json.dumps({'person_id': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)

    person_id = '123456'
    breeze_api.GetPersonDetails(person_id)
    self.assertEquals(
        connection.url,
        '%s%s/%s' % (self.FAKE_SUBDOMAIN,
                      breeze.ENDPOINTS.PEOPLE,
                      person_id))
    self.assertEqual(breeze_api.GetPersonDetails(person_id),
                     json.loads(response.content))

  def testGetEvents(self):
    response = MockResponse(200, json.dumps({'event_id': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)

    start_date = '3-1-2014'
    end_date = '3-7-2014'
    breeze_api.GetEvents(start_date=start_date, end_date=end_date)
    self.assertEquals(
        connection.url,
        '%s%s/?%s' % (self.FAKE_SUBDOMAIN,
                      breeze.ENDPOINTS.EVENTS,
                      '&'.join(['start=%s' % start_date,
                                'end=%s' % end_date])))
    self.assertEqual(breeze_api.GetEvents(),json.loads(response.content))

  def testEventCheckIn(self):
    response = MockResponse(200, json.dumps({'event_id': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)
    self.assertEqual(breeze_api.EventCheckIn('person_id', 'event_id'),
                     json.loads(response.content))

  def testEventCheckOut(self):
    response = MockResponse(200, json.dumps({'event_id': 'Some Data.'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)
    self.assertEqual(breeze_api.EventCheckOut('person_id', 'event_id'),
                     json.loads(response.content))

  def testAddContribution(self):
    response = MockResponse(200, json.dumps({'success': 'true'}))
    connection = MockConnection(response)
    breeze_api = breeze.BreezeApi(
        breeze_url=self.FAKE_SUBDOMAIN,
        api_key=self.FAKE_API_KEY,
        connection=connection)
    date = '3-1-2014'
    name = 'John Doe'
    person_id = '123456'
    uid = 'UID'
    processor = 'Processor'
    method = 'Method'
    funds_json = "[{'id': '12345', 'name': 'Fund', 'amount', '150.00' }]"
    amount = '150.00'
    group = 'Group'
    batch_number = '100'
    batch_name = 'Batch Name'

    breeze_api.AddContribution(
        date=date,
        name=name,
        person_id=person_id,
        uid=uid,
        processor=processor,
        method=method,
        funds_json=funds_json,
        amount=amount,
        group=group,
        batch_number=batch_number,
        batch_name=batch_name)
    self.assertEquals(
        connection.url,
        '%s%s/add?%s' % (self.FAKE_SUBDOMAIN,
                      breeze.ENDPOINTS.CONTRIBUTIONS,
                       '&'.join(['date=%s' % date,
                                 'name=%s' % name,
                                 'person_id=%s' % person_id,
                                 'uid=%s' % uid,
                                 'processor=%s' % processor,
                                 'method=%s' % method,
                                 'funds_json=%s' % funds_json,
                                 'amount=%s' % amount,
                                 'group=%s' % group,
                                 'batch_number=%s' % batch_number,
                                 'batch_name=%s' % batch_name])))
    self.assertEqual(breeze_api.AddContribution(),
                     json.loads(response.content))


if __name__ == '__main__':
  unittest.main()
