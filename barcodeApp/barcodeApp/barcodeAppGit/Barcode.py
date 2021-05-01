from PIL.ImageFont import ImageFont
from barcode import Code128
from barcode.writer import ImageWriter
import PIL
class Barcode:

    @staticmethod
    def barcode(barcodeNumber):
        barcode = Code128(barcodeNumber, writer=ImageWriter())
        barcode.save(f"barcodes/{barcodeNumber}",
                     {"module_width": 0.40, "module_height": 15, "font_size": 18, "text_distance": 1, "quiet_zone": 3})
        return f"barcodes/{barcodeNumber}.png"

    @staticmethod
    def barcode2(barcodeNumber):
        font = PIL.ImageFont.load_default()

        barcode = Code128(barcodeNumber, writer=ImageWriter())
        barcode.save(f"barcodes/{barcodeNumber}",
                     {"module_width": 0.40, "module_height": 15, "font_size": 18, "text_distance": 1, "quiet_zone": 3})
        return f"barcodes/{barcodeNumber}.png"