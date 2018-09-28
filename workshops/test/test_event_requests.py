from django.core import mail
from django.urls import reverse

from .base import TestBase
from ..models import EventRequest, Event, Organization
from ..forms import SWCEventRequestForm, DCEventRequestForm


class TestSWCEventRequestForm(TestBase):
    def setUp(self):
        self._setUpUsersAndLogin()

    def test_fields_presence(self):
        """Test if the form shows correct fields."""
        form = SWCEventRequestForm()
        fields_left = set(form.fields.keys())
        fields_right = set([
            'name', 'email', 'affiliation', 'location', 'country',
            'conference', 'preferred_date', 'language', 'workshop_type',
            'approx_attendees', 'attendee_domains', 'attendee_domains_other',
            'attendee_academic_levels', 'attendee_computing_levels',
            'cover_travel_accomodation', 'understand_admin_fee',
            'travel_reimbursement', 'travel_reimbursement_other',
            'admin_fee_payment', 'comment', 'captcha', 'privacy_consent',
        ])
        self.assertEqual(fields_left, fields_right)

    def test_request_added(self):
        """Ensure the request is successfully added to the pool."""
        data = {
            'workshop_type': 'swc',
            'g-recaptcha-response': 'PASSED',  # to auto-pass RECAPTCHA
            'name': 'Harry Potter', 'email': 'harry@potter.com',
            'affiliation': 'Hogwarts', 'location': 'United Kingdom',
            'country': 'GB', 'preferred_date': 'soon',
            'approx_attendees': '20-40',
            'attendee_domains': [1, 2],  # IDs
            'attendee_domains_other': 'Nonsesology',
            'attendee_academic_levels': [1, 2],  # IDs
            'attendee_computing_levels': [1, 2],  # IDs
            'cover_travel_accomodation': True,
            'understand_admin_fee': True,
            'travel_reimbursement': 'book', 'travel_reimbursement_other': '',
            'admin_fee_payment': 'self-organized', 'comment': '',
            'privacy_consent': True,
        }
        rv = self.client.post(reverse('swc_workshop_request'), data,
                              follow=True)
        self.assertEqual(rv.status_code, 200)
        content = rv.content.decode('utf-8')
        self.assertNotIn('Fix errors below', content)
        self.assertIn('Thank you for requesting a workshop', content)
        self.assertEqual(EventRequest.objects.all().count(), 1)
        self.assertEqual(EventRequest.objects.all()[0].state, 'p')
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(
            msg.subject,
            '[SWC] New workshop request: Hogwarts, United Kingdom'
        )

    def test_request_discarded(self):
        """Ensure the request is discarded properly."""
        # add a minimal request
        er = EventRequest.objects.create(
            name='Harry Potter', email='harry@potter.com',
            affiliation='Hogwarts', location='United Kingdom',
            country='GB', workshop_type='swc',
        )
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[er.pk, 'discarded']))
        self.assertEqual(rv.status_code, 302)
        er.refresh_from_db()
        self.assertEqual(er.state, 'd')


class TestDCEventRequestForm(TestBase):
    def setUp(self):
        self._setUpUsersAndLogin()

    def test_fields_presence(self):
        """Test if the form shows correct fields."""
        form = DCEventRequestForm()
        fields_left = set(form.fields.keys())
        fields_right = set([
            'name', 'email', 'affiliation', 'location', 'country',
            'conference', 'preferred_date', 'language', 'workshop_type',
            'approx_attendees', 'attendee_domains', 'attendee_domains_other',
            'data_types', 'data_types_other', 'attendee_academic_levels',
            'attendee_data_analysis_level', 'cover_travel_accomodation',
            'understand_admin_fee', 'fee_waiver_request',
            'travel_reimbursement', 'travel_reimbursement_other',
            'comment', 'privacy_consent', 'captcha',
        ])
        self.assertEqual(fields_left, fields_right)

    def test_request_added(self):
        """Ensure the request is successfully added to the pool."""
        data = {
            'workshop_type': 'dc',
            'g-recaptcha-response': 'PASSED',  # to auto-pass RECAPTCHA
            'name': 'Harry Potter', 'email': 'harry@potter.com',
            'affiliation': 'Hogwarts', 'location': 'United Kingdom',
            'country': 'GB', 'preferred_date': 'soon',
            'approx_attendees': '20-40',
            'attendee_domains': [1, 2],  # IDs
            'attendee_domains_other': 'Nonsesology',
            'data_types': 'survey', 'data_types_other': '',
            'attendee_academic_levels': [1, 2],  # IDs
            'attendee_data_analysis_level': [1, 2],  # IDs
            'cover_travel_accomodation': True,
            'understand_admin_fee': True, 'fee_waiver_request': True,
            'travel_reimbursement': 'book', 'travel_reimbursement_other': '',
            'comment': '',
            'privacy_consent': True,
        }
        rv = self.client.post(reverse('dc_workshop_request'), data,
                              follow=True)
        self.assertEqual(rv.status_code, 200)
        content = rv.content.decode('utf-8')
        self.assertNotIn('Fix errors below', content)
        self.assertIn('Thank you for requesting a workshop', content)
        self.assertEqual(EventRequest.objects.all().count(), 1)
        self.assertEqual(EventRequest.objects.all()[0].state, 'p')
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(
            msg.subject,
            '[DC] New workshop request: Hogwarts, United Kingdom'
        )

    def test_request_discarded(self):
        """Ensure the request is discarded properly."""
        # add a minimal request
        er = EventRequest.objects.create(
            name='Harry Potter', email='harry@potter.com',
            affiliation='Hogwarts', location='United Kingdom',
            country='GB', workshop_type='dc',
        )
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[er.pk, 'discarded']))
        self.assertEqual(rv.status_code, 302)
        er.refresh_from_db()
        self.assertEqual(er.state, 'd')


class TestEventRequestsViews(TestBase):
    def setUp(self):
        self._setUpUsersAndLogin()

        self.er1 = EventRequest.objects.create(
            state="p", name="Harry Potter", email="harry@potter.com",
            affiliation="Hogwarts", location="Scotland", country="GB",
            preferred_date="soon",
        )
        self.er2 = EventRequest.objects.create(
            state="d", name="Harry Potter", email="harry@potter.com",
            affiliation="Hogwarts", location="Scotland", country="GB",
            preferred_date="soon",
        )

    def test_pending_requests_list(self):
        rv = self.client.get(reverse('all_eventrequests'))
        self.assertIn(self.er1, rv.context['requests'])
        self.assertNotIn(self.er2, rv.context['requests'])

    def test_discarded_requests_list(self):
        rv = self.client.get(reverse('all_eventrequests') + '?state=d')
        self.assertNotIn(self.er1, rv.context['requests'])
        self.assertIn(self.er2, rv.context['requests'])

    def test_set_state_pending_request_view(self):
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[self.er1.pk, 'discarded']))
        self.assertEqual(rv.status_code, 302)
        self.er1.refresh_from_db()
        self.assertEqual(self.er1.state, "d")

    def test_set_state_discarded_request_view(self):
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[self.er2.pk, 'discarded']))
        self.assertEqual(rv.status_code, 302)
        self.er2.refresh_from_db()
        self.assertEqual(self.er2.state, "d")

    def test_pending_request_accept(self):
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[self.er1.pk, 'accepted']))
        self.assertEqual(rv.status_code, 302)

    def test_pending_request_accepted_with_event(self):
        """Ensure a backlink from Event to EventRequest that created the
        event exists after ER is accepted."""
        data = {
            'slug': '2016-06-30-test-event',
            'host': Organization.objects.first().pk,
            'tags': [1],
            'invoice_status': 'unknown',
        }
        rv = self.client.post(
            reverse('eventrequest_accept_event', args=[self.er1.pk]),
            data)
        self.assertEqual(rv.status_code, 302)
        request = Event.objects.get(slug='2016-06-30-test-event').eventrequest
        self.assertEqual(request, self.er1)

    def test_discarded_request_accepted_with_event(self):
        rv = self.client.get(reverse('eventrequest_accept_event',
                                     args=[self.er2.pk]))
        self.assertEqual(rv.status_code, 404)

    def test_pending_request_discard(self):
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[self.er1.pk, 'discarded']),
                             follow=True)
        self.assertEqual(rv.status_code, 200)

    def test_discarded_request_discard(self):
        rv = self.client.get(reverse('eventrequest_set_state',
                                     args=[self.er2.pk, 'discarded']),
                             follow=True)
        self.assertEqual(rv.status_code, 200)

    def test_discarded_request_reopened(self):
        self.er1.state = "a"
        self.er1.save()
        rv = self.client.get(
            reverse('eventrequest_set_state',
                    args=[self.er1.pk, 'pending']),
            follow=True)
        self.er1.refresh_from_db()
        self.assertEqual(self.er1.state, "p")

    def test_accepted_request_reopened(self):
        self.assertEqual(self.er2.state, "d")
        rv = self.client.get(
            reverse('eventrequest_set_state',
                    args=[self.er2.pk, 'pending']),
            follow=True)
        self.er2.refresh_from_db()
        self.assertEqual(self.er2.state, "p")
