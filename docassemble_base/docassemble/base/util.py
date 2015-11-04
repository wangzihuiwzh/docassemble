# -*- coding: utf-8 -*-
import types
import en
import re
import os
import mimetypes
import datetime
import locale
import pkg_resources
from titlecase import titlecase
#from docassemble.base.logger import logmessage
import babel.dates
import locale
import threading
locale.setlocale(locale.LC_ALL, '')

__all__ = ['ordinal', 'comma_list', 'words', 'word', 'get_language', 'set_language', 'get_locale', 'comma_and_list', 'need', 'possessify', 'possessify_long', 'nice_number', 'pickleable_objects', 'in_the', 'a_in_the_b', 'of_the', 'the', 'your', 'his', 'her', 'currency_symbol', 'verb_past', 'verb_present', 'noun_plural', 'indefinite_article', 'do_you', 'does_a_b', 'capitalize', 'underscore_to_space', 'space_to_underscore', 'force_ask', 'period_list', 'currency', 'static_image', 'titlecase', 'url_of']

default_language = 'en'
default_locale = 'US.utf8'

class ThreadVariables(threading.local):
    language = default_language
    this_locale = default_locale
    initialized = False
    def __init__(self, **kw):
        if self.initialized:
            raise SystemError('__init__ called too many times')
        self.initialized = True
        self.__dict__.update(kw)

this_thread = ThreadVariables()

word_collection = {
    'es': {
        'Continue': 'Continuar',
        'Help': 'Ayuda',
        'Sign in': 'Registrarse',
        'Question': 'Interrogación',
        'save_as_multiple': 'The document is available in the following formats:',
        'save_as_singular': 'The document is available in the following format:',
        'pdf_message': 'for printing; requires Adobe Reader or similar application',
        'rtf_message': 'for editing; requires Microsoft Word, Wordpad, or similar application',
        'tex_message': 'for debugging PDF output',
        'attachment_message_plural': 'The following documents have been created for you.',
        'attachment_message_singular': 'The following document has been created for you.'
        },
    'en': {
        'and': "and",
        'or': "or",
        'yes': "yes",
        'no': "no",
        'Document': "Document",
        'content': 'content',
        'Open as:': 'Open this document as:',
        'Open as:': 'Save this documents as:',
        'Question': 'Question',
        'Help': 'Help',
        'Download': 'Download',
        'Preview': 'Preview',
        'Markdown': 'Markdown',
        'Source': 'Source',
        'attachment_message_plural': 'The following documents have been created for you.',
        'attachment_message_singular': 'The following document has been created for you.',
        'save_as_multiple': 'The document is available in the following formats:',
        'save_as_singular': 'The document is available in the following format:',
        'pdf_message': 'for printing; requires Adobe Reader or similar application',
        'rtf_message': 'for editing; requires Microsoft Word, Wordpad, or similar application',
        'tex_message': 'for debugging PDF output',
        'vs.': 'vs.',
        'v.': 'v.',
        'Case No.': 'Case No.',
        'In the': 'In the',
        'This field is required.': 'You need to fill this in.',
        "You need to enter a valid date.": "You need to enter a valid date.",
        "You need to enter a complete e-mail address.": "You need to enter a complete e-mail address.",
        "You need to enter a number.": "You need to enter a number.",
        "You need to select one.": "You need to select one.",
        "Country Code": 'Country Code (e.g., "us")',
        "First Subdivision": "State Abbreviation (e.g., 'NY')",
        "Second Subdivision": "County",
        "Third Subdivision": "Municipality",
        "Organization": "Organization",
    }
}

ordinal_numbers = {
    '0': 'zeroeth',
    '1': 'first',
    '2': 'second',
    '3': 'third',
    '4': 'fourth',
    '5': 'fifth',
    '6': 'sixth',
    '7': 'seventh',
    '8': 'eighth',
    '9': 'ninth',
    '10': 'tenth'
}

nice_numbers = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '10': 'ten'
}

def basic_url_of(text):
    return text

url_of = basic_url_of

def set_url_finder(func):
    global url_of
    url_of = func
    return

def ordinal(j):
    i = j + 1
    num = unicode(i)
    if num in ordinal_numbers:
        return ordinal_numbers[num]
    if 10 <= i % 100 <= 20:
        return num + 'th'
    elif i % 10 == 3:
        return num + 'rd'
    elif i % 10 == 1:
        return num + 'st'
    elif i % 10 == 2:
        return num + 'nd'
    else:
        return num + 'th'

def comma_list(*argv):
    return ", ".join(map(str, argv))

def words():
    return word_collection[this_thread.language]

def word(theword):
    try:
        return word_collection[this_thread.language][theword].decode('utf-8')
    except:
        return theword

def update_word_collection(lang, defs):
    if lang not in word_collection:
        word_collection[lang] = dict()
    for word, translation in defs:
        word_collection[lang][word] = translation
    return

def set_default_language(lang):
    global default_language
    default_language = lang
    return

def reset_language_locale():
    this_thread.language = default_language
    this_thread.locale = default_locale
    return

def set_language(lang):
    this_thread.language = lang
    return

def get_language():
    return this_thread.language

def set_default_locale(loc):
    global default_locale
    default_locale = loc
    return

def set_locale(loc):
    this_thread.this_locale = loc
    return

def get_locale():
    return this_thread.this_locale

def update_locale():
    #logmessage("Using " + str(language) + '_' + str(this_locale) + "\n")
    locale.setlocale(locale.LC_ALL, str(this_thread.language) + '_' + str(this_thread.this_locale))
    return

def comma_and_list(*pargs, **kargs):
    if 'oxford' in kargs and kargs['oxford'] == False:
        extracomma = ""
    else:
        extracomma = ","
    if 'and_string' in kargs:
        and_string = kargs['and_string']
    else:
        and_string = word('and')
    if 'comma_string' in kargs:
        comma_string = kargs['comma_string']
    else:
        comma_string = ", "
    if 'before_and' in kargs:
        before_and = kargs['before_and']
    else:
        before_and = " "
    if 'after_and' in kargs:
        after_and = kargs['after_and']
    else:
        after_and = " "
    if (len(pargs) == 0):
        return
    elif (len(pargs) == 1):
        if type(pargs[0]) == list:
            pargs = pargs[0]
    if (len(pargs) == 0):
        return
    elif (len(pargs) == 1):
        return(unicode(pargs[0]))
    elif (len(pargs) == 2):
        return(unicode(pargs[0]) + before_and + and_string + after_and + unicode(pargs[1]))
    else:
        return(comma_string.join(map(unicode, pargs[:-1])) + extracomma + before_and + and_string + after_and + unicode(pargs[-1]))

def need(*pargs):
    for argument in pargs:
        argument
    return True

def possessify(theword, target):
    #language-specific methods can go here
    return unicode(theword) + "'s " + unicode(target)

def possessify_long(word, target):
    #language-specific methods can go here
    return the(target) + " " + of_the(word)

def nice_number(num):
    if unicode(num) in nice_numbers:
        return nice_numbers[unicode(num)]
    return unicode(num)

def pickleable_objects(input_dict):
    output_dict = dict()
    for key in input_dict:
        if type(input_dict[key]) in [types.ModuleType, types.FunctionType, types.TypeType]:
            continue
        if key == "__builtins__":
            continue
        output_dict[key] = input_dict[key]
    return(output_dict)

def in_the(a):
    #language-specific methods can go here
    return 'in ' + unicode(a)

def a_in_the_b(a, b):
    #language-specific methods can go here
    return unicode(a) + ' in the ' + unicode(b)

def of_the(a):
    #language-specific methods can go here
    return 'of the ' + unicode(a)

def the(a):
    #language-specific methods can go here
    return 'the ' + unicode(a)

def your(a):
    #language-specific methods can go here
    return 'your ' + unicode(a)

def his(a):
    #language-specific methods can go here
    return 'his ' + unicode(a)

def her(a):
    #language-specific methods can go here
    return 'her ' + unicode(a)

def currency_symbol():
    #locale-specific methods can go here
    return(locale.localeconv()['currency_symbol'])

def verb_past(the_verb, **kwargs):
    return(en.verb.past(the_verb, **kwargs))

def verb_present(the_verb, **kwargs):
    return(en.verb.present(the_verb, **kwargs))

def noun_plural(the_noun):
    return(en.noun.plural(the_noun))

def indefinite_article(the_noun):
    return(en.noun.article(the_noun))

def do_you(a, **kwargs):
    #logmessage("do_you kwargs are " + unicode(kwargs) + "\n")
    if 'capitalize' in kwargs and kwargs['capitalize']:
        return('Do you ' + unicode(a))
    else:
        return('do you ' + unicode(a))
        
def does_a_b(a, b, **kwargs):
    #logmessage("does_a_b kwargs are " + unicode(kwargs) + "\n")
    if 'capitalize' in kwargs and kwargs['capitalize']:
        return('Does ' + unicode(a) + ' ' + unicode(b))
    else:
        return('does ' + unicode(a) + ' ' + unicode(b))

def today():
    return(babel.dates.format_date(datetime.date.today(), format='long', locale=this_thread.language))
    #return(today.strftime('%x'))
    
def capitalize(a):
    if a and type(a) is str and len(a) > 1:
        return(a[0].upper() + a[1:])
    else:
        return(unicode(a))

def underscore_to_space(a):
    return(re.sub('_', ' ', unicode(a)))

def space_to_underscore(a):
    return(re.sub(' +', '_', unicode(a).encode('ascii', errors='ignore')))

def remove(variable_name):
    try:
        exec('del ' + variable_name)
    except:
        pass

def force_ask(variable_name):
    raise NameError("name '" + variable_name + "' is not defined")

def period_list():
    return([[12, word("Per Month")], [1, word("Per Year")], [52, word("Per Week")], [24, word("Twice Per Month")], [26, word("Every Two Weeks")]])

def currency(value, decimals=True):
    if decimals:
        return(locale.currency(value, symbol=True, grouping=True))
    else:
        return(currency_symbol() + locale.format("%d", value, grouping=True))

def static_filename_path(filereference):
    return(package_data_filename(static_filename(filereference)))

def static_filename(filereference):
    if re.search(r',', filereference):
        return(None)
    parts = filereference.split(':')
    if len(parts) < 2:
        parts = ['docassemble.base', filereference]
    if re.search(r'\.\./', parts[1]):
        return(None)
    if not re.match(r'data/.*', parts[1]):
        parts[1] = 'data/static/' + parts[1]
    return(parts[0] + ':' + parts[1])

def static_image(filereference, **kwargs):
    filename = static_filename(filereference)
    if filename is None:
        return('ERROR: invalid image reference')
    width = kwargs.get('width', None)
    if width is None:
        return('[IMAGE ' + filename + ']')
    else:
        return('[IMAGE ' + filename + ', ' + width + ']')

def standard_template_filename(the_file):
    try:
        return(pkg_resources.resource_filename(pkg_resources.Requirement.parse('docassemble.base'), "docassemble/base/data/templates/" + str(the_file)))
    except:
        #logmessage("Error retrieving data file\n")
        return(None)

def package_template_filename(the_file, **kwargs):
    parts = the_file.split(":")
    if len(parts) == 1:
        package = kwargs.get('package', None)
        if package is not None:
            parts = [package, the_file]
    if len(parts) == 2:
        if not re.match(r'data/.*', parts[1]):
            parts[1] = 'data/templates/' + parts[1]
        try:
            return(pkg_resources.resource_filename(pkg_resources.Requirement.parse(parts[0]), re.sub(r'\.', r'/', parts[0]) + '/' + parts[1]))
        except:
            return(None)
    return(None)

def standard_question_filename(the_file):
    #try:
    return(pkg_resources.resource_filename(pkg_resources.Requirement.parse('docassemble.base'), "docassemble/base/data/questions/" + str(the_file)))
    #except:
    #logmessage("Error retrieving question file\n")
    return(None)

def package_data_filename(the_file):
    if the_file is None:
        return(None)
    parts = the_file.split(":")
    if len(parts) == 2:
        try:
            return(pkg_resources.resource_filename(pkg_resources.Requirement.parse(parts[0]), re.sub(r'\.', r'/', parts[0]) + '/' + parts[1]))
        except:
            return(None)
    return(None)

def package_question_filename(the_file):
    parts = the_file.split(":")
    if len(parts) == 2:
        if not re.match(r'data/.*', parts[1]):
            parts[1] = 'data/question/' + parts[1]
        try:
            return(pkg_resources.resource_filename(pkg_resources.Requirement.parse(parts[0]), re.sub(r'\.', r'/', parts[0]) + '/' + parts[1]))
        except:
            return(None)
    return(None)

def absolute_filename(the_file):
    if os.path.isfile(the_file) and os.access(the_file, os.R_OK):
        return(the_file)
    return(None)

def nodoublequote(text):
    return re.sub(r'"', '', unicode(text))

# def blank_file_finder(*args, **kwargs):
#     return(dict(filename="invalid"))

# file_finder = blank_file_finder

# def set_file_finder(func):
#     global file_finder
#     logmessage("set the file finder to " + str(func) + "\n")
#     file_finder = func
#     return

# def blank_url_finder(*args, **kwargs):
#     return('about:blank')

# url_finder = blank_url_finder

# def set_url_finder(func):
#     global url_finder
#     url_finder = func
#     return
# grep -E -R -o -h "word\(['\"][^\)]+\)" * | sed "s/^[^'\"]+['\"]//g"