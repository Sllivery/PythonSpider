class Datapipeline:
    def __init__(self, path, raw_data):
        self.raw_data = raw_data
        self.coding = 'utf-8'
        self.save_path = ""
        save_path = self.process_save_path(path)

    def trans_coding(self):
        pass

    def process_save_path(self, path):
        process_path = path
        return process_path

    def process_data(self):
        self.raw_data.split(',')
        av_item_list = []