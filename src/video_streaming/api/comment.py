from fastapi import APIRouter
from collections import defaultdict


table = defaultdict(dict)
table['0001'] = {
    'totalCount': 635733,
    'commentArr': [
        {
            'comment': '''
@ChillVibesStation97 3개월 전
0:00    LANY - Anything 4 u 
0:0:12  LANY - Anything 4 u 
02:14   LANY - you!
2:14    LANY - you!
            ''',
            'src': 'https://yt3.ggpht.com/2HOGEbS4V-u8tiQ6k6RmEbMa2oZJuigscOP1WomUbE6zJ1DvGWXCYS1z2koZUKJDURdVs_CwDw=s88-c-k-c0x00ffffff-no-rj',
        },
        {
            'comment': '''
@ChillVibesStation97 3개월 전
진찌 행복 별거없네요 깨끗하게 씻고 창문열어놓고 포근한 이블속에서 좋아는 향수 뿌려주고 이어폰끼고 들으니까 넘 행복한거같아요 진찌루
이거 읽으시는 분들도 오늘보다 더행복한 내일이었으면 좋겠어요!
            ''',
            'src': 'https://yt3.ggpht.com/Gs5RZTP9_2qb-2ItAy2ZZrKfSGAKoAUCNJjiG_sNkrdpvxrXKRni_8BMDxvgKdlf2FwdhyE=s88-c-k-c0x00ffffff-no-rj',
        },
        {
            'comment': '''
@ummmmmmum 4개월 전
아니 제가 좋아하는 가수 다 모아놓으면 당연히 좋을 수 밖에... 레이니, 콜플, 라우브 노래 진짜 좋아요 ㅠㅠ
            ''',
            'src': 'https://yt3.ggpht.com/ytc/AIdro_lPZ02ITT9XKLBu5yfEZsM6uHNJ9VleTrmdVacaB69VPnM=s88-c-k-c0x00ffffff-no-rj',
        },
    ],
};

router = APIRouter()

filter_words = {'comment'}
def stripValue(json_data: dict):
    result = dict()
    for key, val in json_data.items():
        if key in filter_words:
            result[key] = val.strip()
        elif isinstance(val, dict):
            result[key] = stripValue(val)
        elif isinstance(val, list):
            result[key] = [stripValue(item) for item in val]
        else:
            result[key] = val
    return result

@router.get("/{video_id}")
async def get_comments(video_id: str):
    result = {'videoId': video_id}
    
    quired = table.get(video_id, dict())
    quired = stripValue(quired)
    
    result.update(quired)
    return result
