import json
import pyndn as ndn
import pyndn.security as ndnsec
import sys
import re
try:
    import asyncio
except ImportError:
    import trollius as asyncio
from pyndn.threadsafe_face import ThreadsafeFace
import logging
logging.basicConfig()
import sys
import time
import argparse
import traceback
import random

from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn.security import KeyChain


class Flask():
  def __init__(self, host):
      self.__name__ = __name__
      self.keyChain = KeyChain()
      self.isDone = False
      self.counter = 0
      loop = asyncio.get_event_loop()
      self.face = ThreadsafeFace(loop, host)
      self.a = {}
      self.methods = {}

  def route(self, uri, methods):
      prefix  = uri
      if bool(re.search('<(.*)>', prefix)):
         self.baseName = ndn.Name(re.sub('<(.*)>',  methods[0]+'/<data>', prefix)) 
      else: 
         self.baseName = ndn.Name(prefix+"/"+methods[0])
      self.methods[self.baseName.toUri()]=methods[0]
      return self.dec 

  def onInterest(self, prefix, interest, *k):
      print >> sys.stderr, "<< PyNDN %s" % interest.name
  
      intrestUri = interest.name.toUri()
      prefixUri = prefix.toUri()
     
      parameters = ''
      if intrestUri != prefixUri:
          parameters = intrestUri[len(prefixUri)+1:]
          print 
          prefixUri += "/%3Cdata%3E"

      d = self.a[prefixUri]
      if self.methods[prefixUri] == "POST":
         content = json.dumps(d(interest.getContent().toRawStr().decode('string_escape')))
      else:
         if parameters:
            content = json.dumps(d(parameters))
         else:
            content = json.dumps(d())
      
      self.counter += 1
      data = ndn.Data(interest.getName())

      meta = ndn.MetaInfo()
      meta.setFreshnessPeriod(5000)
      data.setMetaInfo(meta)

      data.setContent(content)
      self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())

      self.face.putData(data)

  def _onRegisterFailed(self, prefix):
      print >> sys.stderr, "<< PyNDN: failed to register prefix"

  def run(self):
      root = logging.getLogger()
      root.setLevel(logging.DEBUG)

      ch = logging.StreamHandler(sys.stdout)
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      ch.setFormatter(formatter)
      root.addHandler(ch)
      loop = asyncio.get_event_loop()
      server = Server(self.face)

      loop.run_forever()
      self.face.shutdown()
      
  def dec(self,func): 
      self.a[self.baseName.toUri()] = func
      self.face.registerPrefix(self.baseName,
                               self.onInterest, self._onRegisterFailed,)

class Server:
  def __init__(self, face):
      self.face = face
      self.counter = 0
      self.keyChain = ndnsec.KeyChain()
      self.face.setCommandSigningInfo(self.keyChain, self.keyChain.getDefaultCertificateName())
