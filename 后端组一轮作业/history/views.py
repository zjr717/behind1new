from flask import request, Blueprint, jsonify, current_app
from 后端组一轮作业.database import db
from 后端组一轮作业.search.models import SearchHistory
import requests
import jwt

history_bp = Blueprint('history_bp', __name__)


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


# 获取搜索历史记录
@history_bp.route('/history', methods=['GET'])
@token_required
def history():
    keyword =SearchHistory.query.order_by(SearchHistory.time.desc()).first().keyword
    page = request.args.get('page', default=1, type=int)
    params = {
        'key': keyword,
        'pn': page - 1,  # 酷我音乐接口页码从0开始
        'rn': 10,  # 每页返回10条记录
        'httpsStatus': 1,  # 是否使用HTTPS协议
    }
    histories = SearchHistory.query.order_by(SearchHistory.time.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    resp = requests.get('http://www.kuwo.cn/api/www/search/searchMusicBykeyWord', headers={
        'Cookie': 'kw_token=' + current_app.config.get('KW_TOKEN'),
        'Referer': 'http://www.kuwo.cn/search/list?key=' + keyword,
        'csrf': current_app.config.get('KW_CSRF'),
        'User-Agent': current_app.config.get('USER_AGENT'),
    }, params=params)

    result = resp.json()

    return jsonify(code=200, message='success', data={
        'songs': [song_info(item) for item in result['data'].get('list', [])],
    },count=histories.page)


# 收藏历史记录
@history_bp.route('/history/lc', methods=['PUT'])
@token_required
def favorite():
    keyword = SearchHistory.query.order_by(SearchHistory.time.desc()).first().keyword
    data = request.get_json()
    history_id = data.get['id']
    history = SearchHistory.query.filter_by(id=history_id).first()
    page = request.args.get('page', default=1, type=int)
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

    result = resp.json()
    if history:
        history.favorite = True
        db.session.commit()

        return jsonify(code=200, message='success',data={
            'songs': [fav_info(item) for item in result['data'].get('list', [])],
        })
    else:
        return jsonify(code=404, message='未找到该历史记录')


# 删除历史记录
@history_bp.route('/history', methods=['DELETE'])
@token_required
def delete_history():
    data = request.get_json()
    history_id = data.get['id']
    history = SearchHistory.query.filter_by(id=history_id).first()
    if request.json['type'] == 1:
        db.session.delete(history)
        db.session.commit()
        return jsonify(code=200, message='success')
    else:
        return jsonify(code=404, message='未找到该历史记录')


def song_info(item):
    return {
        'name': item['name'],
        'artist': item.get('artist', ''),
        'album': item.get('album', {}).get('name', ''),
        'duration': item.get('duration', 0),
        "fav": item.get('fav', ''),
        'rid': item.get('rid', ''),
        'url': item.get('mp3Url', ''),
        'id': item.get('id', ''),
    }


def fav_info(fav):
    return {
        'name': fav['name'],
        'artist': fav.get('artist', ''),
        'album': fav.get('album', {}).get('name', ''),
        'duration': fav.get('duration', 0),
        'rid': fav.get('rid', ''),
    }
