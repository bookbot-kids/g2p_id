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


import os
import re
from typing import Any

from num2words import num2words

resources_path = os.path.join(os.path.dirname(__file__), "resources")


class TextProcessor:
    """Indonesian text processor to normalize numerics, currencies, and timezones."""

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
        measurements_path = os.path.join(resources_path, "measurements.tsv")
        currencies_path = os.path.join(resources_path, "currency.tsv")
        timezones_path = os.path.join(resources_path, "timezones.tsv")

        with open(measurements_path, "r", encoding="utf-8") as file:
            for lines in file:
                line = lines.strip().split("\t")
                self.measurements[line[0]] = line[1]

        self.currencies = {}
        with open(currencies_path, "r", encoding="utf-8") as file:
            for lines in file:
                line = lines.strip().split("\t")
                self.currencies[line[0]] = line[1]

        self.timezones = {}
        with open(timezones_path, "r", encoding="utf-8") as file:
            for lines in file:
                line = lines.strip().split("\t")
                self.timezones[line[0]] = line[1]

        self.re_thousands = "|".join(self.thousands)
        self.re_currencies = r"\b" + re.sub(
            r"\|([^|$£€¥₩]+)", r"|\\b\1", "|".join(list(self.currencies))
        )
        self.re_currencies = re.sub(r"([$£€¥₩])", r"\\\1", self.re_currencies)
        self.re_moneys = (
            rf"(({self.re_currencies}) ?([\d\.\,]+)( ({self.re_thousands})?(an)?)?)"
        )
        self.re_measurements = "|".join(list(self.measurements))
        self.re_measurements = rf"(\b([\d\.\,]+) ?({self.re_measurements})\b)"
        self.re_timezones = "|".join(list(self.timezones))
        self.re_timezones = (
            r"((\d{1,2})[\.:](\d{1,2}) " + rf"\b({self.re_timezones})\b)"
        )
        self.re_http = re.compile(
            r"""
            (https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.
            [a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)
            """,
            re.X,
        )

    @staticmethod
    def is_integer(number: Any) -> bool:
        """Check if integer by type-casting.

        Args:
            number (Any): Number to check.

        Returns:
            bool: Is a valid integer.
        """
        try:
            int(number)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(number: Any) -> bool:
        """Check if float by type-casting.

        Args:
            number (Any): Number to check.

        Returns:
            bool: Is a valid float.
        """
        try:
            float(number)
            return True
        except ValueError:
            return False

    def normalize_url(self, text: str) -> str:
        """Removes URL from text.

        Args:
            text (str): Text with URL to normalize.

        Returns:
            str: Normalized text with URLs removed.
        """
        urls = re.findall(self.re_http, text)
        for url in urls:
            text = text.replace(url[0], "")
        return text

    def normalize_currency(self, text: str) -> str:
        """Normalizes international and Indonesian (Rupiah) currencies.

        Examples:
        - `"$250"` -> `"dua ratus lima puluh dollar"`
        - `"Rp 3,000,000"` -> `"tiga juta rupiah"`

        Args:
            text (str): Text with currency to normalize.

        Returns:
            str: Normalized text with currency transliterated.
        """
        moneys = re.findall(self.re_moneys, text)
        for money in moneys:
            number: Any = re.sub(",", ".", re.sub(r"\.", "", money[2].strip(" ,.")))
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
            except NotImplementedError as error:
                print(error)
                print(f"Problem with money: <{text}>: {number}")
        return text

    def normalize_measurement(self, text: str) -> str:
        """Normalizes measurement units, including its scalar value.

        Examples:
        - `"10,5 km"` -> `"sepuluh koma lima kilometer"`
        - `"5°C"` -> `"lima derajat celsius"`

        Args:
            text (str): Text with measurements to normalize.

        Returns:
            str: Normalized text with measurements transliterated.
        """
        units = re.findall(self.re_measurements, text)
        for unit in units:
            number: Any = re.sub(",", ".", re.sub(r"\.", "", unit[1].strip(" ,.")))
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
            except NotImplementedError as error:
                print(error)
                print(f"Problem with measurements: <{text}>: {number}")
        return text

    def normalize_date(self, text: str) -> str:
        """Normalizes dates.

        Examples:
        - `"(12/3/2021)"` -> `"dua belas Maret dua ribu dua puluh satu"`

        Args:
            text (str): Text with dates to normalize.

        Returns:
            str: Normalized text with dates transliterated.
        """
        dates = re.findall(r"(\((\d{1,2})/(\d{1,2})(/(\d+))?\))", text)
        for date in dates:
            try:
                day = num2words(int(date[1]), to="cardinal", lang="id")
                month: Any = int(date[2]) - 1
                if month >= 12:
                    month = 0
                month = self.months[month]
                if date[4] != "":
                    year = num2words(int(date[4]), to="cardinal", lang="id")
                    date_string = f"{day} {month} {year}"
                else:
                    date_string = f"{day} {month}"
                text = text.replace(date[0], f" {date_string} ")
            except NotImplementedError as error:
                print(error)
                print(f"Problem with dates: <{text}>: {date}")
        return text

    def normalize_timezone(self, text: str) -> str:
        """Normalizes Indonesian time with timezones.

        Examples:
        - `"22.30 WITA"`
            -> `"dua puluh dua lewat tiga puluh menit Waktu Indonesia Tengah"`

        Args:
            text (str): Text with timezones to normalize.

        Returns:
            str: Normalized text with timezones transliterated.
        """
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
            except NotImplementedError as error:
                print(error)
                print(f"Problem with timezones: <{text}>: {timezone}")
        return text

    def normalize_number(self, text: str) -> str:
        """Normalizes Arabic numbers to Indonesian.

        Examples:
        - `"1.000"` -> `"seribu"`
        - `"10,5"` -> `"sepuluh koma lima"`

        Args:
            text (str): Text with numbers to normalize.

        Returns:
            str: Normalized text with numbers transliterated.
        """
        re_numbers = [r"([\d.,]+)", r"\d+"]
        for re_number in re_numbers:
            number_len = 0
            for i in re.finditer(re_number, text):
                start = i.start() + number_len
                end = i.end() + number_len
                number: Any = text[start:end]
                number = re.sub(",", ".", re.sub(r"\.", "", number.strip(" ,.")))
                if number == "":
                    continue
                if self.is_float(number) or self.is_integer(number):
                    try:
                        if self.is_integer(number):
                            number = int(number)
                        else:
                            number = float(number)
                        number = num2words(number, to="cardinal", lang="id")
                        text = text[:start] + number + text[end:]
                        number_len += len(number) - (end - start)
                    except NotImplementedError as error:
                        print(error)
                        print(f"Problem with number: <{text}>: {number}")
        return text

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
        # Remove URL
        text = self.normalize_url(text)
        # Currency
        text = self.normalize_currency(text)
        # Measurements
        text = self.normalize_measurement(text)
        # Date
        text = self.normalize_date(text)
        # Timezones
        text = self.normalize_timezone(text)
        # Any number
        text = self.normalize_number(text)
        # collapse consecutive whitespaces
        text = re.sub(r"\s+", " ", text)
        return text
