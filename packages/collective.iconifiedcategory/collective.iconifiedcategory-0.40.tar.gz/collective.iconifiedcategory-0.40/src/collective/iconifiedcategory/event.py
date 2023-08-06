# -*- coding: utf-8 -*-
"""
collective.iconifiedcategory
----------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from collective.iconifiedcategory.interfaces import ICategorizedElementsUpdatedEvent
from collective.iconifiedcategory.interfaces import IIconifiedCategoryChangedEvent
from collective.iconifiedcategory.interfaces import IIconifiedConfidentialChangedEvent
from collective.iconifiedcategory.interfaces import IIconifiedModifiedEvent
from collective.iconifiedcategory.interfaces import IIconifiedPrintChangedEvent
from collective.iconifiedcategory.interfaces import IIconifiedPublishableChangedEvent
from collective.iconifiedcategory.interfaces import IIconifiedSignedChangedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class IconifiedChangedEvent(ObjectEvent):

    def __init__(self, object, old_values, new_values):
        super(IconifiedChangedEvent, self).__init__(object)
        self.old_values = old_values
        self.new_values = new_values


class IconifiedModifiedEvent(ObjectEvent):
    implements(IIconifiedModifiedEvent)


class IconifiedCategoryChangedEvent(ObjectEvent):
    implements(IIconifiedCategoryChangedEvent)

    def __init__(self, object, sort=False):
        super(IconifiedCategoryChangedEvent, self).__init__(object)
        self.sort = sort


class IconifiedPrintChangedEvent(IconifiedChangedEvent):
    implements(IIconifiedPrintChangedEvent)


class IconifiedConfidentialChangedEvent(IconifiedChangedEvent):
    implements(IIconifiedConfidentialChangedEvent)


class IconifiedSignedChangedEvent(IconifiedChangedEvent):
    implements(IIconifiedSignedChangedEvent)


class IconifiedPublishableChangedEvent(IconifiedChangedEvent):
    implements(IIconifiedPublishableChangedEvent)


class CategorizedElementsUpdatedEvent(ObjectEvent):
    implements(ICategorizedElementsUpdatedEvent)
