from typing import Optional, BinaryIO, Dict, Union

import requests
import aiohttp

from utils.saucenao.containers import SauceResponse
from utils.saucenao.params import _OutputType, DB, Hide, BgColor

class SauceNao:
    SAUCENAO_URL = 'https://saucenao.com/search.php'

    def __init__(self,
                api_key:  Optional[str] = None,
                *,
                testmode: int = 0,
                dbmask:   Optional[int] = None,
                dbmaski:  Optional[int] = None,
                db:       int = DB.ALL,
                numres:   int = 6,
                frame:    int = 1,
                hide:     int = Hide.NONE,
                bgcolor:  int = BgColor.NONE,
                ) -> None:

        params: Dict[str, Union[str, int]] = {}

        if api_key is not None:
            params['api_key'] = api_key
        if dbmask is not None:
            params['dbmask'] = dbmask
        if dbmaski is not None:
            params['dbmaski'] = dbmaski

        params['testmode'] = testmode
        params['db'] = db
        params['numres'] = numres
        params['hide'] = hide
        params['frame'] = frame
        params['bgcolor'] = bgcolor               # from https://saucenao.com/testing/
        params['output_type'] = _OutputType.JSON
        self.params = params

    async def from_file(self, file: BinaryIO) -> SauceResponse:
        return await self._search(self.params, {'file': file})

    async def from_url(self, url: str) -> SauceResponse:
        params = self.params.copy()
        params['url'] = url
        return await self._search(params)

    async def _search(self, params, files=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.SAUCENAO_URL, data=params) as resp:
                status_code = resp.status

                if status_code == 200:
                    raw = await self._verify_response(await resp.json(), params)
                    return SauceResponse(raw)

                # Taken from https://saucenao.com/tools/examples/api/identify_images_v1.1.py
                # Actually server returns 200 and user_id=0 if key is bad
                elif status_code == 403:
                    # raise BadKeyError('Invalid API key')
                    print('Invalid API key')
                    return {}

                elif status_code == 413:
                    return self.msg('File is too large')

                elif status_code == 429:
                    if 'Daily' in await (resp.json())['header']['message']:
                        return self.msg('24 hours limit reached')
                    return self.msg('30 seconds limit reached')

                return self.msg(f'Server returned status code {status_code}')

    @staticmethod
    async def _verify_response(parsed_resp, params):
        resp_header = parsed_resp['header']

        status = resp_header['status']
        user_id = int(resp_header['user_id'])

        # Taken from https://saucenao.com/tools/examples/api/identify_images_v1.1.py
        if status < 0:
            return SauceNao.msg('Unknown client error, status < 0')
        elif status > 0:
            return SauceNao.msg('Unknown API error, status > 0')
        elif user_id < 0:
            return SauceNao.msg('Unknown API error, user_id < 0')

        # Request passed, but api_key was ignored
        elif user_id == 0 and 'api_key' in params:
            # raise BadKeyError('Invalid API key')
            print('Invalid API key')
            return {}

        long_remaining = resp_header['long_remaining']
        short_remaining = resp_header['short_remaining']

        # Taken from https://saucenao.com/tools/examples/api/identify_images_v1.1.py
        if short_remaining < 0:
            return SauceNao.msg('30 seconds limit reached')
        elif long_remaining < 0:
            return SauceNao.msg('24 hours limit reached')

        return parsed_resp

    @staticmethod
    def msg(msg):
        return {'message': msg}