from django.contrib import admin
from .models import Item,Imagedetail,OrderItem,Order,Coupon,Payment
# Register your models here.


# for uploading multiple image for one item method ( inline ( parmi les lignes))
class ImagesInline(admin.StackedInline):
    model=Imagedetail
    extra=1

class DetailItem(admin.ModelAdmin):
    inlines=[ImagesInline]
    class Meta:
        model=Item
 







admin.site.register(Item,DetailItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Payment)