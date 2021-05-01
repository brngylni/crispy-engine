from GroupsDal import GroupsDal

class Product:

    def __init__(self, *args):
        results = GroupsDal.getGroups()
        self.id = args[0]
        self.name = args[1]
        self.quantity = args[2]
        self.dateInward = args[3]
        self.sold = args[4]
        self.saleRate = args[5]
        self.barcodeNumber = args[6]
        self.image1 = args[7]
        self.image2 = args[8]
        self.dateOutward = args[9]
        self.skus = []
        for result in results:
            try:

                self.skus.append([result[0]])
            except Exception:
                continue