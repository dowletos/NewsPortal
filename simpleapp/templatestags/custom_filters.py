from django import template
import re


register=template.Library()
# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

CURRENCIES_LIST={
    'rub':'P',
    'usd':'$',
}
@register.filter()
def currency(value,code='rub'):
    """
      value: значение, к которому нужно применить фильтр
      """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {CURRENCIES_LIST[code]}'




CENSOR_LIST=(
    'мрак','нечесть','дурь','тест','текст','Заголовок'
)
@register.filter()
def censor(value):
    for censor in CENSOR_LIST:
            compiled = re.compile(re.escape(censor), re.IGNORECASE)
            value=compiled.sub('*' * len(censor), value)
    return f'{value}'