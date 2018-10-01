

class GeeksReadEmail(object):
    CHECK_EMAIL = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title></title>
    </head>
    <body>
    <div style="background-color: #FFFFFF; padding: 20px 0;">
        <div style="font-family:'Helvetica Neue',Helvetica,Arial,Sans-serif;
        color:#333;margin:0 auto;padding:24px;max-width:700px;font-size:13px;
        line-height:1.7;border-radius:8px;background-color:#EEEEEE">
            <p style="font-size:28px;line-height:40px;font-weight:300;
            color:#282c32;padding-left:10px;margin-bottom:0;font-weight: bold;
            text-align:center;">
                确认订阅 Geeks Read
            </p>

            <div style="margin-top:5%;margin-left:30%;margin-right:30%;
            padding:2%;max-width:700px;text-align:center;font-size:18px;
            line-height:1.7;border-radius:8px;background-color:#5D5D5D";>
                <a href="{check_link}" style="color:#FFFFFF;
                text-decoration: none">
                    请将我加入到订阅列表
                </a>
            </div>

            <p style="padding:20px;font-size:15px;line-height:2.0;">
                您收到这封邮件，是因为有人用
                "<a href="mailto:{email_address}">{email_address}</a>"
                订阅了 Geeks Read。
                如果这不是您本人的行为，请不要点击上面的链接，
                并请把这封邮件删除，你的邮箱不会被注册。
            </p>
        </div>
    </div>
    </body>
    </html>
    '''

    CONFIRMED_EMAIL = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title></title>
    </head>
    <body>
    <div style="background-color: #FFFFFF; padding: 20px 0;">
        <div style="font-family:'Helvetica Neue',Helvetica,Arial,Sans-serif;
        color:#333;margin:0 auto;padding:24px;max-width:700px;font-size:13px;
        line-height:1.7;border-radius:8px;background-color:#EEEEEE">
            <p style="font-size:28px;line-height:40px;font-weight:300;
            color:#282c32;padding-left:10px;margin-bottom:0;font-weight: bold;
            text-align:center;">
                您已经成功订阅 Geeks Read
            </p>

            <div style="margin-top:5%;margin-left:30%;margin-right:30%;
            padding:2%;max-width:700px;text-align:center;font-size:18px;
            line-height:1.7;border-radius:8px;background-color:#5D5D5D";>
                <a href="{unsubscribe_link}" style="color:#FFFFFF;
                text-decoration:none">
                    我不想再订阅 Geeks Read
                </a>
            </div>

            <p style="padding:20px;font-size:15px;line-height:2.0;">
                您已经成功订阅 Geeks Read。
                您也可以访问我们的网站
                <a href="http://geeksread.geekpark.net/"> Geeks Read </a>
                阅读每日热点新闻。
                我们会为您精选每天热点新闻，每天发送，完全免费。
            </p>
        </div>
    </div>
    </body>
    </html>
    '''

    EMAIL_TEMPLATE = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title></title>
    </head>
    <body>

    <div>
        <div style="margin:0 auto;padding:24px;max-width:700px;
                font-family:'Helvetica Neue',Helvetica,Arial,Sans-serif,serif;
                font-size:13px;line-height:1.7;">

            <div style="text-align: center">
                <p style="font-size: 30px">外媒新闻聚类结果</p>
                <p style="border-collapse: collapse; text-align: center;
                color: #333;">
                    「{time_range}」
                </p>
            </div>

            <div>
                <p style="border-bottom: 1px solid #e2e2e2; font-size: 12px;
                margin-top: 20px; padding-bottom: 4px;
                text-transform: uppercase;">
                    今日国外热点新闻
                </p>
            </div>

            {news_content}



        </div>
    </div>
    </div>

    </body>
    </html>
    '''

    NEWS_CONTENT = '''
    <div style="padding-top: 15px; padding-left: 15px;
        padding-right: 15px; display: block;">

        <div style="    color: #333; text-decoration: none;
            display: block; font-size: 22px; font-weight: bold;
            letter-spacing: -0.5px; line-height: 1.4;margin-bottom: 10px">
            <a style="text-decoration:none" href="{topic_url}"
            target="_blank">
                {topic}
            </a>
        </div>

        <p style="font-size: 15px; color: #8e8e8e; margin-top: 5px;
            margin-bottom: 5px;word-wrap:break-word;">
            {summary}
        </p>

        <p style="font-size: 15px; color: rgba(0,0,0,0.44);
            margin-top: 5px;margin-bottom: 5px;">
            被报道次数：{news_count}次
        </p>

        <ul style="font-size: 15px;">
            {news_list}
        </ul>
    </div>
    '''

    NEWS_LIST = '''
        <li>
            <a style="text-decoration:none" href="{url}"
            target="_blank">{title}</a>
        </li>
    '''

    SUBJECT = '外媒新闻聚类结果（{time_range}）'
