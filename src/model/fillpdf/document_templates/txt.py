from typing import Optional, override
from model.fillpdf.document_template import DocumentTemplate, DocumentWithNoInputs
from pathlib import Path
import codecs
import re

class TXTTemplate(DocumentTemplate):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        assert file_path.suffix.lower() == ".txt", "%s is not .txt!"%file_path.suffix.lower()

        self.file: codecs.StreamReaderWriter =  codecs.open(file_path, "r", self.text_encoding)
        
        self.text: str = self.file.read()
        
        for item in re.findall("\\[.*?\\]",self.text):
            self.valid_inputs.add(item)
        
        if len(self.valid_inputs) == 0:
            raise DocumentWithNoInputs("%s does not have any valid inputs!"% file_path)
        
    
    @override
    def export(self, headers: tuple[str, ...], data: tuple[str, ...], path: str) -> Optional[tuple[str,...]]:
        super().export(headers,data,path)
        new_text:str = self.text

        for i in range(len(headers)):
            new_text = new_text.replace(headers[i],data[i])

        with open(path, "w") as file:
            file.write(new_text)
    
    # @override
    # def prepare_export(self):
    #     print("Before!")
    
    # @override
    # def clean_export(self):
    #     print("AFter")

    
    

            

    
        