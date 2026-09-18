import logging
import os
import requests
import sys
import time

sys.path.append(os.path.abspath(os.path.pardir))

from app.parser import parser

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

def test_net_speed(url: str, num_requests: int=10):
    total_bytes = 0
    total_duration = 0.0
    successful_requests = 0

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    session = requests.Session()

    for i in range(num_requests):

        
        logger.info(f"Начата процедура скачивания {i+1}")
        start_time = time.monotonic()
        try:
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.info(f"ℹ️  Не удалось скачать ресурс - возникли проблемы: {e}")
            continue
        else:
            try:
                content_bytes = response.content
                end_time = time.monotonic()
            except AttributeError as e:
                logger.info(f"ℹ️  Не удалось скачать ресурс - контент утерян: {e}")
                continue
            else:
                successful_requests += 1

        duration = end_time - start_time
        size = len(content_bytes)
        total_bytes += size
        total_duration += duration

    if successful_requests < num_requests:
        logger.info(f"⚠️  Не удалось подсчитать скорость интернета за число запросов {num_requests}")
        return

    avg_duration = total_duration / num_requests
    
    # 📝 ФОРМУЛЫ РАСЧЕТА СКОРОСТИ
    
    total_mbytes = total_bytes / pow(1024, 2)
    # Переводим в Мегабайты в секунду (МБ/с)
    speed_mbytes_per_sec = total_mbytes / total_duration

    logger.info("\n" + "="*50)
    logger.info(f"🏆 ИТОГОВЫЕ РЕЗУЛЬТАТЫ ЗАМЕРА ДЛЯ {num_requests} СКАЧИВАНИЙ:")
    logger.info("="*50)
    logger.info(f"📦 Общий объем данных:       {total_mbytes:.2f} МБ")
    logger.info(f"📉 Среднее время 1 запроса:  {avg_duration:.3f} сек.")
    logger.info(f"🚀 СРЕДНЯЯ СКОРОСТЬ СКАЧИВАНИЯ:")
    logger.info(f"   👉 {speed_mbytes_per_sec:.2f} МБ/с (MegaBytes/sec)")
    logger.info("="*50)


if __name__ == "__main__":
    args = parser.parse_args()
    test_net_speed(**dict(args._get_kwargs()))