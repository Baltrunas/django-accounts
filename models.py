from decimal import Decimal

from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


AbstractUser._meta.get_field('email')._unique = False
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('first_name').blank = True
AbstractUser._meta.get_field('last_name').blank = True
AbstractUser._meta.get_field('last_login').blank = True

class User(AbstractUser):
	phone = models.CharField(_('Phone'), max_length=50)
	address = models.CharField(_('Address'), max_length=50, blank=True, null=True)

	objects = UserManager()

	def __unicode__(self):
		if self.first_name or self.last_name:
			name = '%s %s' % (self.first_name, self.last_name)
		else:
			name = self.username
		return name.strip()


class PromoCode(models.Model):
	code = models.CharField(verbose_name=_('Code'), max_length=32)
	name = models.CharField(verbose_name=_('Name'), max_length=256)
	description = models.TextField(verbose_name=_('Description'))

	TYPE_DISCOUNT = (
		('interest', _('Interest')),
		('percent', _('Percent')),
	)
	discount_type = models.CharField(verbose_name=_('Discout type'), max_length=10, choices=TYPE_DISCOUNT)
	discount_value = models.DecimalField(verbose_name=_('Discout value'), max_digits=10, decimal_places=0)

	limit = models.DecimalField(verbose_name=_('Limit'), max_digits=60, decimal_places=0)

	active = models.BooleanField(verbose_name=_('Active'), default=False)
	active_from = models.DateField(verbose_name=_('Active from'), blank=True, null=True)
	active_before = models.DateField(verbose_name=_('Active before'))

	sum_up = models.BooleanField(verbose_name=_('Sum up'), default=False)
	only_registered = models.BooleanField(verbose_name=_('Only registered'), default=False)
	one_per_user = models.BooleanField(verbose_name=_('One per user'), default=False)

	def used_by_user(self, user):
		return self.orders.filter(user=user).count()

	def used_count(self):
		return self.orders.count()

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('Promo Code')
		verbose_name_plural = _('Promo Codes')


class Order (models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	guid = models.CharField(_('GUID'), max_length=37, null=True, blank=True, editable=False)

	name = models.CharField(_('Name'), max_length=100)
	email = models.EmailField(_('E-Mail'), max_length=100, null=True, blank=True)
	address = models.CharField(_('Address'), max_length=300)
	phone = models.CharField(_('Phone'), max_length=100)

	promocode = models.ForeignKey(PromoCode, verbose_name=_('Promo Code'), related_name='orders', blank=True, null=True)

	comment = models.TextField(_('Comment'), null=True, blank=True)

	retail_price = models.DecimalField(_('Retail Price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	discount_price = models.DecimalField(_('Discount price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))

	STATUS_CHOICES = (
		('new', _('New')),
		('accept', _('Accept by:')),
		('processed', _('Processed (1c)')),
		('paid', _('Paid')),
		('success', _('Success')),
		('canceled', _('Canceled')),
	)

	status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='new', max_length=32)

	PAYMENT_STATUS_CHOICES = (
		('created', _('Created')),
		('failed', _('Failed')),
		('processed', _('Processed')),
		('success', _('Success')),
		('canceled', _('Canceled')),
		('error', _('Error')),
	)
	payment_status = models.CharField(_('Payment status'), choices=PAYMENT_STATUS_CHOICES, default='created', max_length=32)

	payment_method = models.CharField(verbose_name=_('Payment method'), max_length=64, choices=settings.ACCOUNTS_PAYMENTS, default='cash')

	accounting = models.BooleanField(verbose_name=_('Accounting'), default=False)

	acceptor = models.ForeignKey(User, null=True, blank=True, related_name='acceptors')

	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)


	def __unicode__(self):
		string = '#%010d %s = [%s]' % (self.id, self.user, self.discount_price)
		return string


class OrderItem (models.Model):
	user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True)
	order = models.ForeignKey(Order, verbose_name=_('Order'), null=True, blank=True, related_name='items')

	content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'))
	object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
	content_object = GenericForeignKey('content_type', 'object_id')

	retail_price = models.DecimalField(_('Retail price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	discount_price = models.DecimalField(_('Discount price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))

	count = models.IntegerField(_('Count'), null=True, blank=True, default=0)

	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

	def total_retail_price(self):
		return self.retail_price * self.count

	def total_discount_price(self):
		return self.discount_price * self.count

	def __unicode__(self):
		string = '#%s (%sx%s) = [%s]' % (
			self.id,
			self.discount_price,
			self.count,
			self.total_discount_price()
		)
		return string

	def save(self, *args, **kwargs):
		if not self.order:
			self.retail_price = self.content_object.retail_price
			self.discount_price = self.content_object.retail_price_with_discount
		super(OrderItem, self).save(*args, **kwargs)


class Valute (models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=128)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128, help_text=_('A slug is the part of a URL which identifies a page using human-readable keywords'))
	rate = models.DecimalField(_('Currency rate'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	decimal_places = models.PositiveIntegerField(verbose_name=_('Decimal places'), default=0)

	class Meta:
		ordering = ['name']
		verbose_name = _('Currency rate')
		verbose_name_plural = _('Currency rates')

	def __unicode__(self):
		return '%s (%s)' % (self.name, self.rate)
