from bs4 import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter
def markdown_to_plaintext(markdown_string, search_query):
    html = md.markdown(markdown_string)

    soup = BeautifulSoup(html, "html.parser")
    text = '. '.join(soup.stripped_strings)
    sentences = text.split('.')
    return '. '.join(sentence for sentence in sentences if search_query.lower() in sentence.lower())
