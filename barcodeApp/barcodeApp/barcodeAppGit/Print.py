from PIL import Image
import zpl
import os
from zebra import Zebra
class Print:

 def __init__(self):
  self.zebra = Zebra()
  self.printers = self.zebra.getqueues()


 def print(self, queue, height, width):
    z = Zebra(queue)
    z.setup(True, height, width)
    size = str(os.path.getsize(os.path.join(os.path.dirname(os.path.abspath(__file__)),"barcodes/toPrinter.pcx")))
    z.store_graphic("barcode", "barcodes/toPrinter.pcx", size)
    label = """
N
GG0,0, "barcode"
P1    
    """
    z.output(label)
  #  label.preview()


