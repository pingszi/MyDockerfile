from django.conf.urls import url
from .views import question_resolve, question_unresolve, search, hot_question, get_question,unsolved_email
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # 其他 url 配置
    url('search', search, name="search"),
    url('question_resolve', question_resolve, name="question_resolve"),
    url('question_unresolve', question_unresolve, name="question_unresolve"),
    url('hot_question', hot_question, name="hot_question"),
    url('unsolved_email', unsolved_email, name="unsolved_email"),

    # **输入提示
    url('get_question', get_question, name="get_question"),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

