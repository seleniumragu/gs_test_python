
from requests import Session


class BaseSession(Session):
    def __init__(self, base_url, username=None, password=None, header=None):

        self.base_url = base_url
        self.username = username
        self.password = password
        self.header = header
        super(BaseSession, self).__init__()

    def get(self, url, **kwargs):
        """
        Api GET request
        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: Api response
        """
        kwargs.setdefault('timeout', 60)
        url = self.base_url+url
        return super().get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        Api POST request
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: Api response
        """
        self._set_header()
        kwargs.setdefault('timeout', 60)
        url = self.base_url + url
        return super().post(url, data=data, headers=self.header, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """
        Api PUT request
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: Api response
        """
        self._set_header()
        kwargs.setdefault('timeout', 60)
        url = self.base_url + url
        return super().put(url, data=data, headers=self.header, **kwargs)

    def delete(self, url, data=None, **kwargs):
        """
        Api DELETE request
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: Api response
        """
        self._set_header()
        kwargs.setdefault('timeout', 60)
        url = self.base_url + url
        return super().delete(url, data=data, headers=self.header, **kwargs)

    def _set_header(self, header=None):
        if header is None:
            header = {
                "Content-Type": "application/json",
                "charset": "UTF-8"
            }
        self.header = header

