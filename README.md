# 검색 서비스 상품 검색 구현 과제

주어진 요구 사항을 만족하는 검색 서비스를 구현합니다.

## 실행 방법

1. 개발 환경 설치
    1. Docker 설치
        - [Get Docker](https://docs.docker.com/get-docker/)
    2. MySQL Shell 설치
        - [Installing MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)
        - 설치된 mysql의 경로를 PATH 환경변수에 등록
2. Docker Compse로 개발 환경 실행
    ```shell
    > docker compose up
    ```
3. MySQL에 더미 데이터 로드
    ```shell
    > mysql -h 127.0.0.1 -u root -proot -e "CREATE DATABASE ap"
    > mysql -h 127.0.0.1 -u root -proot ap < /Users/edenyoon/Projects/ap-search/data/category_insert_20200407.sql
    > mysql -h 127.0.0.1 -u root -proot ap < /Users/edenyoon/Projects/ap-search/data/product_insert_20200407.sql
    ```
4. Product 인덱스 생성
    ```shell
    > docker exec -it ap-web /bin/ash -c "python tasks/update_products.py"
    ```
5. 검색 API로 검색 테스트
    - 상품 검색 API
        - http://127.0.0.1:5000/search/v1/product?keyword=keyword
    - ex) [손크림](http://127.0.0.1:5000/search/v1/product?keyword=손크림)
