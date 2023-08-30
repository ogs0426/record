## ES 개선

1. 검색 정확도 개선
2. 유의어 사전
3. 사용자 사전
4. Tokenizer
5. 사용자 입력에 따른 검색어
6. 관련 검색어
7. 한글 토큰 1글자 제외

#### feature

해당 내용은 "Elastic Serach" spotv cache, client-api의 사용과 정책 확인 을 통한 개선을 위하여 작성 됩니다.

#### Tokenizer (common)

```json
		"tokenizer": {
			"seunjeon_default_tokenizer": {
				"type": "seunjeon_tokenizer",
				"index_eojeol": false
			},
		    "customer_ngram_tokenizer": {
				"type": "ngram",
				"min_gram": "4",
				"max_gram": "6"
		    }
		}
```

![img](https://t1.daumcdn.net/cfile/tistory/253F013E57F635032F?original)

#### mapper

##### Geting & Seting

| Properties         | analyzer (common)                    | filter (defalut : unique) | ETC                           |
| ------------------ | ------------------------------------ | ------------------------- | ----------------------------- |
| Team               | name, shortName, nameEn, shortNameEn |                           |                               |
| Game               |                                      |                           |                               |
| Live               | title                                | "custom_length_filter"    |                               |
| Video              | title, tags                          |                           |                               |
| Notice             | title, text                          |                           | title > c_filter : html_strip |
| QnA                | title, text                          |                           |                               |
| OriginalContentVod |                                      |                           |                               |

- 현제 사항

  - 모든 Properties가 세부적으로 옵션이 나누어져 있지 않음
  - Properties를 정책및 기능에 따라 분리 하여야 함

- Mapping 정책 수정 요망
  - "search_analyzer" 설정 요망 색인과 검색 정책을 분리
    https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-analyzer.html
  - "mapping fileds" type: keyword 분리 (캐릭터 필터와 토큰 필터 분리 가 필요 시 동일 Data 조회)
    https://www.elastic.co/guide/en/elasticsearch/reference/6.8/keyword.html

[Example Mapping analyzing 정책]

1. title
   2 plan "어절", "형태소"를 이용한 역인덱싱을 사용 때에 따라서 사용 하도록 한다.

### 1. Mapping Best Practices

엘라스틱에서 권장하는 방침은 아래와 같다.

- 직접 정의된 매핑을 사용하라 : 자동 매핑은 적절하지 않은 매핑을 만들어낸다.
- Index Template 을 사용하라 : Index를 추가할 때 기본적으로 적용될 템플릿을 만들어라.
- 모든 신규 템플릿에 적용될 디폴트 템플릿을 만들어라 : 즉 글로벌 세팅을 통해 신규로 추가되는 템플릿에 반드시 적용되도록 하라.
- 커스텀 anlyzer를 만들어 사용하라
- 싱슬 인덱스에 여러개의 타입(type)를 만들지 마라.

#### add idea

1. Char Filters 사전 전의는 크게 유효하지 않아보임 (특수문자 처리등에 대하여 "seunjeon_tokenizer", "standard" 의 tokenizer가 이미 대응함)
2. 기존 사용과는 분리 시킬것
   -3. 검색 Ketword와 Mapping 을 분리 -> 색인 검색시 해당 검색 "analyzer"을 기본으로 사용-
3. must -> should score 할당제 (일정 값 이상만 노출?)

##### Query (정확도 개선)

- Term > "search_key" 를 그대로 적용
  **검색어가 분석기를거쳐 토크나이징 없이 검색을 하지않는다**

  > 찾고자 하는 "properties"에 key 그대로 역 indexing

- Match > "search_key" 를 analyzer 이후 적용
  **토크나이징된 단어들을 찾아 문서들을 검색**하고 토크나이징된 **단어들이 최소 1개라도 들어있다면 검색 결과에 포함**

  > 찾고자 하는 "properties" 에서 "Key"를 분석 이후 역 indexing

- match_phrase 검색어의 순서를 보장 시킬때

- default analyzer -> "keyword"?

query용도 및 일치

Term : tag (정확한 키워드 일치)

Match : title 일치 여부 (Properties의 analysis 정도에 따라서 검색 키워드 타입의 수정이 필요)

match_phrase : 본문의 일치 여부 (위와 같음)

##### Token filter (정확도 기능 개선)

###### 1. 동의어 & 사용자 사전

```json
"synonyms": [
    	"맨유 => 맨체스터 유나이티드"
]
```

###### 2. 문자 검색

1. 정책적 (~어느정도 일치 시킨다, 키의 앞에서 부터 일치 시킨다.)
2. 검색, 텍스트 키워드 (~검색 키워드를 애널라이즈 시킬 것인가?, ~검색 텍스트를 애널라이즈 시킬 것인가?)

```json
"analysis": {
      "filter": {
        "ngram": {
          "type": "nGram",
          "min_gram": 2,
          "max_gram": 3
        }
      }
    }
```

```json
"analysis": {
      "filter": {
        "EDngram": {
          "type": "edgeNGram",
          "min_gram": 1,
          "max_gram": 3
        }
      }
    }
```

###### 3. 단어 검색

1. 검색 하고 하는 문장의 단어 일치 여부 (ngram을 단어로)

   example> "this is a pen" --(Analysis)--> ["this", "is", "a", "pen"]

```json
"analysis": {
      "filter": {
        "shingle": {
          "type": "shingle",
          "min_shingle_size": 3,
          "max_shingle_size": 4
        }
      }
    }
```

#### ### 개선 후 동작

1. 코비 브라이언, 손흥민 의 "코비". "흥민" 으로 해당 영상이 안 찾아 지는 증상 개선
2. 하이라이트 등의 영상을 풀 네임으로 색인 해야 하는 증상 개선
3. 음절로 찾을 수 없는 문제 개선
4.

##### 가중치 계산에 대하여...

#1 단순 가중치

```
 "fields": [ "title^3", "title.ko_ed_gram", "title.ko_ngram", "title.standard", "title.standard_ed" ]
```

#2 Score 합산 방식 변경

```
"type": "most_fields", (5개 필드 합산)
"type": "best_fields", (5개 필드 중 윈 퍼스트)
```

refs #1 : https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#query-dsl-multi-match-query

#### ETC

1. 추천 검색어

2. 한글 토큰 1글자 제외(ex : 거짓말 = 거짓 + 말)

   > 해당 이슈는 본문의 "Token filter"가 애널라이즈 가 된 이후 "검색 키워드"의 애널라이즈화를 확인 하고 수정

#### 환경 설정

1.

#### Example

##### Notice 검색 개선

어떠한 검색어를 주더라도 token값이 없으면 안된다. token 정도 확인

1. "**seunjeon_tokenizer**" 의 애널라이즈 상태 확인

   코비 브라이언트 기준 ["코비", "브라이언트"] > 코비 ["코", "비"]

   > 일반적으로 "analyzing" 된 필드에 같은 방법의 "analyzer"를 적용 하면 되나 "seunjeon" 같은 경우는 찾 을 수 없음 ( //"tokenizer" : "seunjeon_tokenizer", 은 한글 의미 중심으로 )

1. analyzing 정도 Check
   example API

   ```
   https://kibana-dev.spotvnow.co.kr/notice/_analyze

   {"analyzer":"korean", "text":"[서비스공지] 만우절(4.1, 월) 기념 '거짓말 같았던 경기' VOD 안내 "}
   ```

   ```json
   {
     "tokens": [
       {
         "token": "서비스/N",
         "start_offset": 1,
         "end_offset": 4,
         "type": "N",
         "position": 0
       },
       {
         "token": "공지/N",
         "start_offset": 4,
         "end_offset": 6,
         "type": "N",
         "position": 1
       },
       {
         "token": "만우/N",
         "start_offset": 8,
         "end_offset": 10,
         "type": "N",
         "position": 2
       },
       {
         "token": "절/N",
         "start_offset": 10,
         "end_offset": 11,
         "type": "N",
         "position": 3
       },
       {
         "token": "4/SN",
         "start_offset": 12,
         "end_offset": 13,
         "type": "SN",
         "position": 4
       },
       {
         "token": "1/SN",
         "start_offset": 14,
         "end_offset": 15,
         "type": "SN",
         "position": 5
       },
       {
         "token": "월/N",
         "start_offset": 17,
         "end_offset": 18,
         "type": "N",
         "position": 6
       },
       {
         "token": "기념/N",
         "start_offset": 20,
         "end_offset": 22,
         "type": "N",
         "position": 7
       },
       {
         "token": "거짓/N",
         "start_offset": 24,
         "end_offset": 26,
         "type": "N",
         "position": 8
       },
       {
         "token": "말/N",
         "start_offset": 26,
         "end_offset": 27,
         "type": "N",
         "position": 9
       },
       {
         "token": "같/V",
         "start_offset": 28,
         "end_offset": 29,
         "type": "V",
         "position": 10
       },
       {
         "token": "경기/N",
         "start_offset": 32,
         "end_offset": 34,
         "type": "N",
         "position": 11
       },
       {
         "token": "vod/SL",
         "start_offset": 36,
         "end_offset": 39,
         "type": "SL",
         "position": 12
       },
       {
         "token": "안내/N",
         "start_offset": 40,
         "end_offset": 42,
         "type": "N",
         "position": 13
       }
     ]
   }
   ```

**seunjeon_tokenizer**" 의 애널라이즈 상태 확인

Example>
코비 브라이언트 기준 ["코비", "브라이언트"] > 코비 ["코", "비"] -> 검색 불가

> 일반적으로 "standard, patten" 된 필드에 같은 방법의 "analyzer"를 적용 하면 되나 "seunjeon" 같은 경우는 찾을 수 없는 경우 ( //"tokenizer" : "seunjeon_tokenizer", 은 한글 사전상의 의미 중심으로 해석 된다.)

_정확도가 떨어진다고 생각 가능한 시나리오_

- 위와 같은 경우 "의미"가 없는 단어 [브라, 라이] 등의 문자 중심으로 검색 했을 경우 색인이 안됨

  -> analyzer : standard

- "코비" -> ["코", "비"] 와 같이 이름을 의미하나 "<space>" 영역 없이 "비" 라는 "사전상의 의미"가 따로 읽히는 경우
  ->

- "브라1" -> ["브라", "1"] "브라" 과 같이 첫 문자열이 사람이 해석했을 경우 우선 되나 색인이 안 되어 "1"의 내용만 읽히는 경우
  -> filter : edge

**ngram** 의 애널라이즈 상태 확인

Example>
"[코비 브라이언트 1주기 추모] 토론토 랩터스 : LA 레이커스 경기 생중계 안내"-> 검색 불가
-> ["[코비", "[코비 브", "[[코비 브라]", "코비 브" ... ]

> seunjeon_tokenizer로 찾지 못하는 색인을 찾기 위하여 추가 한뜻 보인다.
> -> 하지만 patten (" "split) 작업 을 거치지 않고 쪼개어서 색인의 의미가 분명치 않음

_정확도가 떨어진다고 생각 가능한 시나리오_

- "코비"로 찾을 경우 최소 단위 에서 나뉘어져 찾을 수 없음 (min-size 보다 작은 단어 색인 안됨)
  -> minsize 2 적용 (keyword 최소 2글자 이상 권장)
- -"[코비 브" 와 같이 색인 되지 않을 것으로 보이는 "token"이 많이 발생-
  -> ngram 삭제 또는 keyword 화
-

search ) 사전적의미 검색과 문자일치 검색 용도 분리

example ) "거짓말"

1. doc ["거짓", "말"]
   "거짓" 과 "말" 이 들어가는 문서 search
2. edgd ["거짓", "거짓말", "짓말"]
   "거짓말", "거짓" 이 들어가는 문서 search

위 와같은 경우는 우연한 일치로 검색 가능 할 수 있으나
사전적 의미가 없는 이름, 은어.. 은 search 가 힘들어진다.

example ) "코비 브라이언트"

1. doc ["코비/N", "브라이언트/N"] > split(" ") default
2. edgd ["코비", "브라이", "브라이언", "브라이언트"]

title등과 같은 문서를 찾을 경우 "2"번의 케이스가 더욱 유리
"라이" 와 같은 의미 없는 단어로 찾을 경우에도 2번의 경우는 찾아진다.

["Notice 검색 정확도" 개선 정책]
\1. 긴 문장, 문서로 이루어진 글의 사전적의미보다 해당 음절이 포함된 단어를 중점으로 찾도록 수정 -> "seunjeon" 행태소를 사용 할지 여부 결정 필요
\2. 검색 기준에 " "(공백) 이 들어 가지 않는 다는 전제 하에 어절으로 분리한다. -> Patten(" ")
\3. 중간 음절또한 검색에 이루어 질 수 있도록 음절별로 분리 -> filter(ngram, 2, 5) > 최소단위는 2개로 분리 최대 5개까지)5개가 넘어가는 어절이 많지 않음을 확인
\4. 검색 키워드는 중간 음절 부터 검색 할 필요가 없음 으로 첫 음절을 기준으로 찾는다. -> filter(edge, 2, 5)

##### VIdeos (tags)

tags 없음

수정 전

videossize: 49.0Mi (49.0Mi)docs: 43,611 (43,611)

수정 후

videossize: 48.9Mi (48.9Mi)docs: 43,611 (43,611)

videossize: 33.3Mi (33.3Mi)docs: 43,611 (43,611)

##### Team (ko, en)

team 없음

#### Ref

1. https://esbook.kimjmin.net/06-text-analysis/6.6-token-filter/6.6.4-ngram-edge-ngram-shingle

[add Ref # 1 사람의 언어 다루기] https://www.elastic.co/guide/en/elasticsearch/guide/2.x/languages.html

[ES 기능 개선]

- 유의어 검색 -> 문서 유사도(벡트 필드)
- 사용자 사전 -> 동의어
- 사용자 입력에 따른 추천 검색어(또는 초성 검색어) -> 자동 완성
- 관련 검색어 -> ETC

\1. 백트 필드 (유의어)

[Ref #1 벡터 필드를 사용한 텍스트 유사도 검색] https://www.elastic.co/kr/blog/text-similarity-search-with-vectors-in-elasticsearch

\2. filter:Synonym (동의어)

[Ref #1 synonym-tokenfilter] https://www.elastic.co/guide/en/elasticsearch/reference/6.8/analysis-synonym-tokenfilter.html

\3. Autocomplete (자동완성)

[Ref #1 prefix-query] https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html
[Ref #2 suggest - dev] https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
[Ref #3 started-search] https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-search.html

## ES 관리

##### Curator

- es **인덱스 관리** > waf log 삭제 주기 15 , 결재 로그 삭제 주기 45

https://docs.aws.amazon.com/ko_kr/elasticsearch-service/latest/developerguide/curator.html#curator-sample
