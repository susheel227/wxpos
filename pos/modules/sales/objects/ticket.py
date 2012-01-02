import pos

import pos.modules.base.objects.common as common

from pos.modules.stock.objects.product import Product
from pos.modules.sales.objects.ticketline import TicketLine

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, Enum, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Ticket(pos.database.Base, common.Item):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    date_open = Column(DateTime, nullable=True, default=func.current_timestamp())
    date_close = Column(DateTime, nullable=True)
    payment_method = Column(Enum('cash', 'cheque', 'voucher', 'card', 'free', 'debt'), nullable=True)
    date_paid = Column(DateTime, nullable=True)
    comment = Column(String(255), nullable=True)
    discount = Column(Float, nullable=False, default=0)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    currency = relationship("Currency", backref="tickets")
    customer = relationship("Customer", backref="tickets")
    user = relationship("User", backref="tickets")

    @hybrid_property
    def paid(self):
        return self.date_paid is not None

    @paid.setter
    def paid(self, value):
        if value:
            self.date_paid = func.now()
        else:
            self.date_paid = None

    @paid.expression
    def paid(cls):
        return cls.date_paid != None

    def pay(self, method, paid=True):
        self.payment_method = method
        self.paid = paid
        session = pos.database.session()
        session.commit()
    
    @hybrid_property
    def closed(self):
        return self.date_close is not None

    @closed.setter
    def closed(self, value):
        if value:
            self.date_close = func.now()
            session = pos.database.session()
            result = session.query(Product, TicketLine.amount).filter((TicketLine.ticket == self) & \
                                                        (TicketLine.product_id == Product.id) & \
                                                        Product.in_stock).all()
            for p, amount in result:
                p.quantity_out(amount)
            session.commit()
        else:
            self.date_close = None

    @closed.expression
    def closed(cls):
        return cls.date_close != None

    @hybrid_property
    def total(self):
        session = pos.database.session()
        total = session.query(func.sum(TicketLine.total)).filter(TicketLine.ticket == self).one()[0]
        return total*(1-self.discount) if total is not None else 0
    
    @hybrid_property
    def display(self):
        return 'Ticket #'+str(self.id)
    
    @display.expression
    def display(self):
        return func.concat('Ticket #', self.id)
    
    def __repr__(self):
        return "<Ticket %s>" % (self.id,)
