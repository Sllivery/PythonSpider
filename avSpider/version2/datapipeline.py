class Datapipeline:
    def __init__(self, path):
        self.coding = 'utf-8'
        self.save_path = ""
        save_path = self.process_save_path(path)

    def trans_coding(self):
        pass

    def process_save_path(self, path):
        process_path = path
        return process_path


