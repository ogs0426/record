## 정리

순간의 최적의 해를 구해 결과를 도출하는 법

위의 예제에서 알수 있듯, Greedy 알고리즘은 최적의 방법은 아니다!

단, 모든 노드를 탐색하지 않기 때문에 빠른 속도로 해를 구할수 있다는 장점을 가지고 있다.

탐욕법은 최적의해를 구하는 방법이 아니지만 코딩테스트에서 종종 출제되는 유형이다.

그렇다면 탐욕법을 이용하여 어떤 문제들을 접근하는게 좋은지 알아보자.

### 문제

- 거스름 돈 문제

### 정리

```java
package test;

import java.lang.reflect.Array;
import java.util.*;

class Solution {
    public static long candies(int n, int[] arr) {
        long answer = n;

        int[] num = new int[n];

        // i는 0부터 n-1까지 , 다음수가 크면 num[i+1] =num[i]+1
        for(int i=0;i<n-1;i++){
            if(arr[i+1]>arr[i]){
                num[i+1] = num[i]+1;
            }
        }

        // i는 n-1부터 0까지, 이전수가 크면 num[i]+1와 num[i-1]중의 큰수를 선택
        for(int i=n-1;i>=1;i--) {
            if(arr[i] < arr[i-1]) {
                num[i-1] = Math.max(num[i]+1, num[i-1]);
            }
        }
        for(int i : num) {
        //	System.out.println(i);
            answer +=i;
        }
            System.out.println("answer : "+answer);
            return answer;
    }

    public static void main(String[] args) {
        Solution Test = new Solution();

        System.out.println("Test START");
        int n = 8;
        int[] arr = {2,4,3,5,2,6,4,5};
        // 출력
        long answer = candies(n, arr);

        System.out.println(answer);

        System.out.println("Test END");
    }

}
```

### REF

https://eocoding.tistory.com/26
