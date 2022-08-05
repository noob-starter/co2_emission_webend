
from django.contrib import admin
from django.urls import path,include
from .views import general_explore,world_emission
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('world_emission', world_emission,name= ""),
    # path('tree_map', tree_map,name= ""),
    # path('map_world', map_world,name= ""),
    # path('', world_emission,name= ""),
    # path('', world_emission,name= ""),
    # path('', world_emission,name= ""),
    path('explore/', general_explore,name= ""),
    path('', world_emission,name= ""),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
