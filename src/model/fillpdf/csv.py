from pathlib import Path
import codecs
import csv
import re
import asyncio

class CSV:
    def __init__(self, path: Path, codec: str) -> None:
        self.codec: str = codec
        self.path: Path = path
        self.data: dict[str,list] = {}
        self.valid_indexes: tuple = None
        self.valid_headers: tuple[str] = None
        self.invalid_headers: tuple[str] = None
        self.amount_of_lines: int = 0

    async def read_csv(self) -> None:
        invalid_headers_list: list[str] = []
        valid_heathers_list: list[str] = []
        valid_indexes_list: list[int] = []

        with codecs.open(self.path,"r",self.codec) as file:
            reader: csv.reader = csv.reader(file)
            header: list[str] = next(reader)

            for i in range(len(header)):
                text: str = header[i]
                re.match
                header_match: re.Match = re.match("\\[.*?\\]",text)
                if header_match is not None:
                    valid_heathers_list.append(text)
                    valid_indexes_list.append(i)
                else:
                    invalid_headers_list.append(text)
            
            valid_headers_len: int = len(valid_heathers_list)
            
            if valid_headers_len == 0:
                raise InvalidCSVHeader

            self.invalid_headers = tuple(invalid_headers_list)
            self.valid_headers = tuple(valid_heathers_list)
            self.valid_indexes = tuple(valid_indexes_list)
            
            del invalid_headers_list, valid_heathers_list, valid_indexes_list

            for valid_header_text in self.valid_headers:
                self.data[valid_header_text] = []
            
            await asyncio.sleep(0)

            for line in reader:
                try:
                    for i in range(valid_headers_len):
                        index: int = self.valid_indexes[i]
                        self.data[self.valid_headers[i]].append(line[index])
                except IndexError:
                    continue
                else:
                    self.amount_of_lines += 1



class InvalidCSVHeader(Exception):
    def __init__(self, *args):
        super().__init__(*args)



