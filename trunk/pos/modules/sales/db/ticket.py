class TicketDB:
    def getAllTickets(self):
        sql = "SELECT id FROM tickets WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllTickets', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertTicket(self, user_id):
        sql = "INSERT INTO tickets (date_open, user_id) VALUES (NOW(), %s)"
        params = (user_id,)
        cursor, success = self.db.query('insertTicket', sql, params)
        if success:
            ticket_id = self.conn.insert_id()
            return ticket_id
        else:
            return None

    def deleteTicket(self, ticket_id):
        sql = "UPDATE tickets SET state=-1 WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('deleteTicket', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def closeTicket(self, ticket_id):
        sql = "UPDATE tickets SET date_close=NOW() WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('closeTicket', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def setTicketComment(self, ticket_id, comment):
        sql = "UPDATE tickets SET comment=%s WHERE id=%s"
        params = (comment, ticket_id,)
        cursor, success = self.db.query('setTicketComment', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def setTicketCustomer(self, ticket_id, customer_id):
        sql = "UPDATE tickets SET customer_id=%s WHERE id=%s"
        params = (customer_id, ticket_id,)
        cursor, success = self.db.query('setTicketCustomer', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getTicketComment(self, ticket_id):
        sql = "SELECT comment FROM tickets WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('getTicketComment', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None

    def getTicketCustomer(self, ticket_id):
        sql = "SELECT customer_id FROM tickets WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('getTicketCustomer', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None

    def ticketIsClosed(self, ticket_id):
        sql = "SELECT (date_close IS NOT NULL) as 'closed' FROM tickets WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('ticketIsClosed', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return bool(results[0])
            else:
                return None
        else:
            return None

    def getTicketUser(self, ticket_id):
        sql = "SELECT user_id FROM tickets WHERE id=%s"
        params = (ticket_id,)
        cursor, success = self.db.query('getTicketUser', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None
