from django.db import models
from django.contrib.auth import get_user_model

from solotodo.models import Store, Category


class KeywordSearch(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=512)
    threshold = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'keyword_search_positions'
        ordering = ('-creation_date',)
        permissions = (
            ['backend_list_keyword_searches',
             'Can see keyword searches in the backend'],
        )
