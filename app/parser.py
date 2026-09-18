import argparse
import re
parser = argparse.ArgumentParser()



def raise_(message: str):
    raise ValueError(message)
"https://esahubble.org/media/archives/images/publicationtiff/sci25007a.tif"

parser.add_argument(
    "--url", 
    type=lambda url: url if isinstance(url, str) and re.match(r'^https?:\/\/[\S]+$', url) else raise_(f"Неверный формат URL: {url}"),
    help="URL ресурса",
    default="https://esahubble.org/media/archives/images/original/sci25007a.tif"
)

parser.add_argument(
    "--num_requests", 
    type=int,
    help="Количество запросов",
    default=10
)

