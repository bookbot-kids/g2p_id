"""
MIT License

Copyright (c) 2021 Cahya Wirawan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import re
from num2words import num2words
import os

resources_path = os.path.join(os.path.dirname(__file__), "resources")


class TextProcessor:
    def __init__(self):
        self.measurements = {}
        self.thousands = ["ratus", "ribu", "juta", "miliar", "milyar", "triliun"]
        self.months = [
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
        ]
        self.measurements_path = os.path.join(resources_path, "measurements.tsv")
        self.currencies_path = os.path.join(resources_path, "currency.tsv")
        self.timezones_path = os.path.join(resources_path, "timezones.tsv")

        with open(self.measurements_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.measurements[line[0]] = line[1]

        self.currencies = {}
        with open(self.currencies_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.currencies[line[0]] = line[1]

        self.timezones = {}
        with open(self.timezones_path, "r") as file:
            for line in file:
                line = line.strip().split("\t")
                self.timezones[line[0]] = line[1]

        self.re_thousands = "|".join([t for t in self.thousands])
        self.re_currencies = r"\b" + re.sub(
            r"\|([^|$£€¥₩]+)", r"|\\b\1", "|".join([c for c in self.currencies])
        )
        self.re_currencies = re.sub(r"([$£€¥₩])", r"\\\1", self.re_currencies)
        self.re_moneys = r"(({}) ?([\d\.\,]+)( ({})?(an)?)?)".format(
            self.re_currencies, self.re_thousands
        )
        self.re_measurements = "|".join([t for t in self.measurements])
        self.re_measurements = r"(\b([\d\.\,]+) ?({})\b)".format(self.re_measurements)
        self.re_timezones = "|".join([c for c in self.timezones])
        self.re_timezones = r"((\d{1,2})[\.:](\d{1,2}) " + r"\b({})\b)".format(
            self.re_timezones
        )
        self.re_http = r"(https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

    @staticmethod
    def is_integer(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def normalize(self, text: str) -> str:
        """Normalizes Indonesian text by expanding:
        
        - URL
        - Currency
        - Measurements
        - Dates
        - Timezones
        - Arabic Numerals

        Args:
            text (str): Text to normalize.

        Returns:
            str: Normalized text.
        """
        found_errors = False
        # Remove URL
        urls = re.findall(self.re_http, text)
        for url in urls:
            text = text.replace(url[0], "")

        # Currency
        moneys = re.findall(self.re_moneys, text)
        for money in moneys:
            number = re.sub(",", ".", re.sub(r"\.", "", money[2].strip(" ,.")))
            try:
                if number == "":
                    continue
                if self.is_integer(number):
                    number = int(number)
                elif self.is_float(number):
                    number = float(number)
                else:
                    number = re.sub(r"[.,]", "", number)
                    number = int(number)
                number = num2words(number, to="cardinal", lang="id")
                text = text.replace(
                    money[0].strip(" ,."),
                    f"{number} {money[3]} {self.currencies[money[1]]}",
                )
            except Exception as error:
                found_errors = True
                print(error)
                print(f"Problem with money: <{text}>: {number}")

        # Measurements
        units = re.findall(self.re_measurements, text)
        for unit in units:
            number = re.sub(",", ".", re.sub(r"\.", "", unit[1].strip(" ,.")))
            try:
                if number == "":
                    continue
                if re.search(r"\.", number):
                    number = float(number)
                else:
                    number = int(number)
                number = num2words(number, to="cardinal", lang="id")
                text = text.replace(
                    unit[0].strip(" ,."), f"{number} {self.measurements[unit[2]]}"
                )
            except Exception as error:
                found_errors = True
                print(error)
                print(f"Problem with measurements: <{text}>: {number}")

        # Date
        dates = re.findall(r"(\((\d{1,2})/(\d{1,2})(/(\d+))?\))", text)
        for date in dates:
            try:
                day = num2words(int(date[1]), to="cardinal", lang="id")
                month = int(date[2]) - 1
                if month >= 12:
                    month = 0
                month = self.months[month]
                if date[4] != "":
                    year = num2words(int(date[4]), to="cardinal", lang="id")
                    date_string = f"{day} {month} {year}"
                else:
                    date_string = f"{day} {month}"
                text = text.replace(date[0], f" {date_string} ")
            except Exception as error:
                found_errors = True
                print(error)
                print(f"Problem with dates: <{text}>: {date}")

        # Timezones
        timezones = re.findall(self.re_timezones, text)
        for timezone in timezones:
            try:
                hour = num2words(int(timezone[1]), to="cardinal", lang="id")
                minute = num2words(int(timezone[2]), to="cardinal", lang="id")
                zone = self.timezones[timezone[3]]
                if minute == "nol":
                    time_string = f"{hour} {zone}"
                else:
                    time_string = f"{hour} lewat {minute} menit {zone}"
                text = text.replace(timezone[0], f"{time_string}")
            except Exception as error:
                found_errors = True
                print(error)
                print(f"Problem with timezones: <{text}>: {timezone}")

        # Any number
        re_numbers = [r"([\d.,]+)", r"\d+"]
        for re_number in re_numbers:
            number_len = 0
            for i in re.finditer(re_number, text):
                start = i.start() + number_len
                end = i.end() + number_len
                number = text[start:end]
                number = re.sub(",", ".", re.sub(r"\.", "", number.strip(" ,.")))
                if number == "":
                    continue
                if self.is_integer(number) or self.is_float(number):
                    try:
                        if self.is_integer(number):
                            number = int(number)
                        else:
                            number = float(number)
                        number = num2words(number, to="cardinal", lang="id")
                        text = text[:start] + number + text[end:]
                        number_len += len(number) - (end - start)
                    except Exception as error:
                        found_errors = True
                        print(error)
                        print(f"Problem with number: <{text}>: {number}")

        text = re.sub(r"\s+", " ", text)
        if found_errors:
            print(f">>> {text}")
        return text
