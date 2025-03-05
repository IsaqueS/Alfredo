from typing import override
from docx.document import Document
from model.fillpdf.document_template import DocumentTemplate, DocumentWithNoInputs
import re
import docx

class DOCXTemplate(DocumentTemplate):
    def __init__(self, file_path) -> None:
        super().__init__(file_path)

        self.document: Document = docx.Document(file_path)

        paragraphs_with_input: list[int] = []

        for index in range(len(self.document.paragraphs)):
            text: str = self.document.paragraphs[index].text
            inputs_found: list[str] = re.findall("\\[.*?\\]",text)
            if len(inputs_found) > 0:
                paragraphs_with_input.append(index)
                for input in inputs_found:
                    self.valid_inputs.add(input)
        
        if len(self.valid_inputs) == 0:
            raise DocumentWithNoInputs
        
        self.paragraphs_with_input: tuple[str,...] = tuple(paragraphs_with_input)
    
    @override
    def set_export_type(self, file_type) -> None:
        super().set_export_type(file_type)
        match file_type:
            case "docx":
                self._current_export_function = self.export_docx
            case "pdf":
                self._current_export_function = self.export_pdf
            case _:
                raise NotImplementedError("'%s' file type export is not implemented!")
    
    def export_docx(self, headers, data, path):
        super().export(headers, data, path)
        print("DOCX")
    
    def export_pdf(self, headers, data, path):
        super().export(headers, data, path)
        print("PDF")

            
        