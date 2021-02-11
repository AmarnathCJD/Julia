import asyncio
import hashlib
import inspect
import math
import os
import logging
from collections import defaultdict
from typing import (AsyncGenerator, Awaitable, BinaryIO, DefaultDict, List,
                    Optional, Tuple, Union)

from telethon import TelegramClient, helpers, utils
from telethon.crypto import AuthKey
from telethon.network import MTProtoSender
from telethon.tl.functions.auth import (ExportAuthorizationRequest,
                                        ImportAuthorizationRequest)
from telethon.tl.functions.upload import (GetFileRequest,
                                          SaveBigFilePartRequest,
                                          SaveFilePartRequest)
from telethon.tl.types import (Document, InputDocumentFileLocation, InputFile,
                               InputFileBig, InputFileLocation,
                               InputPeerPhotoFileLocation,
                               InputPhotoFileLocation, TypeInputFile)

TypeLocation = Union[Document, InputDocumentFileLocation, InputPeerPhotoFileLocation,
                     InputFileLocation, InputPhotoFileLocation]

async def upload_file(client: TelegramClient,
                      file: BinaryIO,
                      file_name: str,
                      progress_callback: callable = None) -> TypeInputFile:
    res = (await _internal_transfer_to_telegram(client, file, progress_callback, file_name))[0]
    return res
async def download_file(client: TelegramClient,
                        location: TypeLocation,
                        out: BinaryIO,
                        progress_callback: callable = None
                        ) -> BinaryIO:
    size = location.size
    dc_id, location = utils.get_input_location(location)
    # We lock the transfers because telegram has connection count limits
    downloader = ParallelTransferrer(client, dc_id)
    downloaded = downloader.download(location, size)
    async for x in downloaded:
        out.write(x)
        if progress_callback:
            r = progress_callback(out.tell(), size)
            if inspect.isawaitable(r):
                await r

    return out
