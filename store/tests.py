from django.test import TestCase, Client
from django.urls import reverse
from store.models import Part, Order, OrderItem


class StoreCartOrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.part1 = Part.objects.create(
            name="Synthetic Engine Oil 5W-40",
            category="Engine",
            price=899.00,
            part_number="AP-ENG-001",
            stock=50,
            description="Test Engine Oil"
        )
        self.part2 = Part.objects.create(
            name="Ceramic Brake Pads",
            category="Brakes",
            price=1299.00,
            part_number="AP-BRK-002",
            stock=30,
            description="Test Brake Pads"
        )

    def test_home_page_and_categories(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Synthetic Engine Oil 5W-40")
        self.assertContains(response, "Ceramic Brake Pads")

        # Test category filter
        resp_filter = self.client.get(reverse('home') + '?category=Engine')
        self.assertEqual(resp_filter.status_code, 200)
        self.assertContains(resp_filter, "Synthetic Engine Oil 5W-40")
        self.assertNotContains(resp_filter, "Ceramic Brake Pads")

    def test_add_to_cart(self):
        # Add part 1
        response = self.client.get(reverse('add_to_cart', args=[self.part1.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['cart_count'], 1)

        # Check session cart
        session = self.client.session
        self.assertIn('cart', session)
        self.assertEqual(session['cart'][str(self.part1.id)]['quantity'], 1)

        # Add part 1 again
        response2 = self.client.get(reverse('add_to_cart', args=[self.part1.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data2 = response2.json()
        self.assertEqual(data2['cart_count'], 2)

    def test_cart_quantity_update_and_removal(self):
        # Add item
        self.client.get(reverse('add_to_cart', args=[self.part1.id]))
        self.client.get(reverse('add_to_cart', args=[self.part1.id]))

        # Increment
        resp_inc = self.client.get(reverse('update_cart_quantity', args=[self.part1.id, 'inc']), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data_inc = resp_inc.json()
        self.assertEqual(data_inc['item_quantity'], 3)

        # Decrement
        resp_dec = self.client.get(reverse('update_cart_quantity', args=[self.part1.id, 'dec']), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data_dec = resp_dec.json()
        self.assertEqual(data_dec['item_quantity'], 2)

        # Remove item completely
        resp_rem = self.client.get(reverse('remove_from_cart', args=[self.part1.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data_rem = resp_rem.json()
        self.assertEqual(data_rem['cart_count'], 0)
        self.assertTrue(data_rem['cart_empty'])

    def test_delivery_order_submission_and_confirmation(self):
        # Put items in cart
        self.client.get(reverse('add_to_cart', args=[self.part1.id]))
        self.client.get(reverse('add_to_cart', args=[self.part2.id]))

        # Submit delivery form
        delivery_data = {
            'full_name': 'Pranav Khode',
            'phone': '9876543210',
            'email': 'pranav@example.com',
            'address': 'Flat 402, Auto Residency, Sinhgad Road',
            'city': 'Pune',
            'state': 'Maharashtra',
            'pincode': '411041',
            'delivery_method': 'Express',
        }

        response = self.client.post(reverse('delivery'), data=delivery_data)
        self.assertEqual(response.status_code, 302)

        # Verify Order is in DB
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Pranav Khode')
        self.assertEqual(order.phone, '9876543210')
        self.assertEqual(order.delivery_method, 'Express')
        self.assertEqual(order.delivery_cost, 149.00)
        self.assertEqual(order.status, 'Placed')
        self.assertEqual(order.items.count(), 2)

        # Verify Cart is now empty in session
        session = self.client.session
        self.assertEqual(session.get('cart'), {})

        # Verify confirmation page
        conf_resp = self.client.get(reverse('order_confirmation', args=[order.order_id]))
        self.assertEqual(conf_resp.status_code, 200)
        self.assertContains(conf_resp, order.order_id)
        self.assertContains(conf_resp, "Pranav Khode")
        self.assertContains(conf_resp, "Live Delivery Tracking")

        # Verify order tracking
        track_resp = self.client.get(reverse('track_order') + f'?order_id={order.order_id}')
        self.assertEqual(track_resp.status_code, 200)
        self.assertContains(track_resp, order.order_id)
