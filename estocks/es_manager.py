from elasticsearch_dsl.connections import connections


class ESManager:
    def __init__(self, hosts=None, http_auth=None, timeout=None):
        self.hosts = hosts
        self.http_auth = http_auth
        self.timeout = timeout
        self.client = None
        self._do_init()

    def _do_init(self):
        if not self.hosts:
            return

        if self.http_auth:
            self.client = connections.create_connection(alias='default',
                                                        hosts=self.hosts,
                                                        timeout=self.timeout,
                                                        http_auth=self.http_auth)
        else:
            self.client = connections.create_connection(alias='default',
                                                        hosts=self.hosts,
                                                        timeout=self.timeout)

    def init_from_dict(self, dict_conf):
        hosts = dict_conf.get('ES_HOSTS', '')
        self.hosts = hosts.split(',') if hosts else []
        es_user, es_passwd = dict_conf.get('ES_USER', None), dict_conf.get('ES_PASSWD', None)
        self.http_auth = (es_user, es_passwd) if es_user and es_passwd else None
        self.timeout = dict_conf.get('ES_TIMEOUT', 20)

        self._do_init()
