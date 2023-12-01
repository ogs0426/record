## DA (Developer - Associate)

https://aws.amazon.com/ko/certification/certified-developer-associate/?c=sec&sec=resources

AWS Certified Developer - Associate Official Practice Question Set
https://awscertificationpractice.benchprep.com/app/aws-certified-developer-associate-official-practice-question-set-dva-c02?locale=ko-kr#exams/take_exam/168411

> 20개의 문항만 기본 제공



### AWS 교육 권장 사항

시험 준비를 위해 다음 모듈로 이동하기 전에 다음 교육(또는 유사한 과정)을 완료하는 것이 좋습니다. 시험에 응시하기 전에 특정 교육을 받을 것을 요구하지는 않습니다.

[AWS 기술 에센셜](https://explore.skillbuilder.aws/learn/course/external/view/elearning/1851/aws-technical-essentials?da=sec&sec=prep)

[AWS Elastic Beanstalk 소개](https://explore.skillbuilder.aws/learn/course/external/view/elearning/184/introduction-to-aws-elastic-beanstalk?da=sec&sec=prep)

[컨테이너 소개](https://explore.skillbuilder.aws/learn/course/external/view/elearning/106/introduction-to-containers?da=sec&sec=prep)

[서버리스 개발 소개](https://explore.skillbuilder.aws/learn/course/external/view/elearning/37/introduction-to-serverless-development?da=sec&sec=prep)

[Amazon Elastic Container Services(ECS) 입문서](https://explore.skillbuilder.aws/learn/course/external/view/elearning/91/amazon-elastic-container-service-ecs-primer?da=sec&sec=prep)

[Amazon Elastic Kubernetes Service(EKS) 입문서](https://explore.skillbuilder.aws/learn/course/external/view/elearning/57/amazon-elastic-kubernetes-service-eks-primer?da=sec&sec=prep)

[AWS에서 DevOps 시작하기](https://explore.skillbuilder.aws/learn/course/external/view/elearning/2000/getting-started-with-devops-on-aws?da=sec&sec=prep)

[AWS 기반 개발(유료 강의실 교육)](https://aws.amazon.com/training/classroom/developing-on-aws/?da=sec&sec=prep)





### 하얀 종이

시험과 관련된 AWS 백서를 탐색하여 AWS 서비스와 모범 사례를 알아보세요.

* [AWS Well-Architected 프레임워크](https://aws.amazon.com/architecture/well-architected/?da=sec&sec=prep)
* [AWS에서 지속적인 통합 및 지속적인 전달 실행](https://d1.awsstatic.com/whitepapers/DevOps/practicing-continuous-integration-continuous-delivery-on-AWS.pdf) 
* [AWS의 마이크로서비스](https://d1.awsstatic.com/whitepapers/microservices-on-aws.pdf) 
* [AWS Lambda를 사용한 서버리스 아키텍처](https://d1.awsstatic.com/whitepapers/serverless-architectures-with-aws-lambda.pdf) 
* [서버리스 아키텍처로 기업 경제성 최적화](https://d1.awsstatic.com/whitepapers/optimizing-enterprise-economics-serverless-architectures.pdf) 
* [AWS에서 컨테이너화된 마이크로서비스 실행](https://d1.awsstatic.com/whitepapers/DevOps/running-containerized-microservices-on-aws.pdf) 
* [AWS에서의 블루/그린 배포](https://d1.awsstatic.com/whitepapers/AWS_Blue_Green_Deployments.pdf) 



### Qna

- [아마존 SQS](https://aws.amazon.com/sqs/faqs/?da=sec&sec=prep)
- [아마존 다이나모DB](https://aws.amazon.com/dynamodb/faqs/?da=sec&sec=prep)
- [아마존 엘라스티캐시](https://aws.amazon.com/elasticache/faqs/?da=sec&sec=prep)
- [아마존 키네시스](https://aws.amazon.com/kinesis/data-streams/faqs/?da=sec&sec=prep)
- [AWS 람다](https://aws.amazon.com/lambda/faqs/?da=sec&sec=prep)
- [아마존 API 게이트웨이](https://aws.amazon.com/api-gateway/faqs/?da=sec&sec=prep)
- [AWS 엘라스틱 빈스토크](https://aws.amazon.com/elasticbeanstalk/faqs/?da=sec&sec=prep)
- [AWS ID 및 액세스 관리](https://aws.amazon.com/iam/faqs/?da=sec&sec=prep)
- [AWS 키 관리 서비스](https://aws.amazon.com/kms/faqs/?da=sec&sec=prep)





### 오답 노트

####  EFS 와 Lambda의 이벤트 호출을 통한 연결의 이해

```
 Lambda 함수는 Amazon EFS 파일 시스템에 연결할 수 있습니다. 그러나 Amazon EFS 파일 시스템 변경은 Lambda 함수를 호출할 수 없습니다.

Amazon EFS에서 Lambda 함수를 사용하는 방법에 대한 자세한 내용은 Lambda에서 Amazon EFS 사용을 참조하세요.


 Lambda 함수는 S3 이벤트에서 호출할 수 있으며 S3 버킷에서 읽을 수 있습니다. 이벤트 기반 호출을 사용하면 S3 객체가 도착하는 즉시 처리될 수 있습니다.

S3에서 Lambda 함수를 호출하는 방법에 대한 자세한 내용은 튜토리얼: Amazon S3 트리거를 사용하여 Lambda 함수 호출을 참조하세요.
```



#### DynamoDB 



DynamoDB 스캔 작업으로 검색해야 하는 최대 항목 수를 설정하려면 limit 파라미터를 1로 설정합니다.

스캔에서 결과 수를 제한하는 방법에 대한 자세한 내용은 [결과 집합의 항목 수 제한](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.Limit)을 참조하세요.

DynamoDB에서 쿼리 필터 표현식 문을 사용하는 방법에 대한 자세한 내용은 [Query(쿼리)](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html)를 참조하세요.

DynamoDB에서 쿼리 필터 표현식 문을 사용하는 방법에 대한 자세한 내용은 [Query(쿼리)](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html)를 참조하세요.



##### DynamoDB Streams

DynamoDB Streams 사용에 대한 자세한 내용은 [DynamoDB Streams 및 AWS Lambda 트리거](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html)를 참조하세요.



##### Encryption Client

DynamoDB Encryption Client가 사용하는 직접 KMS 자료 공급자에 대한 자세한 내용은 [Direct KMS Materials Provider(직접 KMS 자료 공급자)](https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/direct-kms-provider.html)를 참조하세요.

KMS 키에 대한 자세한 내용은 [AWS KMS 개념](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys)을 참조하세요.



DynamoDB 클라이언트 측 및 서버 측 암호화에 대한 자세한 내용은 [Client-Side and Server-Side Encryption(클라이언트 측 및 서버 측 암호화)](https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/client-server-side.html)을 참조하세요.

DynamoDB Encryption Client에 대한 자세한 내용은 [What Is the Amazon DynamoDB Encryption Client?(Amazon DynamoDB Encryption Client란 무엇입니까?)](https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/what-is-ddb-encrypt.html)를 참조하세요.

DynamoDB Encryption Client의 작동 방식에 대한 자세한 내용은 [How the DynamoDB Encryption Client Works(DynamoDB Encryption Client 작동 방식)](https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/how-it-works.html)를 참조하세요.



```
 AWS KMS를 사용하도록 DynamoDB Encryption Client를 구성하면 DynamoDB Encryption Client는 AWS KMS 외부에서 사용될 경우 항상 암호화되는 KMS 키를 사용합니다. 이 암호화 자료 공급자는 각 테이블 항목에 대해 고유한 암호화 키 및 서명 키를 반환합니다. 이 암호화 방법에는 비대칭 키가 아닌 대칭 KMS 키가 필요합니다.
```





####  AWS Step Functions

HeartbeatSeconds 속성에 대한 자세한 내용은 [활동 태스크가 완료될 때까지 대기](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html#activities-wait)를 참조하세요.

Retry(재시도) 필드에 대한 자세한 내용은 [Error Handling in Step Functions(Step Functions의 오류 처리)](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)를 참조하세요.

```
오류 처리에 대한 자세한 내용은 Error Handling in Step Functions(Step Functions의 오류 처리)를 참조하세요.
```



#### AWS System Parameter Store

Parameter Store를 사용하면 API 키와 같은 파라미터를 쉽게 외부화할 수 있습니다. 보안 문자열 옵션은 저장된 값을 암호화하여 데이터 보안을 제공합니다. 파라미터에 대한 권한이 부여된 액세스는 IAM 권한에 의해 관리됩니다. 파라미터 값은 함수를 다시 배포하지 않아도 언제든지 권한 있는 보안 주체가 쉽게 변경할 수 있습니다. 단, 함수가 파라미터 값을 다시 읽으려면 인텔리전스가 필요합니다.

Parameter Store에 대한 자세한 내용은 [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)를 참조하세요.

보안 문자열 옵션에 대한 자세한 내용은 [Systems Manager의 보안 모범 사례](https://docs.aws.amazon.com/systems-manager/latest/userguide/security-best-practices.html)를 참조하세요.

파라미터 액세스에 IAM 권한 부여를 요구하는 방법에 대한 자세한 내용은 [IAM 정책을 사용하여 Systems Manager 파라미터에 대한 액세스 제한](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html)을 참조하세요.



#### Lambda

```
B Lambda 별칭을 새 버전의 Lambda 함수로 지정합니다. (o)

D Lambda 별칭을 새 Lambda 함수 별칭으로 지정합니다. (x)
```

> 아니 말 장난 하냐...

이벤트 소스 매핑에서 Lambda 함수에 ARN을 사용하는 대신 별칭 ARN을 사용할 수 있습니다. 새 버전을 승격하거나 이전 버전으로 롤백할 때 이벤트 소스 매핑을 업데이트할 필요가 없습니다.

Lambda 함수 별칭 생성 및 사용에 대한 자세한 내용은 [Lambda 함수 별칭](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)을 참조하세요.



#### AWS SAM



AWS SAM CLI를 사용하여 애플리케이션을 배포하는 방법에 대한 자세한 내용은 [sam deploy(sam 배포)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)를 참조하세요.



#### Secrets Manager



정답입니다. API 키 회전(Lambda 함수를 사용한 서드 파티 키 회전 포함)은 Secrets Manager에서 사용할 수 있습니다

서드 파티 비밀을 회전하는 방법에 대한 자세한 내용은 [회전 작동 방식](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html)을 참조하세요.

-------

