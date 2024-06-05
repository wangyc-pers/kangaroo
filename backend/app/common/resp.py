from asgi_correlation_id import correlation_id
from starlette.responses import JSONResponse


class JsonResp(object):
    SUCCESS = 0
    FAILED = -1

    def __init__(self, code, msg="", data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data,
            "request_id": correlation_id.get(),
        }

    @property
    def ok(self):
        return self.code == self.SUCCESS

    def __call__(self, data=None, msg=None, **kwargs):
        content = self.to_dict()
        content.update(kwargs)
        if data is not None:
            content["data"] = data
        if msg is not None:
            content["msg"] = msg
        resp = JSONResponse(content, **kwargs)
        return resp


SUCCESS = JsonResp(code=JsonResp.SUCCESS, msg="success")

ERR_UNKNOWN = JsonResp(code=JsonResp.FAILED, msg="unknown error")
