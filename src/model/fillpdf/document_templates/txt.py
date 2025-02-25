from model.fillpdf.document_template import DocumentTemplate
from pathlib import Path
import codecs
import re

class TXTTemplate(DocumentTemplate):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        assert file_path.suffix.lower() == ".txt", "% is not .txt!"%file_path.suffix.lower()

        self.file: codecs.StreamReaderWriter =  codecs.open(file_path, "r", self.text_encoding)
        
        text: str = self.file.read()
        
        self.valid_inputs = set(
            re.findall("\\[.*?\\]",text)
        )
        print(self.valid_inputs)

            

    
        