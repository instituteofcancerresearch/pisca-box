import __init__ # noqa: F401
import libs.widgets as widgets

def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca tutorial')
            
    widgets.show_pdf('app/static/pisca-help-inputs.pdf',height=800)
