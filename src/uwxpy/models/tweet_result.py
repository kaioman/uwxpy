from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Any

@dataclass
class TweetResult:
    
    status: Optional[HTTPStatus]
    """ HTTPステータスコード """

    tweet_id: Optional[str]
    """ TweetID """
    
    media_id: Optional[str]
    """ MediaID """
    
    raw: Optional[Any]
    """ rawデータ """