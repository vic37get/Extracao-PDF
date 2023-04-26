from parsr_client import ParsrClient as client


def conect():
   parsr = client('localhost:3001')
   return parsr
