from flask import Flask, request
from ext import redis_store, mongo, cache
from source import Source

def create_app():
    """initialize flask app
    """

    app = Flask(__name__)
    app.config.update(
        REDIS_URL= "redis://@localhost:6379/0",
        MONGO_URI= "mongodb://root:1qaz2wsx@127.0.0.1:27017/cachesimulate"
    )

    register_extensions(app)

    return app

def register_extensions(app):
    """註冊app service
    """
    redis_store.init_app(app)
    mongo.init_app(app)
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

app = create_app()

@app.route('/')
def index():
    # 條件
    # - 縣市
    # - 區域
    # - 用途
    # - 價格起
    # - 價格訖

    county = request.args.get('county') or "taipei"
    district = request.args.get('district') or ""
    purpose  = request.args.get('purpose') or ""
    price_l = request.args.get('pricel') or ""
    price_h = request.args.get('priceh') or ""

    s = Source(county, district, purpose, price_l, price_h)
    val = s.get_value()

    return ""

@app.route('/cache')
def cache_keys():
    return cache

@app.route('/hotkey', methods=['POST'])
def hotkey():
    req_data = request.get_json()
    if 'caches' in req_data:
        for cv in req_data['caches']:
            cache[cv['cache_key']] = cv['cache_value']
    
    return "ok"

if __name__ == '__main__':
    app.run()