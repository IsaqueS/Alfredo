import asyncio
from typing import Optional, override
from model.fillpdf.document_template import DocumentTemplate
from pathlib import Path
import codecs
import re
import random

class TXTTemplate(DocumentTemplate):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        assert file_path.suffix.lower() == ".txt", "% is not .txt!"%file_path.suffix.lower()

        self.file: codecs.StreamReaderWriter =  codecs.open(file_path, "r", self.text_encoding)
        
        self.text: str = self.file.read()
        
        self.valid_inputs = set(
            re.findall("\\[.*?\\]",self.text)
        )
    
    @override
    def export(self, headers: tuple[str, ...], data: tuple[str, ...], path: str) -> Optional[tuple[str,...]]:
        super().export(headers,data,path)
        new_text:str = self.text
        
        assert isinstance(headers, tuple), "%s is not an tuple!"
        assert isinstance(data, tuple), "%s is not an tuple!"

        for i in range(len(headers)):
            new_text = new_text.replace(headers[i],data[i])

        with open(path, "w") as file:
            file.write(new_text)

    
    

            

    
        