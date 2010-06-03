##
# Copyright (c) 2010 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from semantix.caos import session


class Session(session.Session):
    def __init__(self, realm, connection, entity_cache):
        super().__init__(realm, entity_cache=entity_cache)
        self.connection = connection
        self.xact = []

    def _new_transaction(self):
        xact = self.connection.xact()
        xact.begin()
        return xact

    def in_transaction(self):
        return super().in_transaction() and bool(self.xact)

    def begin(self):
        super().begin()
        self.xact.append(self._new_transaction())

    def commit(self):
        super().commit()
        xact = self.xact.pop()
        xact.commit()

    def rollback(self):
        super().rollback()
        if self.xact:
            xact = self.xact.pop()
            xact.rollback()

    def rollback_all(self):
        super().rollback_all()
        while self.xact:
            self.xact.pop().rollback()
