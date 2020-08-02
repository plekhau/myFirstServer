from django.test import TestCase

from birds.models import Birds


class BirdsViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Birds.objects.create(species="sparrow", name="Kadu", color="black & white", body_length=14, wingspan=23)
        Birds.objects.create(species="magpie", name="Belka", color="black", body_length=44, wingspan=52)
        Birds.objects.create(species="pigeon", name="Tima", color="grey", body_length=30, wingspan=56)
        Birds.objects.create(species="pigeon", name="Ptusha", color="red & white", body_length=31, wingspan=63)
        Birds.objects.create(species="crow", name="Cown", color="black & white", body_length=56, wingspan=100)
        Birds.objects.create(species="crow", name="Koul", color="red & white", body_length=78, wingspan=95)
        Birds.objects.create(species="sparrow", name="Like", color="black", body_length=18, wingspan=24)
        Birds.objects.create(species="magpie", name="Clod", color="red & white", body_length=45, wingspan=54)
        Birds.objects.create(species="titmouse", name="Birdy", color="red", body_length=12, wingspan=22)
        Birds.objects.create(species="crow", name="Nord", color="black", body_length=72, wingspan=110)

    # VersionView
    # GET /version
    def test_VersionView_get(self):
        response = self.client.get('/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Birds Service. Version 0.1")

    # BirdsView
    # GET /birds
    def test_BirdsView_get(self):
        response = self.client.get('/birds')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_order_by_name(self):
        response = self.client.get('/birds?attribute=name&order=asc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Belka")

    def test_BirdsView_get_order_by_name_desc(self):
        response = self.client.get('/birds?attribute=name&order=desc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Tima")

    def test_BirdsView_get_order_by_name_without_order(self):
        # default order=asc is used
        response = self.client.get('/birds?attribute=name')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Belka")

    def test_BirdsView_get_only_order(self):
        # no ordering
        response = self.client.get('/birds?order=asc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_order_by_int_field(self):
        response = self.client.get('/birds?attribute=body_length&order=asc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Birdy")

    def test_BirdsView_get_order_by_int_field_desc(self):
        response = self.client.get('/birds?attribute=body_length&order=desc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Koul")

    def test_BirdsView_get_wrong_attribute(self):
        response = self.client.get('/birds?attribute=id&order=asc')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'id' column is not present in db")

    def test_BirdsView_get_wrong_order(self):
        response = self.client.get('/birds?attribute=name&order=increase')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "Unexpected order: 'increase'")

    def test_BirdsView_get_offset(self):
        offset = 3
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count()-offset)
        self.assertEqual(response.data[0].get('name'), "Ptusha")

    def test_BirdsView_get_zero_offset(self):
        offset = 0
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count()-offset)
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_negative_offset(self):
        offset = -3
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'offset' must be 0 or more")

    def test_BirdsView_get_float_offset(self):
        offset = 3.5
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'offset' must be integer")

    def test_BirdsView_get_string_offset(self):
        offset = 'abc'
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'offset' must be integer")

    def test_BirdsView_get_empty_offset(self):
        offset = ''
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'offset' must be integer")

    def test_BirdsView_get_offset_more_than_count(self):
        offset = Birds.objects.count() + 10
        response = self.client.get('/birds?offset={}'.format(offset))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, "No birds were found")

    def test_BirdsView_get_limit(self):
        limit = 3
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), limit)
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_limit_more_than_count(self):
        limit = Birds.objects.count()+10
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_zero_limit(self):
        # no limit
        limit = 0
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Birds.objects.count())
        self.assertEqual(response.data[0].get('name'), "Kadu")

    def test_BirdsView_get_negative_limit(self):
        limit = -3
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'limit' must be more than 0")

    def test_BirdsView_get_float_limit(self):
        limit = 3.5
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'limit' must be integer")

    def test_BirdsView_get_string_limit(self):
        limit = 'abc'
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'limit' must be integer")

    def test_BirdsView_get_empty_limit(self):
        limit = ''
        response = self.client.get('/birds?limit={}'.format(limit))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, "'limit' must be integer")

    def test_BirdsView_get_several_params1(self):
        limit = 3
        offset = 3
        response = self.client.get('/birds?limit={}&offset={}'.format(limit, offset))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), limit)
        self.assertEqual(response.data[0].get('name'), "Ptusha")

    def test_BirdsView_get_several_params2(self):
        limit = 3
        offset = 3
        response = self.client.get('/birds?limit={}&offset={}&attribute=name&order=asc'.format(limit, offset))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), limit)
        self.assertEqual(response.data[0].get('name'), "Cown")

    def test_BirdsView_get_extra_params(self):
        limit = 3
        offset = 3
        response = self.client.get('/birds?limit={}&offset={}&attribute=name&order=asc&db=my_db'.format(limit, offset))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), limit)
        self.assertEqual(response.data[0].get('name'), "Cown")

    # BirdsView
    # POST /birds
    def test_BirdsView_post(self):
        data = {"species": "sparrow", "name": "test1", "color": "black & white", "body_length": 14, "wingspan": 23}
        response = self.client.post('/birds', data, format='json')
        self.assertEqual(response.status_code, 200)

