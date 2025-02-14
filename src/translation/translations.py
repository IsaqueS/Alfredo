import asyncio
import csv
import locale
import warnings
import codecs
from model.app_data import AppData
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import flet as ft



# TRANSLATION_PATH: str = (os.environ["FLET_ASSETS_DIR"] + "\\translations\\lang.csv")
DIALECT_OPTION_WARNING: str = """'%s' should be the 'with-dialects' or 'no-dialects' option
For example, the 'with-dialects' options allows to have options like 'en-us' and 'en-au' for translation
Languages dialects are going to be ignored by default
Please check the first value of the 'Lang.csv' translation file'"""
DUPLICATED_LANGUAGES_WARNING: str = "'%s' is duplicated on the %sº column of the 'lang.csv' translation file\nThis column will be ignored"

class Translations:
    def __init__(self, csv_encoding: str = "utf-8") -> None:

        self.__messages:dict[str,str] = {}
        self.__current_language: str = None
        self.__available_languages: dict[str, int] = {}
        self.enable_dialects: bool = False
        self.csv_encoding: str = csv_encoding

        self.system_language: str = locale.getlocale()[0]

        self.csv_path: str = None

    def validade_csv(self) -> None:
        with codecs.open(self.csv_path, mode="r", encoding=self.csv_encoding) as file:
            reader: csv.reader = csv.reader(file)
            header: list[str] = next(reader)

            match header[0]:
                case "key":
                    self.enable_dialects = False
                case "with-dialects":
                    self.enable_dialects = True
                case "no-dialects":
                    self.enable_dialects = False
                case _:
                    self.enable_dialects = False
                    warnings.warn(DIALECT_OPTION_WARNING %header[0])
            
            if self.enable_dialects:
                for i in range(1,len(header)):

                    language_code_with_dialect: str = header[i]

                    if not self.__available_languages.get(language_code_with_dialect, False):
                        self.__available_languages[language_code_with_dialect] = i
                    else:
                        warnings.warn(DUPLICATED_LANGUAGES_WARNING %(language_code_with_dialect, i))
            else:
                self.system_language = self.system_language.split("_")[0]

                for i in range(1,len(header)):

                    language_code_no_dialect: str = header[i].split("_")[0]

                    if not self.__available_languages.get(language_code_no_dialect, False):
                        self.__available_languages[language_code_no_dialect] = i
                    else:
                        warnings.warn(DUPLICATED_LANGUAGES_WARNING %(language_code_no_dialect, i))
        
        
        self.FALLBACK_LANGUAGE: str = next(iter(self.__available_languages))

    @property
    def current_language(self) -> str:
        return self.__current_language

    @property
    def available_languages(self) -> dict[str, int]:
        return self.__available_languages
    
    async def load_messages(self, page: "ft.Page",data: AppData) -> None:
        config_language = await page.client_storage.get_async("%s.app_language"%data.prefix)
        
        if config_language is None:
            config_language = "default"
            asyncio.create_task(page.client_storage.set_async("%s.app_language"%data.prefix, config_language))

        if config_language == "default":
            if self.__available_languages.get(self.system_language,False):
                self.__current_language = self.system_language
            else:
                self.__current_language = self.FALLBACK_LANGUAGE

        elif self.__available_languages.get(config_language,False):
            self.__current_language = config_language
        
        else:
            self.__current_language = self.FALLBACK_LANGUAGE
        
        current_language_index: int = self.__available_languages[self.__current_language]

        with codecs.open(self.csv_path, mode="r", encoding=self.csv_encoding) as file:
            reader: csv.reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.__messages[row[0]] = row[current_language_index]
    
    def get_message(self, msg: str) -> str:
        return self.__messages.get(msg, msg)