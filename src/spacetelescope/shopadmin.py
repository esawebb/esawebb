from product.models import *
from products.admin import *

from django.contrib.admin.sites import AdminSite
from djangoplicity.authtkt.utils import authtkt_decorator

admin = authtkt_decorator( AdminSite( name="adminshop_site" ) )

admin.site.register(Category, CategoryOptions)
admin.site.register(Discount, DiscountOptions)
admin.site.register(OptionGroup, OptionGroupOptions)
admin.site.register(Option, OptionOptions)
admin.site.register(Product, ProductOptions)
admin.site.register(CustomProduct, CustomProductOptions)
admin.site.register(CustomTextField, CustomTextFieldOptions)
admin.site.register(ConfigurableProduct)
admin.site.register(DownloadableProduct)
admin.site.register(SubscriptionProduct, SubscriptionProductOptions)
admin.site.register(ProductVariation, ProductVariationOptions)
admin.site.register(TaxClass)