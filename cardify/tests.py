from django.http import JsonResponse
from django.urls import reverse
from django.test import TestCase


class GraphQLAPITest(TestCase):

    def test_is_GraphQL_API_working(self):
        url = reverse('graphql')
        body = "{\"query\":\"query{\\r\\n    hello\\r\\n}\",\"variables\":{}}"
        response = self.client.post(
            url, content_type="application/json", data=body)
        data = response.json()
        return self.assertEquals(data['data']['hello'], "world")
