import re

# 간단한 이메일 정규식 (실무용 간단 검사, RFC 완전 준수 아님)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(email: str) -> bool:
    """이메일 주소가 패턴에 맞으면 True, 아니면 False."""
    return bool(EMAIL_RE.match(email))

# 샘플 이메일 10개 (유효/무효 혼합)
samples = [
    "user@example.com",                        # valid
    "user.name+tag@example.co.uk",             # valid
    "user_name@example.io",                    # valid
    "user-name@sub.domain.com",                # valid
    "user@localhost",                          # invalid (TLD 없음)
    "user@.com",                               # invalid (도메인 시작 점)
    "@example.com",                            # invalid (로컬 파트 없음)
    "user@exam_ple.com",                       # invalid (도메인에 밑줄)
    "user..dot@example.com",                   # invalid (로컬 파트 연속 점; regex는 쉽게 잡지 못할 수 있음)
    "user@-example.com"                        # invalid (도메인 레이블이 하이픈으로 시작)
]

if __name__ == "__main__":
    for e in samples:
        print(f"{e:40} -> {'VALID' if is_valid_email(e) else 'INVALID'}")