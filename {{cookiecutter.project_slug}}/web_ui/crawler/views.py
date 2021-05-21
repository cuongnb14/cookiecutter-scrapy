import json
import logging
import re
from datetime import datetime

import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from crawler.scrapyd import ScraydAPI

logger = logging.getLogger('apps')

SCRAPYD_HOST = '127.0.0.1'
SCRAPYD_PORT = 6800


def index(request):
    scrapy_client = ScraydAPI(host=SCRAPYD_HOST, port=SCRAPYD_PORT)

    jobs = scrapy_client.listjobs()
    jobs['finished'] = list(reversed(jobs['finished']))[:15]
    for job in jobs['finished']:
        during = datetime.strptime(job["end_time"], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(
            job["start_time"], "%Y-%m-%d %H:%M:%S.%f")
        job["during"] = during.total_seconds() / 60

    spiders = scrapy_client.listspiders()["spiders"]

    context = dict(
        status=scrapy_client.daemonstatus(),
        jobs=jobs,
        spiders=spiders,
        log_url="http://{}:{}/logs/default".format(SCRAPYD_HOST, SCRAPYD_PORT),
    )

    return render(request, 'crawler/status.html', context)


def run_spider(request, spider):
    try:
        try:
            scrapy_client = ScraydAPI(host=SCRAPYD_HOST, port=SCRAPYD_PORT, spider=spider)
            params = request.GET.get('params', None)
            args = {}
            if params:
                peices = params.split(",")
                for item in peices:
                    temp = item.strip().split("=")
                    args[temp[0].strip()] = temp[1].strip()
        except Exception:
            raise Exception("Parse params error")

        response = scrapy_client.schedule(args=args)

        msg = 'Job id: {}'.format(response["jobid"])
        if params:
            msg += '. Params: {}'.format(params)
        messages.add_message(request, messages.SUCCESS, msg)
    except Exception as e:
        messages.add_message(request, messages.ERROR, "Error: {}".format(str(e)))
    return redirect(reverse('status'))


def cancel_job(request, job_id):
    try:
        scrapy_client = ScraydAPI(host=SCRAPYD_HOST, port=SCRAPYD_PORT)
        response = scrapy_client.cancel(job_id=job_id)
        if response["status"] == "ok":
            msg = 'Closing Job id: {}'.format(job_id)
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            msg = "Error: {}".format(str(response))
            messages.add_message(request, messages.ERROR, msg)
    except Exception as e:
        logger.exception(e)
        messages.add_message(request, messages.ERROR, "Error: {}".format(str(e)))
    return redirect(reverse('status'))


def log_stats(request, spider, job_id):
    try:
        url = "http://{}:{}/logs/default/{}/{}.log".format(SCRAPYD_HOST, SCRAPYD_PORT, spider, job_id)
        response = requests.get(url)
        content = response.text
        matches = re.search(r"Dumping Scrapy stats:(.*)\d\d\d\d-\d\d", content.replace("\n", ""))
        stats = matches.group(1)

        stats = re.sub(r'(?is)(datetime\.datetime\([\d\,\s]+\))', r'"\1"', stats).replace("'", '"')
        stats = json.loads(stats)

        result = {
            "result": {
                "item_scraped_count": 0,
                "response_received_count": 0,
                "finish_reason": ""
            },
            "downloader": {},
            "log_count": {},
            "scheduler": {},
            "item_scraped_count": 0,
            "finish_reason": "",
            "more": {},
        }
        for k, v in stats.items():
            if k.startswith("downloader"):
                result["downloader"][k[11:]] = v
            elif k.startswith("log_count"):
                result["log_count"][k[10:]] = v
            elif k.startswith("scheduler"):
                result["scheduler"][k[10:]] = v
            elif k in result['result'].keys():
                result['result'][k] = v
            else:
                if k in ['start_time', 'finish_time']:
                    # result["more"][k] = str(eval(v))
                    continue
                else:
                    result["more"][k] = v

        return TemplateResponse(request, "crawler/log_stats.html", {"data": result})
    except Exception as e:
        logger.exception(e)
        raise e


def log_detail(request, spider, job_id):
    url = "http://{}:{}/logs/default/{}/{}.log".format(SCRAPYD_HOST, SCRAPYD_PORT, spider, job_id)
    response = requests.get(url)
    content = response.text
    return HttpResponse(content, content_type='text/plain')
