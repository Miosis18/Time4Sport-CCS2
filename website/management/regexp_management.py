import re


class RegexpManagement:
    @staticmethod
    def check_phone_number(phone_number):
        phone_regexps = [r"^((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d"
                         r"{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$",
                         r"^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$"]

        match = False if [re.search(regexp, phone_number) for regexp in phone_regexps] == [None, None] else True

        return match
