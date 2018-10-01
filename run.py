import mongoengine

from apscheduler.schedulers.background import BackgroundScheduler

from skr import settings
from skr import app
from skr.api import v1  # noqa: F401
from skr.service.cluster import save_cluster_data
from skr.service.email import send_geeks_read_email
from skr.service.health_clean import clean_article

mongoengine.connect(
    settings.DB_NAME, host=settings.DB_HOST, port=settings.DB_PORT)

sched = BackgroundScheduler()

sched.add_job(save_cluster_data, 'cron', minute=20)
sched.add_job(send_geeks_read_email, 'cron', hour=7, minute=30)
sched.add_job(clean_article, 'cron', day_of_week=6)

sched.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
