#!/usr/bin/env python3

from faker import Faker
import aiohttp
from urllib.parse import urljoin, urlparse
import asyncio
from enum import Enum, unique
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
from requests.models import Response

@dataclass
class Page:
    """
    A data class that bundles related `Page` properties.
    """
    url: str
    ext: str
    width: int
    height: int

    @property
    def filename(self) -> Path:
        """
        Return the file name for this `Page` as Path object.
        Example
        -------
            >>> from hentai import Hentai
            >>> doujin = Hentai(177013)
            >>> [page.filename for page in doujin.pages]
            [WindowsPath('1.jpg'), WindowsPath('2.jpg'), ...]
        """
        num = Path(urlparse(self.url).path).name
        return Path(num).with_suffix(self.ext)

@unique
class Extension(Enum):
    """
    Known file extensions used by `nhentai` images.
    """
    JPG = 'j'
    PNG = 'p'
    GIF = 'g'

    @classmethod
    def convert(cls, key: str) -> str:
        """
        Convert Extension enum to its string representation.
        Example
        -------
            >>> from hentai import Extension
            >>> Extension.convert('j')
            '.jpg'
        """
        return f".{cls(key).name.lower()}"

@unique
class Format(Enum):
    """
    The title format. In some instances, `Format.Japanese` or `Format.Pretty` 
    return an empty string.
    """
    English = 'english'
    Japanese = 'japanese'
    Pretty = 'pretty'

class RequestHandler(object):
    _timeout = (5, 5)
    _total = 5
    _fake = Faker()

    def __init__(self, 
                timeout: Tuple[float, float]=_timeout, 
                total: int=_total):
        self.timeout = timeout
        self.total = total
    
    async def get(self, url: str, params: dict=None, **kwargs):
        response = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={ "User-Agent" : RequestHandler._fake.chrome(version_from=80, version_to=86, build_from=4100, build_to=4200) }) as response:
                if response.headers['content-type'] == 'application/json':
                    response.json = await response.json()
                if response.status == 404:
                    return None
        return response

class Hentai(object):
    HOME = "https://nhentai.net/" 
    _URL = urljoin(HOME, '/g/')
    _API = urljoin(HOME, '/api/gallery/')

    @classmethod
    async def init(cls, 
                id_: int=0, 
                timeout: Tuple[float, float]=RequestHandler._timeout, 
                total: int=RequestHandler._total,
                json: dict=None):
        """
        Start a request session and parse meta data from <https://nhentai.net> for this `id`.
        """
        self = Hentai()
        self.timeout = timeout
        self.total = total
        if id_ and not json:
            self.__id = id_
            self.__handler = RequestHandler(self.timeout, self.total)
            self.__url = urljoin(Hentai._URL, str(self.id))
            self.__api = urljoin(Hentai._API, str(self.id))
            self.__response = await self.__handler.get(self.api)
            if self.__response is None:
                return None
            self.__json = self.__response.json
        elif not id_ and json:
            self.__json = json
            self.__id = Hentai.__get_id(self.json)
            self.__url = Hentai.__get_url(self.json)
            self.__api = Hentai.__get_api(self.json)
        return self
    
    @staticmethod
    def __get_id(json: dict) -> int:
        """
        Return the ID of an raw nhentai response object.
        """
        return int(json['id'])

    @staticmethod
    def __get_url(json: dict) -> str:
        """
        Return the URL of an raw nhentai response object.
        """
        return urljoin(Hentai._URL, str(Hentai.__get_id(json)))

    @staticmethod
    def __get_api(json: dict) -> str:
        """
        Return the API access point of an raw nhentai response object.
        """
        return urljoin(Hentai._API, str(Hentai.__get_id(json)))

    @property
    def id(self) -> int:
        """
        Return the ID of this `Hentai` object.
        """
        return self.__id

    @property
    def url(self) -> str:
        """
        Return the URL of this `Hentai` object.
        """
        return self.__url

    @property
    def api(self) -> str:
        """
        Return the API access point of this `Hentai` object.
        """
        return self.__api

    @property
    def json(self) -> dict:
        """
        Return the JSON content of this `Hentai` object.
        """
        return self.__json

    def title(self, format_: Format=Format.English) -> str:
        """
        Return the title of this `Hentai` object. The format of the title
        defaults to `English`, which is the verbose counterpart to `Pretty`.
        """
        return self.json['title'].get(format_.value)

    @property
    def pages(self) -> List[Page]:
        """
        Return a collection of pages detailing URL, file extension, width and 
        height of this `Hentai` object.
        """
        pages = self.json['images']['pages']
        extension = lambda num: Extension.convert(pages[num]['t'])
        image_url = lambda num: f"https://i.nhentai.net/galleries/{self.media_id}/{num}{extension(num-1)}"
        return [Page(image_url(num + 1), Extension.convert(_['t']), _['w'], _['h']) for num, _ in enumerate(pages)]

    @property
    def media_id(self) -> int:
        """
        Return the media ID of this `Hentai` object.
        """
        return int(self.json['media_id'])

    @property
    def image_urls(self) -> List[str]:
        """
        Return all image URLs of this `Hentai` object, excluding cover and thumbnail.
        """
        return [image.url for image in self.pages]

    @property
    def num_pages(self) -> int:
        """
        Return the total number of pages of this `Hentai` object.
        """
        return int(self.json['num_pages'])

class Utils(object):
    """
    Hentai Utility Library
    ======================
    This class provides a handful of miscellaneous static methods that extend the 
    functionality of the `Hentai` class.
    Example 1
    ---------
        >>> from hentai import Utils
        >>> print(Utils.get_random_id())
        177013
    """
    @staticmethod
    async def get_random_id(handler=RequestHandler()) -> int:
        """
        Return a random ID.
        """
        response = await handler.get(urljoin(Hentai.HOME, 'random'))
        return int(str(response.url).split('/')[-2])

    @staticmethod
    async def get_random_hentai(handler=RequestHandler()) -> Hentai:
        """
        Return a random `Hentai` object.
        """
        return await Hentai.init(await Utils.get_random_id(handler))
