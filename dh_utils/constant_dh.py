RCPNO_REGEX: str = r'''node[0-9]\['rcpNo'\]\s*=\s*"[0-9]*"'''
DCMNO_REGEX: str = r'''node[0-9]\['dcmNo'\]\s*=\s*"[0-9]*"'''
ELEID_REGEX: str = r'''node[0-9]\['eleId'\]\s*=\s*"[0-9]*"'''

OG_URL = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcpno}"
SRC_URL = "https://dart.fss.or.kr/report/viewer.do?rcpNo={rcpno}&dcmNo={dcmNo}&eleId={id}&offset=800&length=4053&dtd=dart3.xsd"
