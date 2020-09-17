from django.contrib.auth.models import User
from django.test import TestCase, Client, tag
from django.urls import reverse
from djangoplicity.announcements.models import Announcement

from djangoplicity.media.models import Video
from djangoplicity.newsletters.models import Newsletter, NewsletterType
# from djangoplicity.products.models import Book
from djangoplicity.releases.models import Release
from djangoplicity.science.models import ScienceAnnouncement

# from product.models import Product, Category
# from satchmo_store.shop.models import Config


class TestViewAsAdminUser(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test_admin', password='admin')
        # self.book = Book.objects.first()

    def test_login(self):
        login_url = reverse('admin:login')
        index_url = reverse('admin:index')

        response = self.client.get(login_url, follow=True)

        self.assertGreater(len(response.redirect_chain), 0)

        last_url, status_code = response.redirect_chain[-1]

        self.assertEqual(last_url, index_url)
        self.assertEqual(status_code, 302)


# class TestViewsAsStandardUser(TestCase):
#     fixtures = ['test']
#
#     def setUp(self):
#         self.client = Client()
#         self.client.login(username='test_standard', password='admin')
#         self.published_book = Book.objects.filter(published=True).first()
#         self.not_published_book = Book.objects.filter(published=False).first()
#
#     def test_book_published(self):
#         url = reverse('books_detail', args=[str(self.published_book.id)])
#         response = self.client.get(url)
#
#         self.assertContains(response, self.published_book.title, status_code=200)
#
#     def test_book_not_published(self):
#         """
#         This test provides coverage for:
#         spacetelescope/templates/403.html
#         """
#         url = reverse('books_detail', args=[str(self.not_published_book.id)])
#         response = self.client.get(url)
#
#         self.assertContains(response, 'Access Denied', status_code=403)


@tag('announcements')
class TestAnnouncements(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.announcement = Announcement.objects.first()
        self.science_announcement = ScienceAnnouncement.objects.first()

    def test_announcements(self):
        response = self.client.get('/announcements/')
        self.assertContains(response, '<h1>Announcements <a href="http://feeds.feedburner.com/hubble_announcements/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_announcements_detail(self):
        response = self.client.get('/announcements/%s/' % self.announcement.pk)
        self.assertContains(response, self.announcement.title)

    def test_announcements_webupdates(self):
        response = self.client.get('/announcements/webupdates/')
        self.assertContains(response,
                            '<h1>Web Updates <a href="/announcements/webupdates/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_forscientists(self):
        response = self.client.get('/forscientists/announcements/')
        self.assertContains(response,
                            '<h1>Announcements <a href="/forscientists/announcements/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_forscientists_detail(self):
        response = self.client.get('/forscientists/announcements/{}/'.format(self.science_announcement.pk))
        self.assertContains(response, self.science_announcement.title)


@tag('media')
class TestMedia(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()
        self.video = Video.objects.get(pk='10000')

    def test_images(self):
        response = self.client.get('/images/')
        self.assertContains(response, 'View All')
        self.assertContains(response, 'Ranking')
        self.assertContains(response, 'Date')
        #self.assertContains(response, '<h1>Images <a href="/images/feed/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>', html=True)

    def test_images_potw(self):
        response5 = self.client.get('/images/potw/')
        self.assertContains(response5,
                            '<h1>Picture of the Week <a href="http://feeds.feedburner.com/hubble_potw/" class="listviewrsslink"><span class="fa fa-rss"></span></a></h1>')

    def test_images_comparisons(self):
        response = self.client.get('/images/comparisons/')
        self.assertContains(response, '<h1>Image Comparisons</h1>')

    def test_image_top(self):
        response = self.client.get('/images/archive/top100/')
        self.assertContains(response, 'Top 100 Images')

    def test_videos_list(self):
        response = self.client.get('/videos/')
        self.assertContains(response, '<a href="/copyright/">Usage of ESA/Hubble Images and Videos</a>')

    def test_videos_detail(self):
        response = self.client.get('/videos/{}/'.format(self.video.id))
        self.assertContains(response, self.video.title)

    def test_video_hubblecast(self):
        response = self.client.get('/videos/archive/category/hubblecast/')
        self.assertContains(response, 'All Hubblecasts')


# @tag('shop')
# class TestShop(TestCase):
#     fixtures = ['test', 'test/shop']
#
#     def setUp(self):
#         self.client = Client()
#
#         self.shop = Config.objects.first()
#         # Shows a category hierarchy in product_detail view
#         self.category = Category.objects.get(pk=10000)
#         self.category_with_meta = Category.objects.get(pk=10002)
#         self.product = Product.objects.first()
#
#     def test_index(self):
#         response = self.client.get('/shop/')
#         self.assertContains(response, self.shop.store_name)
#
#     def test_freeorder(self):
#         response = self.client.get('/shop/freeorder/')
#         self.assertContains(response, 'Full Name')
#         self.assertContains(response, 'Email Address')
#         self.assertContains(response, 'Country of delivery')
#         self.assertContains(response, 'Justification')
#
#     def test_freeorder_done(self):
#         # Submit form in order to proceed to freeorder confirmation
#         response = self.client.post(
#             '/shop/freeorder/',
#             data={
#                 'name': 'jhon doe',
#                 'email': 'doe@test.com',
#                 'newsletter': 'on',
#                 'country': 10000,
#                 'justification': 'Whatever',
#                 'g-recaptcha-response': None
#             },
#             follow=True
#         )
#         self.assertContains(response, 'Free order application submitted')
#
#     def test_category_detail(self):
#         response = self.client.get('/shop/category/%s/' % self.category.slug)
#         self.assertContains(response, self.category.name)
#
#     def test_category_detail_meta(self):
#         response = self.client.get('/shop/category/%s/' % self.category_with_meta.slug)
#         self.assertContains(response, self.category.name)
#
#     def test_product_process(self):
#         # Visit cart page without products in cart
#         response = self.client.get('/shop/cart/')
#         self.assertContains(response, 'Shopping Cart')
#
#         # Add some products to cart, in order to render the cart_box template in the product detail
#         response = self.client.post('/shop/add/', {
#             'quantity': 3,
#             'productname': self.product.slug
#         })
#         self.assertEqual(response.status_code, 302)
#
#         # Visit product detail
#         response = self.client.get('/shop/product/%s/' % self.product.slug)
#         self.assertContains(response, self.product.name)
#
#         # Visit cart page
#         response = self.client.get('/shop/cart/')
#         self.assertContains(response, self.product.name)
#
#         # Visit checkout page
#         response = self.client.get('/shop/checkout/')
#         self.assertContains(response, 'Step 1 of 3')
#
#         # Bad submit form in order to raise form errors
#         response = self.client.post(
#             '/shop/checkout/',
#             {
#                 'paymentmethod': 'CONCARDIS',
#                 'ship_country': 10000,
#                 'discount': '000'
#             },
#             follow=True
#         )
#         self.assertEqual(response.status_code, 200)
#
#         # Submit form in order to proceed to payment
#         response = self.client.post(
#             '/shop/checkout/',
#             {
#                 'paymentmethod': 'CONCARDIS',
#                 'email': 'test@mail.com',
#                 'city': 'Neverland',
#                 'first_name': 'Sheldon',
#                 'last_name': 'Cooper',
#                 'phone': '69300012',
#                 'addressee': 'Amy Farrah Fowler',
#                 'street1': 'In the middle of Nowhere',
#                 'street2': 'Maybe you should look behing you',
#                 'state': 'Bermuda',
#                 'postal_code': '23836',
#                 'country': 10000,
#                 'copy_address': 'on',
#                 'discount': '666',
#             },
#             follow=True
#         )
#         self.check_redirection_to(response, '/shop/checkout/payment/')
#
#         # Submit form in order to proceed to confirmation
#         response = self.client.post(
#             '/shop/checkout/payment/',
#             {
#                 'shipping': 'PUP1'
#             },
#             follow=True
#         )
#         self.check_redirection_to(response, '/shop/checkout/payment/confirm/')
#
#         # We can't check concardis, but we can assume the order was placed successfully
#         response = self.client.get('/shop/checkout/success/')
#         self.assertContains(response, 'Order successfully completed')
#
#     def check_redirection_to(self, response, to):
#         redirects_number = len(response.redirect_chain)
#         last_url, status_code = response.redirect_chain[-1] if redirects_number > 0 else (None, None)
#
#         self.assertGreater(redirects_number, 0)
#         self.assertEqual(status_code, 302)
#         self.assertEqual(last_url, to)


@tag('pages')
class TestPageTemplate(TestCase):
    fixtures = ['test', 'test/pages']

    def setUp(self):
        self.client = Client()

    def test_onecolumn(self):
        response_online = self.client.get('/test-online/')
        response_offline = self.client.get('/test-not-online/')

        self.assertEqual(response_online.status_code, 200)
        self.assertEqual(response_offline.status_code, 404)

    def test_onecolumn_as_admin(self):
        self.client.login(username='test_admin', password='admin')
        response_offline = self.client.get('/test-not-online/')

        self.assertEqual(response_offline.status_code, 200)

    def test_onecolumn_coming_soon(self):
        self.client.login(username='test_admin', password='admin')
        response_online = self.client.get('/test-online-coming-soon/')
        self.assertEqual(response_online.status_code, 200)


@tag('newsletters')
class TestNewsletters(TestCase):
    fixtures = ['test', 'test/newsletters']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.filter(is_staff=True).first())

        self.newsletter_types = NewsletterType.objects.all()
        self.newsletter = Newsletter.objects.filter(published=True, send__isnull=False).first()

    def test_newsletter_generation(self):
        for newsletter_type in self.newsletter_types:
            response = self.client.post(
                '/admin/newsletters/newsletter/new/',
                {
                    'type': newsletter_type.pk,
                    'start_date_0': '01/01/2000',
                    'start_date_1': '00:00:00',
                    'end_date_0': '31/12/2020',
                    'end_date_1': '23:59:59',
                    '_generate': 'Generate'
                },
                follow=True
            )

            self.assertGreater(len(response.redirect_chain), 0)

            last_url, status_code = response.redirect_chain[-1]

            self.assertEqual(status_code, 302)
            self.assertRegexpMatches(last_url, r'/admin/newsletters/newsletter/[0-9]+/change/')

    def test_newsletter_list(self):
        url = '/newsletters/{}/'.format(self.newsletter.type.slug)

        response = self.client.get('{}{}'.format(url, '?search=this+does+not+exists'))
        self.assertContains(response, 'No entries were found')

        response = self.client.get(url)
        self.assertContains(response, self.newsletter.type.name)

    def test_newsletter_detail(self):
        response = self.client.get('/newsletters/{}/html/{}/'.format(self.newsletter.type.slug, self.newsletter.pk))
        self.assertContains(response, self.newsletter.subject)


class TestGeneralPurpose(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.client = Client()

    def test_login_error(self):
        response = self.client.post('/login/', {'username': 'test_standard', 'password': 'badpassword'})
        self.assertContains(response, 'Your username and password didn\'t match. Please try again.')

    def test_login_success(self):
        response = self.client.post('/login/', {'username': 'test_standard', 'password': 'admin'}, follow=True)

        self.assertGreater(len(response.redirect_chain), 0)

        last_url, status_code = response.redirect_chain[-1]

        self.assertEqual(last_url, '/')
        self.assertEqual(status_code, 302)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertContains(response, 'You have been successfully logged out.')

    def test_feed(self):
        response = self.client.get('/rss/feed.xml')
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        response_get = self.client.get('/password_reset/')
        self.assertContains(response_get,
                            '<p>Forgotten your password? Enter your e-mail address below, and we\'ll e-mail instructions for setting a new one.</p>')

        response_post = self.client.post("/password_reset/", data={"email": "test@email.com"})
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_post["Location"], "/password_reset/done/")


@tag('releases')
class TestReleases(TestCase):
    fixtures = ['test', 'test/releases']

    def setUp(self):
        self.client = Client()
        self.release = Release.objects.get(pk=10000)
        self.release_staging = Release.objects.get(pk=10001)
        self.release_unpublished = Release.objects.get(pk=10002)
        self.release_embargoed = Release.objects.get(pk=10003)

    def test_news(self):
        response = self.client.get('/news/')
        self.assertContains(response, 'Press Releases')

    def test_release_detail(self):
        response = self.client.get('/news/{}/'.format(self.release.pk))
        self.assertContains(response, self.release.title)

    def test_release_embargoed(self):
        self.client.login(username='test_admin', password='admin')
        response = self.client.get('/news/{}/'.format(self.release_embargoed.pk))
        self.assertContains(response, self.release_embargoed.title)

    def test_release_staging(self):
        self.client.login(username='test_admin', password='admin')
        response = self.client.get('/news/{}/'.format(self.release_staging.pk))
        self.assertContains(response, self.release_staging.title)

    def test_release_unpublished(self):
        self.client.login(username='test_admin', password='admin')
        response = self.client.get('/news/{}/'.format(self.release_unpublished.pk))
        self.assertContains(response, self.release_unpublished.title)

    def test_release_kids(self):
        response = self.client.get('/news/{}/kids/'.format(self.release.pk))
        self.assertContains(response, self.release.kids_title)


# @tag('products')
# class TestProducts(TestCase):
#     fixtures = ['test', 'test/products']
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_arts(self):
#         response = self.client.get('/products/art/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_kidsdrawing(self):
#         response = self.client.get('/kidsandteachers/drawings/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_postcards(self):
#         response = self.client.get('/products/postcards/')
#         self.assertContains(response, 'Postcards')
#
#     def test_merchandise(self):
#         response = self.client.get('/products/merchandise/')
#         self.assertContains(response, 'Merchandise')
