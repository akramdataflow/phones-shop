# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from django.utils.dateformat import DateFormat

from .boolean import is_date
from dateutil.parser import parse
import re
import string
import random


def timestamp2datetime(timestamp):
    return timezone.datetime.fromtimestamp(float(timestamp) / 1000.0)


def readable_date_format(datetime):
    return DateFormat(datetime).format("d F Y H:i")


def get_client_ip(request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def str2date(date_string, lang="en"):
    lang_day_first = {
        "en": False,
        "tr": True,
        "ar": False,
    }
    return timezone.make_aware(parse(date_string, dayfirst=lang_day_first[lang])) if is_date(
        date_string) else timezone.now()


def paginate(objects, per_page=24, page=1):
    paginator = Paginator(objects, per_page)
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects


# def remove_xss_from_html(html):
#     " prevent Cross-site scripting attack "
#     from lxml.html.clean import clean_html
#     return clean_html(html) if isinstance(html, str) and html else ""


def remove_html_tags(html):
    return re.sub(re.compile('<.*?>'), '', html) if isinstance(html, str) and html else ""


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    if not terms:
        query = Q(**{"%s__icontains" % search_fields[0]: ""})
    return query


def display_form_validations(form, request, message_type=messages.ERROR):
    for field_name, errors in form.errors.items():
        field = form.fields.get(field_name)
        field_name = field.label if field else field_name
        messages.add_message(request, message_type, "<b>{}</b>: {}".format(field_name, ", ".join(errors)))


def shortenLargeNumber(num, digits=1):
    units = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    for i in range(len(units) - 1, -1, -1):
        decimal = 1000 ** (i + 1)
        if abs(num) >= decimal:
            return "{}{}".format(round(num / decimal, digits), units[i])
    return str(num)


def password_generator(size=8, chars=string.ascii_letters + string.digits):
    """
    Returns a string of random characters, useful in generating temporary
    passwords for automated password resets.

    size: default=8; override to provide smaller/larger passwords
    chars: default=A-Za-z0-9; override to provide more/less diversity

    Credit: Ignacio Vasquez-Abrams
    Source: http://stackoverflow.com/a/2257449
    """
    return ''.join(random.choice(chars) for i in range(size))


def get_channel_group_name(user=None):
    if user:
        return password_generator(size=10)
    return False
