from os.path import exists, join

from click import get_app_dir

from diskcache import Cache

from jsonpatch import JsonPatch

from loguru import logger

from re import sub

from requests import get as http_get, HTTPError

from yarl import URL

from .tokenbucket import TokenBucket
from .index import Index
from .torrent import Torrent
from .group import Group

ENDPOINTDEF = 'https://redacted.ch/'
SUCCESS_EXPIRY = 7 * 24 * 60 * 60
FAILURE_EXPIRY = 60


class API(object):
    def __init__(self, api_key, endpoint=ENDPOINTDEF, cache=True, config_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.endpoint = URL(endpoint) if not isinstance(endpoint, URL) else endpoint
        self.cache = cache
        self.config_path = get_app_dir(__package__) if not config_path else config_path
        self.bucket = TokenBucket(10, 5 / 10)

    def get_index(self):
        result = self._get(self.endpoint / 'ajax.php' % {'action': 'index'})
        if result is None:
            return
        return Index(result)

    def rename_torrent_file(self, hash, path):
        result = self.get_directory(hash)
        if result is None:
            return
        return sub('^.*?\/+', result, path)

    def get_directory(self, hash):
        torrent = self.get_torrent(hash)
        group = self.get_group(hash)
        if torrent is None or group is None:
            return
        musicInfo = group.musicInfo
        artists = musicInfo.artists
        release = ''
        
        if group.catalogueNumber:
            release = f' {{{group.catalogueNumber}}}'
        if torrent.remasterCatalogueNumber:
            release = f' {{{torrent.remasterCatalogueNumber}}}'
        if torrent.mb_albumid:
            release = f' {{{torrent.mb_albumid}}}'

        if group.releaseType == 3 or group.releaseType == 7:
            return f'{group.releaseTypeName} - {group.year} - {group.name} [{" ".join([torrent.media, torrent.format, torrent.encoding]).strip()}]{release}'.replace(' []', '').replace('/','-') + '/'
        else:
            return f'{artists[0].name} - {group.releaseTypeName} - {group.year} - {group.name} [{" ".join([torrent.media, torrent.format, torrent.encoding]).strip()}]{release}'.replace(' []', '').replace('/','-') + '/'

    def get_torrent(self, hash):
        result = self._patched_torrent(hash)
        if result is None:
            return
        return Torrent(result['torrent'])

    def get_group(self, hash):
        result = self._patched_torrent(hash)
        if result is None:
            return
        return Group(result['group'])

    def _patched_torrent(self, hash, patch_path = None):
        if patch_path is None:
            patch_path = join(self.config_path, f'{hash}.json-patch')
        result = self._get(self.endpoint / 'ajax.php' % {'action': 'torrent', 'hash': hash.upper()})
        if not exists(patch_path):
            logger.debug(f'{patch_path} does not exist, not applying')
            return result
        logger.debug(f'Applying json patch {patch_path}')
        with open(patch_path, 'r') as patch_file:
            patch = JsonPatch.from_string(patch_file.read())
            result = patch.apply(result)
        return result

    def _get(self, url):
        with Cache(self.config_path) as cache:
            if not self.cache or url not in cache:
                self.bucket.consume()
                logger.trace(url)
                try:
                    r = http_get(
                        url,
                        headers={
                            'User-Agent': 'illallangi-redactedapi/0.0.1',
                            'Authorization': f'{self.api_key}'
                        })
                    r.raise_for_status()
                except HTTPError as http_err:
                    logger.error(f'HTTP error occurred: {http_err}')
                    cache.set(url, None, expire=FAILURE_EXPIRY)
                    return
                except Exception as err:
                    logger.error(f'Other error occurred: {err}')
                    cache.set(url, None, expire=FAILURE_EXPIRY)
                    return
                logger.debug('Received {0} bytes from API'.format(len(r.content)))

                logger.trace(r.request.url)
                logger.trace(r.request.headers)
                logger.trace(r.headers)
                logger.trace(r.text)
                cache.set(
                    url,
                    r.json()['response'],
                    expire=SUCCESS_EXPIRY)
            return cache[url]

    @property
    def supported_trackers(self):
        return ['flacsfor.me']
