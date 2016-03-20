from django.db import models
from django.db.models import constants
from django.core import urlresolvers

from rest_framework import serializers

from . import fields as api_fields
from .. import fields as model_fields

# Exports.
__all__ = [
    'RegistryRootSerializerMixin',
    'RegistryItemSerializerMixin',
]


class RegistryRootSerializerMixin(object):
    """
    Mixin for serializing registry roots.
    """

    def to_representation(self, instance):
        data = super(RegistryRootSerializerMixin, self).to_representation(instance)

        data['@context'] = {
            '@base': urlresolvers.reverse('apiv2:api-root'),
            # TODO: Replace with actual schema API endpoint.
            '@vocab': 'http://schema.nodewatcher.net/v2/#',
        }

        del data['registry_metadata']

        for field in instance._meta.virtual_fields:
            if not hasattr(field, 'src_model'):
                continue

            def serialize_instance(item):
                if hasattr(field, '_registry_annotations'):
                    for target_attribute, source_attribute in field._registry_annotations.items():
                        setattr(item, target_attribute, getattr(instance, source_attribute))

                return item._registry.serializer_class(item).data

            meta = field.src_model._registry
            value = getattr(instance, field.name)
            namespace = data.setdefault(meta.registration_point.namespace, {})
            if field.src_field:
                atoms = field.src_field.split(constants.LOOKUP_SEP)

                if isinstance(value, models.Manager):
                    base_container = namespace.setdefault(meta.registry_id, [])
                    for index, item in enumerate(value.all()):
                        try:
                            container = base_container[index]
                        except IndexError:
                            container = {}
                            base_container.append(container)

                        container = reduce(lambda a, b: a.setdefault(b, {}), atoms[:-1], container)
                        container[atoms[-1]] = item
                        annotate_instance(meta, base_container[index])
                else:
                    base_container = namespace.setdefault(meta.registry_id, {})
                    container = reduce(lambda a, b: a.setdefault(b, {}), atoms[:-1], base_container)
                    container[atoms[-1]] = value
                    annotate_instance(meta, base_container)
            elif isinstance(value, models.Manager):
                namespace[meta.registry_id] = map(serialize_instance, value.all())
            else:
                namespace[meta.registry_id] = serialize_instance(value)

        return data


class RegistryItemSerializerMixin(object):
    """
    Mixin for serializing registry items.
    """

    def build_relational_field(self, field_name, relation_info):
        if isinstance(relation_info.model_field, model_fields.IntraRegistryForeignKey):
            return (api_fields.IntraRegistryForeignKeyField, {'related_model': relation_info.related_model})

        return super(RegistryItemSerializerMixin, self).build_relational_field(field_name, relation_info)

    def to_representation(self, instance):
        data = super(RegistryItemSerializerMixin, self).to_representation(instance)

        # Remove some internal fields.
        del data['polymorphic_ctype']
        del data['root']
        del data['display_order']
        del data['annotations']

        # Add JSON-LD annotations.
        annotate_instance(instance._registry, data, self)

        return data


def annotate_instance(meta, data, serializer=None):
    if 'id' in data:
        data['@id'] = '_:%s' % meta.get_api_id(data['id'])
        del data['id']

    data['@type'] = meta.get_api_type()
