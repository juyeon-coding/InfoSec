## IP Fragmentation 기반 공격 정리

### 1. 개념 배경
- 네트워크 패킷이 경로의 **MTU(Maximum Transmission Unit)** 보다 클 경우 IP 단편화(Fragmentation)가 발생하며, 분할 및 재조립은 **Identification**, **Flags(MF 등)**, **Fragment Offset** 필드를 통해 이루어진다.

### 2. Teardrop 공격
- **핵심 원리**: 단편화된 패킷들의 **Fragment Offset**(및 길이)이 비정상적으로 **겹치거나(Overlap) 역전**되도록 조작하여, 수신 측 재조립 과정에서 커널/스택 예외나 오류를 유발해 **서비스 거부(DoS)**를 일으키는 공격.
- **우회·변형 기법**:
  1. **Tiny Fragment**: 첫 번째 조각(또는 헤더/상위 프로토콜 정보가 걸리는 조각)을 아주 작게 만들어, 포트/헤더 정보를 온전히 보지 못하는 패킷 필터링·IDS를 우회하려는 시도.
  2. **Fragment Overlap**: 조각 간 오프셋을 겹치게 구성해, 장비(IDS/방화벽)의 재조립·덮어쓰기(Overwrite) 해석 방식과 실제 호스트의 재조립 해석 차이를 노리거나 재조립 오류를 유발하는 방식.

### 3. Ping of Death (비교 정리)
- ICMP Echo Request 등을 조각내어 전송하되, 재조립된 IP 패킷 전체 크기가 허용 한계(65,535바이트)를 넘기도록 구성해 수신 시스템의 재조립 버퍼 오류·마비(DoS)를 유발하는 공격.
