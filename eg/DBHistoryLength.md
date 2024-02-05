### History Length란?

Aurora MySQL은 On-premise MySQL 환경과 동일하게 REPEATABLE READ isolation level이 Default로 설정되어 있습니다. REPEATABLE READ 환경은 쿼리 실행 시점의 결과와, 실행 완료 시점의 결과가 동일해야 하기 때문에, 스냅샷 형태로 해당 시점의 결과를 저장하게 됩니다. 동시성이 높은 환경에서, 롱쿼리가 발생하게 되어 오랜 시간 시점데이터가 유지될수록, History Legnth 수치가 상승하게 됩니다.

History Length가 높아질수록, 오래된 데이터 스냅샷으로 인해 다른 조회 쿼리들도 시점 데이터를 통해 걸러내는 과정이 추가되면서, 검색 비효율이 발생하고 지연이 발생할 수 있습니다. 극단적으로 트래픽이 높은 서비스 환경에서는 약간의 지연으로 고객들의 불편함이 커지고, 서비스 장애의 원인이 될 수 있기 때문에, 모니터링해야 하는 필수적인 지표 중 하나입니다.

### 그러면 어떠한 영향이 발생 하는가?

https://m.blog.naver.com/parkjy76/221392765699