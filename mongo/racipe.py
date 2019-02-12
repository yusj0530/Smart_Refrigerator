from datetime import datetime
from urllib.request import Request, urlopen


def crawling(url='', encoding='utf-8'):
    try:
        request = Request(url)
        response = urlopen(request)
        # 공통적인 것은 모듈화 시켜줘야 한다.
        # 파싱하는 html에서 utf-8이 아닐경우 에러가 나오기 때문에 미리 try구문을 쓴다.
        try:
            receive = response.read()
            result = receive.decode(encoding)
        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace')

        print('%s : success for request [%s]' % (datetime.now(), url))
        return result

    except Exception as e:
        # string으로 포멧(e=에러 내용)
        print('%s : %s' % (e, datetime.now()))
