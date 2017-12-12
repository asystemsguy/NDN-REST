import pyndn as ndn
import sys
try:
    import asyncio
except ImportError:
    import trollius as asyncio
from pyndn.threadsafe_face import ThreadsafeFace
import logging
logging.basicConfig()

class NdnClient:
    def __init__(self,localhub_ip):
        self.loop = asyncio.get_event_loop()
        self.face = ThreadsafeFace(self.loop, localhub_ip)
         
    def request(self,req,callback,content= None, mustbefresh= False):
        baseName = ndn.Name(req)
        interest = ndn.Interest(ndn.Name(baseName))
        interest.setMustBeFresh(mustbefresh)
        self.callback = callback
        if content != None:
         interest.setContent(content)
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        self.loop.run_forever()
    
    def _onData(self, interest, data):
        self.callback(data.content)
        self.loop.stop()
    def destroy(self):
        self.face.shutdown()
    def _onTimeout(self, interest):
        print >> "request timeout">> interest.name.toUri()
