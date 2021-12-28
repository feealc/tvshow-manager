from datetime import datetime
import locale


class TVShowBase:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR')
        self.__format_str_in = '%Y-%m-%d'
        self.__format_str_out = '%d/%b/%y'

    def format_date(self, value):
        if value != '':
            date_obj = self.__convert_to_date_obj(value=value)
            return date_obj.strftime(self.__format_str_out)
        else:
            return ''

    def is_episode_air_date_valid(self, value):
        if value != '':
            date_obj = self.__convert_to_date_obj(value=value)
            if date_obj <= datetime.now():
                return True
            else:
                return False
        else:
            return False

    def __convert_to_date_obj(self, value):
        return datetime.strptime(value, self.__format_str_in)
