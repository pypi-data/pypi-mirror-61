"""Mutable BeautifulSoup database type"""

from bs4 import BeautifulSoup
from flask import Markup
from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator, Unicode

from copy import copy


class SoupBase(BeautifulSoup):
    def text(self, selector):
        """Get text from selector. 
        
        Return `None` if the selector does not find an element.
        """
        elem = self.select_one(selector)
        return None if elem is None else elem.text

    def copy(self):
        return copy(self)

    def render(self):
        """Render for insertion into a Jinja template"""
        return Markup(str(self))

    def set_element(
            self, parent_selector, val, target_selector=None, 
            gen_target=None, args=[], kwargs={}
        ):
        """Set a soup element
        
        `parent_selector` selects an ancestor of the target from self. 
        The target is then selected as a descendent of the parent. Its 
        value is set to the input value.
        """
        parent = self.select_one(parent_selector)
        if not val:
            return parent.clear()
        target = self._get_target(
            parent, target_selector, gen_target, args, kwargs
        )
        if type(val) in [str, int, float]:
            val = BeautifulSoup(str(val), 'html.parser')
        target.clear()
        target.append(val)

    def _get_target(self, parent, target_selector, gen_target, args, kwargs):
        """Get target element

        If `target_selector` is None, the target attribute is assumed to be 
        the parent attribute. Otherwise, the target is assumed to be a 
        descendent of the parent. If the target does not yet exist, generate 
        a child Tag which includes the target.
        """
        if target_selector is None:
            return parent
        target = parent.select_one(target_selector)
        if target is not None:
            return target
        parent.append(gen_target(*args, **kwargs))
        return parent.select_one(target_selector)


class MutableSoup(Mutable, SoupBase):
    @classmethod
    def coerce(cls, key, obj):
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, str):
            return cls(obj, 'html.parser')
        if isinstance(obj, BeautifulSoup):
            return cls(str(obj), 'html.parser')
        return super().coerce(key, obj)

    def set_element(self, *args, **kwargs):
        super().set_element(*args, **kwargs)
        self.changed()

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d


class MutableSoupType(TypeDecorator):
    """Mutable Soup database type

    Encode soup as `str` when storing in database; restore `BeautifulSoup` 
    object when accessing from database.
    """
    impl = Unicode

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return None if value is None else BeautifulSoup(value, 'html.parser')


MutableSoup.associate_with(MutableSoupType)