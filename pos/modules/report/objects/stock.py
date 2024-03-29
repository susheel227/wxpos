import pos

import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, \
                                                 Paragraph, Spacer

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from pos.modules.report.objects.pdf import PDFReport, stylesheet

import pos.modules.currency.objects.currency as currency
from pos.modules.stock.objects.product import Product

class StockPDFReport(PDFReport):
    def _init_content(self):
        session = pos.database.session()
        ps = session.query(Product).filter(Product.in_stock).all()
    
        total = 0
        def_c = currency.get_default()
        headers = ('Reference', 'Name', 'Price', 'Quantity', 'Total')
        data = []
        marked = []
        for p in ps:
            pc = p.currency
            p_total = p.quantity*p.price
            
            data.append([p.reference,
                         p.name,
                         pc.format(p.price),
                         'x%d' % (p.quantity,),
                         pc.format(p_total)])
            if p.quantity<=0:
                marked.append(len(data))

            total += currency.convert(p_total, pc, def_c)

        table = self.doTable(data=data, header=headers, marked_rows=marked)

        total_para = Paragraph('Total: %s' % (def_c.format(total),),
                               stylesheet['Heading3Right'])
        self.elements.append(Spacer(36,36))
        self.elements.append(total_para)

def generateReport(filename):
    today = datetime.date.today()
    rep = StockPDFReport(filename, 'Stock Report',
                         None,
                         (today, None))
    return rep.build()
