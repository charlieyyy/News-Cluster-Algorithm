import datetime

import aiohttp

from skr import settings


def api_response(data=None, status_code=200):
    if data is None:
        data = {}
    return {'data': data}, status_code, {'Access-Control-Allow-Origin': '*'}


def item_pop(item, pop_list):
    for name in pop_list:
        item.pop(name, None)
    return item


def get_last_day_str(day=None):
    if day is None:
        day = datetime.date.today()
    last_day = day - datetime.timedelta(days=1)
    day_str = str(last_day).replace('-', '')
    return day_str


def mail_generator(template: str, format_map: dict) -> str:
    return template.format_map(format_map)


async def sendmail(subject, context, to_email_address):
    data = dict(subject=subject, mail_body=context,
                tag='SKR', to_email=to_email_address)
    headers = {'apikey': settings.MAIL_SERVICE_API_KEY}
    common_mail_api_url = f'{settings.MAIL_SERVICE_HOST}/common_email'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(common_mail_api_url, json=data) as resp:
            return {'status': resp.status == 200, 'email': data['to_email']}
