Java 에서 문자열을 다루를 대표적인 클래스로 
String , StringBuffer, StringBuilder 
가 있습니다. 

연산이 많지 않을때는 위에 나열된 어떤 클래스를 사용하더라도 이슈가 발생할 가능성은 거의 없습니다. 그러나 연산횟수가 많아지거나 멀티쓰레드, Race condition 등의 상황이 자주 발생 한다면 각 클래스의 특징을 이해하고 상황에 맞는 적절한 클래스를 사용해 주셔야 합니다!

### String  vs  StringBuffer/StringBuilder

String과 StringBuffer/StringBuilder 클래스의 가장 큰 차이점은 String은 **불변(immutable)** 의 속성을 갖는다는 점입니다.

새로운 메모리영역을 가리키게 변경되고 처음 선언했던 "hello"로 값이 할당되어 있던 메모리 영역은 Garbage로 남아있다가 GC(garbage collection)에 의해 사라지게 되는 것 입니다. String 클래스는 불변하기 때문에 문자열을 수정하는 시점에 새로운 String 인스턴스가 생성된 것이지요.

> String Pool 참조

> 불변 객체란? 
> 불변 객체(Immutable Object)란 객체 생성 이후 내부의 상태가 변하지 않는 객체이다.
> Thread-Safe 하여 병렬 프로그래밍에 유용하며 동기화를 고려하지 않아도 된다.

Java에서는 **가변(mutable)** 성을 가지는 StringBuffer / StringBuilder 클래스를 도입했습니다.

String 과는 반대로 StringBuffer/StringBuilder 는 가변성 가지기 때문에 .append() .delete() 등의 API를 이용하여 동일 객체내에서 문자열을 변경하는 것이 가능합니다. 따라서 문자열의 추가,수정,삭제가 빈번하게 발생할 경우라면 String 클래스가 아닌 StringBuffer/StringBuilder를 사용하셔야 합니다.

> 가변 성과 불변성에 따른 메모리의 참조 여부

### String Pool

Java String Pool
흔히 new 연산자로 String 객체를 생성하지 않는 것이 좋다는 말을 볼 수 있다.

 
![1](./img/StringPool.png)

String literal로 생성하면 해당 String 값은 Heap 영역 내 "String Constant Pool"에 저장되어 재사용되지만, new 연산자로 생성하면 같은 내용이라도 여러 개의 객체가 각각 Heap 영역을 차지하기 때문이다.


### Static Final 의 불변 가변 메모리 관리


### Refs

https://starkying.tistory.com/entry/what-is-java-string-pool

https://ifuwanna.tistory.com/221
