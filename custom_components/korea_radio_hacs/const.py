DOMAIN = 'korea_radio'
TITLE  = 'Korea Radio'

CONF_HOST = "host"
CONF_TOKEN = "token"

DEFAULT_TOKEN = "homeassistant"

# Backward compatibility mapping for channel keys
CHANNEL_MAPPING = {
    "YTN": "ytn", "TBS": "tbs", "TBN": "tbn", "ITV": "ifm", "KFN": "kfn",
    "OBS": "obs", "WBS": "wbs", "CBSMusic": "cbs_music", "CBSFM": "cbs_fm",
    "SBSPowerFM": "sbs_power", "SBSLoveFM": "sbs_love", "KBSCoolFM": "kbs_cool",
    "KBSHappyFM": "kbs_happy", "KBSClassic": "kbs_classic", "KBS1FM": "kbs_1radio",
    "KBS3FM": "kbs_3radio", "MBCFM": "mbc_fm", "MBCFM4U": "mbc_fm4u", "EBSFM": "ebs",
}

# Media Source types
MEDIA_TYPE_RADIO = "radio"
