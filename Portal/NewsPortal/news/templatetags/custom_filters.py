from django import template

register = template.Library()


bad_list = [
    'bad',
    'awful',
    'rude',
    'beats',
]


@register.filter(name='censor')
def censor(value):
    words_list = value.split()
    for index, word in enumerate(words_list):
        if word.lower() in bad_list:
            words_list[index] = "***"
    return " ".join(words_list)