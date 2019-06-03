import io
import xlsxwriter
from datetime import timedelta

from django import forms
from django.core.files.base import ContentFile
from django.db.models import Count
from django.db.models.functions import ExtractWeek, ExtractYear
from guardian.shortcuts import get_objects_for_user

from solotodo.filter_utils import IsoDateTimeRangeField
from solotodo.models import Category, Brand, EntitySectionPosition, \
    StoreSection
from solotodo_core.s3utils import PrivateS3Boto3Storage


class StoreHistoricEntityPositionsForm(forms.Form):
    timestamp = IsoDateTimeRangeField()
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False
    )
    position_threshold = forms.IntegerField(
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        valid_categories = get_objects_for_user(
            user, 'view_category_entity_positions', Category)
        self.fields['categories'].queryset = valid_categories

    def clean_categories(self):
        selected_categories = self.cleaned_data['categories']
        if selected_categories:
            return selected_categories
        else:
            return self.fields['categories'].queryset

    def generate_report(self, store):
        categories = self.cleaned_data['categories']
        brands = self.cleaned_data['brands']
        timestamp = self.cleaned_data['timestamp']
        position_threshold = self.cleaned_data['position_threshold']

        entity_section_positions = EntitySectionPosition.objects.filter(
            entity_history__entity__category__in=categories,
            entity_history__entity__store=store,
            entity_history__entity__product__isnull=False,
            entity_history__timestamp__gte=timestamp.start,
            entity_history__timestamp__lte=timestamp.stop
        ).select_related(
            'section__store',
            'entity_history__entity__product__brand',
            'entity_history__entity__product__instance_model',
            'entity_history__entity__category',
            'entity_history__entity__store',
        ).annotate(
            week=ExtractWeek('entity_history__timestamp'),
            year=ExtractYear('entity_history__timestamp')
        )

        if position_threshold:
            entity_section_positions = entity_section_positions.filter(
                value__lte=position_threshold
            )

        relevant_sections = entity_section_positions \
            .order_by('section') \
            .values('section')

        categories_in_report = Category.objects.filter(pk__in=[
            e['entity_history__entity__category'] for e in
            entity_section_positions
            .order_by('entity_history__entity__category')
            .values('entity_history__entity__category')
        ])

        section_year_week_category_raw_data = entity_section_positions \
            .order_by(
                'section', 'year', 'week',
                'entity_history__entity__category') \
            .values(
                'section', 'year', 'week',
                'entity_history__entity__category') \
            .annotate(c=Count('*'))

        section_year_week_category_data = {
            (e['section'], '{}-{}'.format(e['year'], e['week']),
             e['entity_history__entity__category']): e['c']
            for e in section_year_week_category_raw_data
        }

        year_week_category_raw_data = entity_section_positions \
            .order_by(
                'year', 'week',
                'entity_history__entity__category') \
            .values(
                'year', 'week',
                'entity_history__entity__category') \
            .annotate(c=Count('*'))

        year_week_category_data = {
            ('{}-{}'.format(e['year'], e['week']),
             e['entity_history__entity__category']): e['c']
            for e in year_week_category_raw_data
        }

        if brands:
            entity_section_positions = entity_section_positions.filter(
                entity_history__entity__product__brand__in=brands
            )

        section_year_week_category_brand_raw_data = entity_section_positions \
            .order_by(
                'section', 'year', 'week',
                'entity_history__entity__category',
                'entity_history__entity__product__brand') \
            .values(
                'section', 'year', 'week',
                'entity_history__entity__category',
                'entity_history__entity__product__brand') \
            .annotate(
                c=Count('*'))

        section_year_week_category_brand_data = {
            (e['section'], '{}-{}'.format(e['year'], e['week']),
             e['entity_history__entity__category'],
             e['entity_history__entity__product__brand']): e['c']
            for e in section_year_week_category_brand_raw_data
        }

        year_week_category_brand_raw_data = entity_section_positions \
            .order_by(
                'year', 'week',
                'entity_history__entity__category',
                'entity_history__entity__product__brand') \
            .values(
                'year', 'week',
                'entity_history__entity__category',
                'entity_history__entity__product__brand') \
            .annotate(
                c=Count('*'))

        year_week_category_brand_data = {
            ('{}-{}'.format(e['year'], e['week']),
             e['entity_history__entity__category'],
             e['entity_history__entity__product__brand']): e['c']
            for e in year_week_category_brand_raw_data
        }

        iter_date = timestamp.start
        one_week = timedelta(days=7)
        end_year, end_week = timestamp.stop.isocalendar()[:2]
        year_weeks = []

        while True:
            year, week = iter_date.isocalendar()[:2]
            year_weeks.append('{}-{}'.format(year, week))

            if year == end_year and week == end_week:
                break

            iter_date += one_week

        # # # REPORT # # #
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output)
        workbook.formats[0].set_font_size(10)

        header_format = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter'
        })

        percentage_format = workbook.add_format()
        percentage_format.set_num_format('0.00%')
        percentage_format.set_font_size(10)

        percentage_bold_format = workbook.add_format()
        percentage_bold_format.set_num_format('0.00%')
        percentage_bold_format.set_font_size(10)
        percentage_bold_format.set_bold(True)

        # # # 1st WORKSHEET # # #
        for category in categories_in_report:
            entity_section_positions_in_category = entity_section_positions \
                .filter(entity_history__entity__category=category)

            sections_in_category = StoreSection.objects.filter(
                pk__in=[e['section'] for e in relevant_sections
                        .filter(entity_history__entity__category=category)]) \
                .select_related('store')

            if brands:
                brands_in_category = brands
            else:
                brands_in_category = Brand.objects.filter(
                    pk__in=[e['entity_history__entity__product__brand']
                            for e in entity_section_positions_in_category
                            .order_by('entity_history__entity__product__brand')
                            .values('entity_history__entity__product__brand')])

            worksheet = workbook.add_worksheet()
            worksheet.name = category.name

            headers = [
                'Tienda',
                'Sección'
            ]

            for year_week in year_weeks:
                headers.extend([str(brand) for brand in brands_in_category])

            for idx, header in enumerate(headers):
                worksheet.write(1, idx, header, header_format)

            row = 2

            for section in sections_in_category:
                col = 0
                worksheet.write(row, col, str(section.store))

                col += 1
                worksheet.write(row, col, section.name)

                for year_week in year_weeks:
                    worksheet.merge_range(
                        0, col+1,
                        0, col+len(brands_in_category),
                        year_week,
                        header_format)

                    for brand in brands_in_category:
                        col += 1
                        value = section_year_week_category_brand_data.get(
                            (section.id, year_week, category.id, brand.id), 0)
                        total = section_year_week_category_data.get(
                            (section.id, year_week, category.id), 1)

                        worksheet.write(row, col, value/total,
                                        percentage_format)
                row += 1

            col = 1
            for year_week in year_weeks:
                for brand in brands_in_category:
                    col += 1
                    value = year_week_category_brand_data.get(
                        (year_week, category.id, brand.id), 0)
                    total = year_week_category_data.get(
                        (year_week, category.id), 1)

                    worksheet.write(row, col, value / total,
                                    percentage_bold_format)

        workbook.close()
        output.seek(0)
        file_value = output.getvalue()
        file_for_upload = ContentFile(file_value)
        storage = PrivateS3Boto3Storage()
        filename = 'historic_sku_positions.xlsx'
        path = storage.save(filename, file_for_upload)

        return {
            'file': file_value,
            'path': path
        }