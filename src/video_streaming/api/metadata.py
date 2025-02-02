from fastapi import APIRouter
from collections import defaultdict


table = defaultdict(dict)
table['0001'] = {
    'title': 'ROSÉ & Bruno Mars - APT. (Official Music Video)',
    'publisher': 'ROSÉ',
    'numDescripter': 15800000,
    'numLikes': 13450000,
    'bdsrc': 'https://yt3.ggpht.com/qjsflFmyakGs5ekX8fPsDNfuKABx-yxIDrv-4ooPAFcZ6JUUpUPlue7g_d-VAk2YAiYR-0yr=s48-c-k-c0x00ffffff-no-rj',
};

router = APIRouter()

@router.get("/{video_id}")
async def get_metadata(video_id: str):
    result = {'videoId': video_id}
    
    quired = table.get(video_id, dict())
    result.update(quired)
    return result
