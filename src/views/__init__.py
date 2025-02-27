from views.view_container import ViewContainer
from views.main.start_view import StartView
from views.pdf.fill_pdf import FillPdf
from views.pdf.export.loading_export import LoadingExport

routes: dict[str,ViewContainer] = {
    "/": StartView("/"),
    "/pdffill/": FillPdf("/pdffill/"),
    "/pdffill/export": LoadingExport("/pdffill/export"),
}