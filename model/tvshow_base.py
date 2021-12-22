from datetime import datetime
import locale


class TVShowBase:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        self.__format_str_in = '%Y-%m-%d'
        self.__format_str_out = '%d/%b/%y'

    def _format_date(self, value):
        if value != '':
            date_obj = datetime.strptime(value, self.__format_str_in)
            return date_obj.strftime(self.__format_str_out)
        else:
            return ''
