from rest_framework import serializers

from metamodel.models import MetaModel, MetaField, InstanceModel, InstanceField


class MetaModelWithoutFieldsSerializer(serializers.HyperlinkedModelSerializer):
    is_primitive = serializers.BooleanField('is_primitive')

    class Meta:
        model = MetaModel
        fields = ['url', 'is_primitive', 'id', 'name', 'unicode_template',
                  'ordering_field']


class MetaFieldSerializer(serializers.HyperlinkedModelSerializer):
    model = MetaModelWithoutFieldsSerializer()

    class Meta:
        model = MetaField
        fields = ['url', 'id', 'name', 'ordering', 'nullable',
                  'multiple', 'hidden', 'model']


class MetaModelAddFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaField
        fields = ['parent', 'name', 'ordering', 'nullable',
                  'multiple', 'hidden', 'model']


class MetaModelSerializer(serializers.HyperlinkedModelSerializer):
    fields = MetaFieldSerializer(many=True)

    class Meta:
        model = MetaModel
        fields = [
            'url', 'id', 'name', 'unicode_template', 'ordering_field',
            'fields']


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstanceModel
        fields = ['id', 'url', 'decimal_value', 'unicode_value',
                  'unicode_representation']


class InstanceFieldSerializer(serializers.HyperlinkedModelSerializer):
    parent = InstanceSerializer()
    field = MetaFieldSerializer()
    value = InstanceSerializer()

    class Meta:
        model = InstanceField
        fields = ['parent','field', 'value']
