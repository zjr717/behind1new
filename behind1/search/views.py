from flask import request, Blueprint, jsonify, current_app
from behind1.database import db
from behind1.search.models import SearchHistory
import requests
import jwt

search_bp = Blueprint('search_bp', __name__)


# Token 验证装饰器
def token_required(f):
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization']
            jwt.decode(token, '123456', algorithms=['HS256'])

        except:
            return jsonify(code=403, message='无法检验token，请尝试重新登陆')

        return f(*args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated


@search_bp.route('/', methods=['GET'])
@token_required
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', default=1, type=int)

    if not keyword:
        return jsonify(code=400, message='关键词为空')

    params = {
        'key': keyword,
        'pn': page - 1,  # 酷我音乐接口页码从0开始
        'rn': 10,  # 每页返回10条记录
        'httpsStatus': 1,  # 是否使用HTTPS协议
    }
    resp = requests.get('http://www.kuwo.cn/api/www/search/searchMusicBykeyWord', headers={
        'Cookie': 'kw_token=' + current_app.config.get('KW_TOKEN'),
        'Referer': 'http://www.kuwo.cn/search/list?key=' + keyword,
        'csrf': current_app.config.get('KW_CSRF'),
        'User-Agent': current_app.config.get('USER_AGENT'),
    }, params=params)

    if resp.status_code != 200:
        return jsonify(code=500, message='搜索失败')

    result = resp.json()

    data = {
        'songs': [song_info(item) for item in result['data'].get('list', [])],
        }

    # 保存搜索历史记录
    history = SearchHistory(keyword=keyword)
    db.session.add(history)
    db.session.commit()

    return jsonify(code=200, message='Search results', data=data)


@search_bp.route('/download', methods=['GET'])
@token_required
def download():
    rid = request.args.get('rid')
    if not rid:
        return jsonify(code=400, message='Missing rid parameter')

    resp = requests.get('https://link.hhtjim.com/qq/' + rid + '.mp3')

    if resp.status_code != 200:
        return jsonify(code=500, message='下载失败')

    return resp.content


def song_info(item):
    return {
        'name': item['name'],
        'artist': item.get('artist', ''),
        'album': item.get('album', {}).get('name', ''),
        'duration': item.get('duration', 0),
        'rid': item.get('rid', ''),
        'url': item.get('mp3Url', ''),
    }
