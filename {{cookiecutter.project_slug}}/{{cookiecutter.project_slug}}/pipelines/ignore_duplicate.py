class IgnoreDuplicatePipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            item['dropped'] = True
        else:
            item['dropped'] = False
            self.ids_seen.add(item['id'])
        return item
