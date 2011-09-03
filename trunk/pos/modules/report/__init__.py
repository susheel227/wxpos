from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

import pos.modules

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Reports", 'reports')

    def loadSubItems(self):
        if pos.modules.isInstalled('sales'):
            from pos.modules.report.panels import SalesReportPanel
            MenuItem(self.menu, "Reports", "Sales", SalesReportPanel)
        if pos.modules.isInstalled('customer'):
            from pos.modules.report.panels import CustomersReportPanel
            MenuItem(self.menu, "Reports", "Customers", CustomersReportPanel)
        if pos.modules.isInstalled('stock'):
            from pos.modules.report.panels import StockReportPanel
            MenuItem(self.menu, "Reports", "Stock", StockReportPanel)
        if pos.modules.isInstalled('user'):
            from pos.modules.report.panels import UsersReportPanel
            MenuItem(self.menu, "Reports", "Users", UsersReportPanel)

dependencies = ('base',)