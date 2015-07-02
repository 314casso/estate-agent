# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand 
from django.db.models.loading import get_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 2:
            print u'Specify app_label and model_name... estatebase layoutfeature'
            return
        model = get_model(args[0],args[1])
        if not model:
            return        
        for st in model.objects.all().order_by('name'):
            result = '%s = %s' % (transliterate(st.name), st.pk)
            print result.upper()
             

_capital_letters = {
    u'А': u'A',
    u'Б': u'B',
    u'В': u'V',
    u'Г': u'G',
    u'Д': u'D',
    u'Е': u'E',
    u'Ё': u'E',
    u'Ж': u'Zh',
    u'З': u'Z',
    u'И': u'I',
    u'Й': u'Y',
    u'К': u'K',
    u'Л': u'L',
    u'М': u'M',
    u'Н': u'N',
    u'О': u'O',
    u'П': u'P',
    u'Р': u'R',
    u'С': u'S',
    u'Т': u'T',
    u'У': u'U',
    u'Ф': u'F',
    u'Х': u'H',
    u'Ц': u'Ts',
    u'Ч': u'Ch',
    u'Ш': u'Sh',
    u'Щ': u'Sch',
    u'Ъ': u'',
    u'Ы': u'Y',
    u'Ь': u'',
    u'Э': u'E',
    u'Ю': u'Yu',
    u'Я': u'Ya',}

_lower_case_letters = {
    u'а': u'a',
    u'б': u'b',
    u'в': u'v',
    u'г': u'g',
    u'д': u'd',
    u'е': u'e',
    u'ё': u'e',
    u'ж': u'zh',
    u'з': u'z',
    u'и': u'i',
    u'й': u'y',
    u'к': u'k',
    u'л': u'l',
    u'м': u'm',
    u'н': u'n',
    u'о': u'o',
    u'п': u'p',
    u'р': u'r',
    u'с': u's',
    u'т': u't',
    u'у': u'u',
    u'ф': u'f',
    u'х': u'h',
    u'ц': u'ts',
    u'ч': u'ch',
    u'ш': u'sh',
    u'щ': u'sch',
    u'ъ': u'',
    u'ы': u'y',
    u'ь': u'',
    u'э': u'e',
    u'ю': u'yu',
    u'я': u'ya',}

def transliterate(string):
    capital_letters = _capital_letters
    lower_case_letters = _lower_case_letters
    len_str = len(string)
    translit_string = u""
    for index, char in enumerate(string, 1):
        repl = lower_case_letters.get(char)
        if repl:
            translit_string += repl
            continue
        repl = capital_letters.get(char)
        if repl:
            if len_str > index:
                if string[index] not in lower_case_letters:
                    repl = repl.upper()
            else:
                repl = repl.upper()
        else:
            repl = ''
        translit_string += repl
    return translit_string 