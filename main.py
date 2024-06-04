import os
import patterns
import json
import re
from collections import defaultdict
from datetime import datetime

"""
общее количество выполненных запросов
количество запросов по HTTP-методам: GET, POST, PUT, DELETE, OPTIONS, HEAD. Например, GET - 20, POST - 10 и т.п.
топ 3 IP адресов, с которых было сделано наибольшее количество запросов
топ 3 самых долгих запросов - должны выводиться HTTP-метод, URL, IP, длительность запроса, дата и время запроса
"""
def parse(file):
    requests_number = 0
    method_requests_count = defaultdict(int)
    ip_requests_count = defaultdict(lambda: {"requests_number": 0})
    methods = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "OPTIONS": 0, "HEAD": 0}
    requests = []
    top3_ips = defaultdict(int)
    top3_longest_requests = []
    with open(file, 'r') as file:
        for line in file:
            host_ip = re.search(patterns.HOST_IP, line).group(0)
            timestamp = re.search(patterns.TIMESTAMP, line).group(0)
            method = re.search(patterns.METHOD, line).group(0)
            referer = re.search(patterns.REFERER, line)
            if referer:
                url = referer.group(0)[1:-1]
            else:
                url = "empty url"
            duration = re.search(patterns.DURATION, line).group(0).split('\n')[0]

            requests_number += 1
            methods[method] += 1
            body = {
                'ip': host_ip,
                'method': method,
                'duration': int(duration),
                'date': timestamp,
                'url': url,
            }
            requests.append(body)
            ip_requests_count[body['ip']]["requests_number"] += 1
            top3_ips = dict(sorted(ip_requests_count.items(), key=lambda x: x[1]["requests_number"], reverse=True)[0:3])
            top3_longest_requests = sorted(requests, key=lambda x: x['duration'], reverse=True)[0:3]

        result = {
            'filename' : str(file.name),
            'top_ips': {k: v['requests_number'] for k, v in top3_ips.items()},
            'top_longest': top3_longest_requests,
            'total_stat': methods,
            'total_requests': requests_number
        }
        result = json.dumps(result, indent=4)
        print(result)

        dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(dt, "a") as file:
            file.write(result)



def main (path):
    try:
        if os.path.isfile(path):
            print("File was passed")
            parse(path)
        elif os.path.isdir(path):
            print("Dir was passed")
            for file in os.listdir(path):
                if file.endswith(".log"):
                    print(file)
                    parse(os.path.join(path, file))
    except Exception as e:
        print("Exception occured", str(e))


if __name__ == '__main__':
    main("logs")
