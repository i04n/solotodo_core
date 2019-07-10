import csv
import io

from django.contrib.auth.models import Group
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models, connections
from django.db.models import Max
from django_redshift_backend.distkey import DistKey
from guardian.shortcuts import get_objects_for_group

from solotodo.models import Product
from solotodo_core.s3utils import PrivateSaS3Boto3Storage


class LgRsEntityHistory(models.Model):
    entity_history_id = models.IntegerField()
    entity_id = models.IntegerField()
    timestamp = models.DateTimeField()
    normal_price = models.DecimalField(decimal_places=2, max_digits=12)
    offer_price = models.DecimalField(decimal_places=2, max_digits=12)
    picture_count = models.IntegerField(null=True, blank=True)
    video_count = models.IntegerField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    review_avg_score = models.FloatField(null=True, blank=True)
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=256)
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=256)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=256)
    brand_id = models.IntegerField()
    brand_name = models.CharField(max_length=256)
    is_active = models.BooleanField()
    sku = models.CharField(max_length=256, blank=True, null=True)
    sku_url = models.URLField(max_length=512)
    sku_name = models.CharField(max_length=256, blank=True, null=True)
    cell_plan_id = models.IntegerField(blank=True, null=True)
    cell_plan_name = models.CharField(blank=True, null=True, max_length=256)

    def str(self):
        return self.id

    @classmethod
    def synchronize_with_db_entity_histories(cls):
        from solotodo.models import Store, Category, EntityHistory

        from django.conf import settings
        lg_group = Group.objects.get(pk=settings.LG_CHILE_GROUP_ID)

        stores = get_objects_for_group(lg_group, 'view_store', Store)
        categories = get_objects_for_group(lg_group, 'view_category', Category)

        histories_to_synchronize = EntityHistory.objects.filter(
            cell_monthly_payment__isnull=True,
            entity__store__in=stores,
            entity__category__in=categories,
            entity__product__isnull=False,
        ).get_available().select_related(
            'entity__category',
            'entity__store',
            'entity__product__instance_model',
            'entity__product__brand'
        ).order_by('timestamp')

        last_synchronization = cls.objects.aggregate(Max(
            'timestamp'))['timestamp__max']

        if last_synchronization:
            print('Synchronizing since {}'.format(last_synchronization))
            histories_to_synchronize = histories_to_synchronize.filter(
                entity_history__timestamp__gt=last_synchronization
            )
        else:
            print('Synchronizing from scratch')

        print('Creating CSV File')
        csv_file = open('lg_pricing/entity_histories.csv', 'w', newline='')
        writer = csv.writer(csv_file)

        print('Obtaining data')

        products_to_synchronize = Product.objects.filter_by_category(
            categories)
        products_count = len(products_to_synchronize)

        for idx, product in enumerate(products_to_synchronize):
            print('Processing product: {} / {}'.format(
                idx + 1, products_count))

            product_entities = histories_to_synchronize.filter(
                entity__product=product
            )
            entity_count = len(product_entities)

            for idx2, entity_history in enumerate(product_entities):
                print('Processing: {} / {}'.format(idx2 + 1, entity_count))

                if entity_history.entity.cell_plan:
                    cell_plan_name = str(entity_history.entity.cell_plan)
                else:
                    cell_plan_name = None

                writer.writerow([
                    entity_history.id,
                    entity_history.entity.id,
                    entity_history.timestamp,
                    entity_history.normal_price,
                    entity_history.offer_price,
                    entity_history.picture_count,
                    entity_history.video_count,
                    entity_history.review_count,
                    entity_history.review_avg_score,
                    entity_history.entity.store.id,
                    str(entity_history.entity.store),
                    entity_history.entity.category.id,
                    str(entity_history.entity.category),
                    entity_history.entity.product.id,
                    str(entity_history.entity.product),
                    entity_history.entity.product.brand.id,
                    str(entity_history.entity.product.brand),
                    entity_history.entity.active_registry_id ==
                    entity_history.id,
                    entity_history.entity.sku,
                    entity_history.entity.url,
                    entity_history.entity.name,
                    entity_history.entity.cell_plan_id,
                    cell_plan_name,
                ])

        csv_file.close()

        # csv_file.seek(0)
        # import ipdb
        # ipdb.set_trace()
        # django_file = ContentFile(csv_file)
        #
        # print('Uploading CSV file')
        #
        # storage = PrivateSaS3Boto3Storage()
        # storage.file_overwrite = True
        # path = 'lg_pricing/entity_histories.csv'
        # import ipdb
        # ipdb.set_trace()
        # storage.save(path, django_file)
        #
        # import ipdb
        # ipdb.set_trace()
        #
        # file.close()
        #
        # return
        #
        # print('Loading new data into Redshift')
        #
        # cursor = connections['lg_pricing'].cursor()
        # command = """
        #             copy {} from 's3://{}/{}'
        #             credentials 'aws_access_key_id={};aws_secret_access_key={}'
        #             csv;
        #             """.format(
        #     cls._meta.db_table,
        #     settings.AWS_SA_STORAGE_BUCKET_NAME,
        #     path,
        #     settings.AWS_ACCESS_KEY_ID,
        #     settings.AWS_SECRET_ACCESS_KEY
        # )
        #
        # cursor.execute(command)
        # cursor.close()

    class Meta:
        app_label = 'lg_pricing'
        indexes = [DistKey(fields=['product_id'])]
        ordering = ['timestamp']