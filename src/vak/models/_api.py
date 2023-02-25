from .das import DAS
from .tweetynet import TweetyNet
from .teenytweetynet import TeenyTweetyNet


# TODO: Replace constant with decorator that registers models, https://github.com/vocalpy/vak/issues/623
BUILTIN_MODELS = {
    'DAS': DAS,
    'TweetyNet': TweetyNet,
    'TeenyTweetyNet': TeenyTweetyNet
}

MODEL_NAMES = list(BUILTIN_MODELS.keys())
