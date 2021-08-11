
from gzip import GzipFile
from io import  BytesIO
import json

def compress(data):
  out = BytesIO()
  gz = GzipFile(None, 'wb', 9, out)
  gz.write(json.dumps(data).encode('utf-8'))
  gz.close()
  return out.getvalue()