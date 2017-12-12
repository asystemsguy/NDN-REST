import matplotlib
from ndnPyClient import  NdnClient
matplotlib.use('Agg')
import time
import matplotlib.pyplot as plt
#matplotlib.use('Agg')

client =  NdnClient('172.17.0.6')

def test(data):
    print data

def test1(data):
    print data
if __name__ == '__main__':
    #client.request()
    
  
     #start = time.time()
     #client.request("/changeshowtimes/POST",test,"000123456789123456789123456789",mustbefresh=True)
     #roundtrip = time.time() - start
     #print roundtrip
     #client.request("/showtimes/GET",test,mustbefresh=True)
     #client.request("/showtimes/GET",test1,mustbefresh=True)
     #start = time.time()
     #client.request("/changeshowtimes/POST",test,"000123456789123456789123456789",mustbefresh=True)
     #roundtrip = time.time() - start
     #print roundtrip
    x = []
    i = 0  
    while i!=10000: 
     start = time.time()
     client.request("/changeshowtimes/POST",test,"000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789000123456789123456789123456789",mustbefresh=True)
     roundtrip = time.time() - start
     i = i +1
     x.insert(i,roundtrip)
    plt.ioff()
    fig = plt.figure()
    #plt.subplot(221)
    plt.plot(x)
    #plt.yscale('linear')
    #plt.title('linear')
    #plt.grid(True) 
    fig.savefig('plot.png')
    plt.close(fig)
     

