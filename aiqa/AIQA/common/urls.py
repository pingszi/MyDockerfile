from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import findall


urlpatterns = [
    # 根据sql查询所有数据
    url('findall', findall, name="findall"),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
