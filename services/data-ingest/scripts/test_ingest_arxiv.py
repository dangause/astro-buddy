from src.config import settings
from src.core.utils import get_today_and_n_days_ago, ingest_arxiv

today, yesterday = get_today_and_n_days_ago(1)
if __name__ == '__main__':
    ingest_arxiv(date_from=yesterday, date_until=today)
