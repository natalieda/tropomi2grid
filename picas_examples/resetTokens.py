'''
Created on 17 March 2016
   
@author: Natalie Danezi <anatoli.danezi@surfsara.nl>
@helpdesk: SURFsara helpdesk <helpdesk@surfsara.nl>

usage: python resetTokens.py [viewname]
  e.g. python resetTokens.py Monitor/locked

description:
	Connect to PiCaS server
	Reset all the Tokens in the [viewname] View
	Increase the scrubcount and update the database
'''

# python imports
import sys
import picasconfig

# picas imports
from picas.actors import RunActor
from picas.clients import CouchClient
from picas.iterators import BasicViewIterator
from picas.modifiers import BasicTokenModifier


class ExampleActor(RunActor):
    def __init__(self, iterator, modifier):
        self.iterator = iterator
        self.modifier = modifier
        self.client = iterator.client

    def reset(self, viewname):
        server = self.client.server
        db = self.client.db
        v = db.view(viewname)
        to_update = []
        for x in v:
            document = db[x['key']]
            document['lock'] = 0
            document['done'] = 0
            document['scrub_count'] += 1
            document['hostname'] = ''
            document['exit_code'] = ''
            to_update.append(document)
        db.update(to_update)


def reset():
    client = CouchClient(url=picasconfig.PICAS_HOST_URL, db=picasconfig.PICAS_DATABASE,
                         username=picasconfig.PICAS_USERNAME, password=picasconfig.PICAS_PASSWORD)
    modifier = BasicTokenModifier()
    viewname = str(sys.argv[1])
    # iterator = BasicViewIterator(client, "Monitor/locked", modifier)
    iterator = BasicViewIterator(client, viewname, modifier)
    actor = ExampleActor(iterator, modifier)
    return actor.reset(viewname)


if __name__ == '__main__':
    reset()
