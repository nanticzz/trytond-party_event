#This file is part party_event module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool
from trytond.transaction import Transaction

import datetime

class PartyEvent(ModelSQL, ModelView):
    'Party Event'
    _name = 'party.event'
    _description = __doc__
    _order_name = 'date'

    event_date = fields.DateTime('Date', required=True, readonly=True)
    subject = fields.Char('Subject', required=True, readonly=True)
    description = fields.Text('Description', readonly=True)
    party = fields.Many2One('party.party', 'Party', required=True, readonly=True)
    resource = fields.Reference('Resource', selection='get_resource', readonly=True)
    user = fields.Many2One('res.user', 'User', required=True, readonly=True)

    def __init__(self):
        super(PartyEvent, self).__init__()
        self._order.insert(0, ('event_date', 'DESC'))
        self._error_messages.update({
            'not_subject': 'Not subject',
        })

    def get_resource(self):
        '''Get Resources. Rewrite this method to add new resource references'''
        res = []
        return res

    def get_rec_name(self, ids, name):
        if not ids:
            return {}
        res = {}
        for mail in self.browse(ids):
            res[mail.id] = mail.subject
        return res

    def get_message(self, message):
        """
        Get message translated by language user
        :param message: srt
        :return: str
        """
        translation_obj = Pool().get('ir.translation')
        message = self._error_messages.get(message, message)
        language = Transaction().language
        res = translation_obj.get_source(self._name, 'error', language, message)
        if not res:
            res = translation_obj.get_source(message, 'error', language)
        if res:
            message = res
        return message

    def create_event(self, party, resource, values={}):
        """
        Create event at party from details
        :param party: party ID
        :param resource: str (object,id) Eg: 'electrinic.mail,1'
        :param values: Dicc {subject:, date:, description:} (optional)
        """
        now = datetime.datetime.now()

        values = {
            'event_date':values.get('date') or now,
            'subject':values.get('subject') or self.get_message('Not subject'),
            'description':values.get('description',''),
            'party':party,
            'resource':resource,
            'user':Transaction().user,
        }
        try:
            self.create(values)
        except:
            pass
        return True

PartyEvent()
