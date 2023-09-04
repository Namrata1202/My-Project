from django.contrib import admin

# Register your models here.
from .models import Book,Product,Categories, BookUser,MyBook

admin.site.register(Book)
admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(BookUser)
admin.site.register(MyBook)


  # Register your model with the admin site
