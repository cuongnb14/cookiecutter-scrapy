import requests
import logging

logger = logging.getLogger('cms')


class ScraydAPI:
    def __init__(self, host="localhost", port=6800, project="default", spider=None):
        self.base_url = "http://{}:{}".format(host, port)
        self.project = project
        self.spider = spider

    def daemonstatus(self):
        response = requests.get("{}/daemonstatus.json".format(self.base_url))
        return response.json()

    def schedule(self, args=None):
        data = {
            "project": self.project,
            "spider": self.spider,
        }
        if args:
            data.update(args)

        logger.info(data)

        response = requests.post("{}/schedule.json".format(self.base_url), data=data)
        return response.json()

    def listjobs(self):
        params = {
            'project': self.project
        }
        response = requests.get("{}/listjobs.json".format(self.base_url), params=params)
        return response.json()

    def listspiders(self):
        params = {
            'project': self.project
        }
        response = requests.get("{}/listspiders.json".format(self.base_url), params=params)
        return response.json()

    def cancel(self, job_id):
        params = {
            'project': self.project,
            'job': job_id
        }
        response = requests.post("{}/cancel.json".format(self.base_url), params=params)
        return response.json()
