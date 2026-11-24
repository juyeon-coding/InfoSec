from dataclasses import dataclass

@dataclass
class IPFragment:
    identification: int
    offset: int
    payload: bytes
    more_fragments: bool

    @property
    def end_offset(self) -> int:
        # 시작 오프셋(바이트 단위) + 페이로드 길이를 더하면 끝나는 위치(End Offset)
        return self.offset + len(self.payload)


class ReassemblyError(Exception):
    """조각 재조립 과정에서 발생하는 충돌/오류"""


# IP 패킷 조각 하나를 헤더 필드 + 페이로드로 표현
pkt1 = {
    "id": 54321,            # Identification (같은 원본 패킷 조각인지 구분)
    "flags_mf": True,       # More Fragments (True면 뒤에 조각이 더 있음)
    "frag_offset": 0,       # Fragment Offset (8바이트 단위 기준 -> 0 * 8 = 0바이트)
    "payload": b"01234567",  # 바이트 데이터 
}

pkt2 = {
    "id": 54321,
    "flags_mf": False,      # 마지막 조각
    "frag_offset": 1,       # 1 * 8 = 8바이트부터 시작!
    "payload": b"WXYZ1234",    # 8바이트 데이터 (8 ~ 16바이트 차지)
}

# 딕셔너리를 IPFragment 객체로 변환
frag1 = IPFragment(
    identification=pkt1["id"],
    offset=pkt1["frag_offset"] * 8,
    payload=pkt1["payload"],
    more_fragments=pkt1["flags_mf"],
)

frag2 = IPFragment(
    identification=pkt2["id"],
    offset=pkt2["frag_offset"] * 8,
    payload=pkt2["payload"],
    more_fragments=pkt2["flags_mf"],
)

# 같은 ID이고 두 번째 조각 시작 위치가 첫 번째 조각 끝 위치보다 앞이면 겹침
if frag1.identification == frag2.identification and frag2.offset < frag1.end_offset:
    overlap_bytes = frag1.end_offset - frag2.offset
    print(f"겹침 발생! {overlap_bytes}바이트 겹침 (첫 번째 끝: {frag1.end_offset})")

else:
    print("겹침 없음, 정상적으로 재조립 가능")