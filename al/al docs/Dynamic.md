### Dynamic Programming

> (특히 최적화 문제, 조합 문제, 피보나치 수열 계산, 최장 공통 부분 수열(LCS) 찾기, 0-1 배낭 문제, 그래프 경로 찾기)

다이나믹 프로그래밍(Dynamic Programming)은 문제를 여러 하위 문제로 나누고, 그 하위 문제들의 결과를 저장하며 효율적으로 해결하는 알고리즘 기법입니다. 이를 통해 중복 계산을 피하고, 계산 속도를 대폭 향상시킬 수 있습니다. 다이나믹 프로그래밍은 큰 문제를 작은 하위 문제로 나누어 해결하며, 작은 문제의 해결 결과를 이용하여 큰 문제를 해결하는 Bottom-up 방식과, 큰 문제를 작은 하위 문제로 쪼개어 해결하는 Top-down 방식으로 구현할 수 있습니다.

다이나믹 프로그래밍의 주요 아이디어는 "Memoization"과 "Optimal Substructure"입니다. Memoization은 작은 하위 문제의 해결 결과를 저장하여 중복 계산을 피하는 기법을 의미하며, Optimal Substructure는 큰 문제의 최적해가 작은 하위 문제의 최적해로부터 구성될 수 있는 성질을 의미합니다.

다이나믹 프로그래밍은 다양한 문제에 적용될 수 있으며, 특히 최적화 문제나 조합 문제 등에 주로 사용됩니다. 예를 들어, 피보나치 수열 계산, 최장 공통 부분 수열(LCS) 찾기, 0-1 배낭 문제, 그래프 경로 찾기 등에 다이나믹 프로그래밍을 적용할 수 있습니다.

다음은 다이나믹 프로그래밍을 사용하여 피보나치 수열을 계산하는 예제 코드입니다.

---

```java
public class Solution {
    public static int fibonacci(int n) {
        if (n <= 1) {
            return n;
        }

        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;

        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }

        return dp[n];
    }

    public static void main(String[] args) {
        int n = 10;
        int result = fibonacci(n);
        System.out.println("Fibonacci(" + n + ") = " + result);
    }
}

```
