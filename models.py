from django.db import models

from django.utils.translation import ugettext_lazy as _


from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


AbstractUser._meta.get_field('email')._unique = False
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('first_name').blank = True
AbstractUser._meta.get_field('last_name').blank = True

class User(AbstractUser):
	phone = models.CharField(_('Phone'), max_length=50)
	address = models.CharField(_('Address'), max_length=50, blank=True, null=True)

	objects = UserManager()

	def __unicode__(self):
		return self.username


from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Order (models.Model):
	user = models.ForeignKey(User, null=True, blank=True)

	name = models.CharField(_('Name'), max_length=100)
	email = models.EmailField(_('E-Mail'), max_length=100)
	phone = models.CharField(_('Phone'), max_length=100)
	comment = models.TextField(_('Comment'), null=True, blank=True)

	retail_price = models.DecimalField(_('Retail Price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	wholesale_price = models.DecimalField(_('Wholesale Price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))
	retail_price_with_discount = models.DecimalField(_('Retail Price With Discount'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))

	STATUS_CHOICES = (
		('created', _('Created')),
		('processed', _('Processed')),
		('canceled', _('Canceled')),
		('success', _('Success')),
	)
	status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='created', max_length=32)
	def save(self, sort=True, *args, **kwargs):
		for item in self.items.all():
			self.retail_price += item.get_total_retail_price()
			self.wholesale_price += item.get_total_wholesale_price()
			self.retail_price_with_discount += item.get_total_retail_price_with_discount()
		super(Order, self).save(*args, **kwargs)

	def __unicode__(self):
		string = '%s #%s = [%s]' % (self.user, self.id, self.retail_price_with_discount)
		return string

class OrderItem (models.Model):
	user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True)
	order = models.ForeignKey(Order, verbose_name=_('Order'), null=True, blank=True, related_name='items')

	content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'))
	object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
	content_object = GenericForeignKey('content_type', 'object_id')

	retail_price = models.DecimalField(_('Retail Price'), max_digits=16, decimal_places=4, default=Decimal('0.0000'))
	wholesale_price = models.DecimalField(_('Wholesale Price'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))
	retail_price_with_discount = models.DecimalField(_('Retail Price With Discount'), max_digits=16, decimal_places=4, null=True, blank=True, default=Decimal('0.0000'))

	count = models.IntegerField(_('Count'), null=True, blank=True, default=0)

	def get_total_retail_price(self):
		return self.retail_price * self.count

	def get_total_wholesale_price(self):
		return self.wholesale_price * self.count

	def get_total_retail_price_with_discount(self):
		return self.retail_price_with_discount * self.count

	def __unicode__(self):
		string = '#%s (%sx%s) = [%s]' % (
			self.id,
			self.retail_price_with_discount,
			self.count,
			self.get_total_retail_price_with_discount()
		)
		return string

	def save(self, sort=True, *args, **kwargs):
		if not self.order:
			self.retail_price = self.content_object.retail_price
			self.wholesale_price = self.content_object.wholesale_price
			self.retail_price_with_discount = self.content_object.retail_price_with_discount
		super(OrderItem, self).save(*args, **kwargs)
