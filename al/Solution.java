import java.lang.*;
import java.util.*;

public class Solution {
    
    public static String bfs(int start, int[][] graph, boolean[] visited) {
		// 탐색 순서를 출력하기 위한 용도
		StringBuilder sb = new StringBuilder();
		// BFS에 사용할 큐를 생성해줍니다.
		Queue<Integer> q = new LinkedList<Integer>();

		// 큐에 BFS를 시작 할 노드 번호를 넣어줍니다.
		q.offer(start);

		// 시작노드 방문처리
		visited[start] = true;

		// 큐가 빌 때까지 반복
		while(!q.isEmpty()) {
			int nodeIndex = q.poll();
			sb.append(nodeIndex + " -> ");
			//큐에서 꺼낸 노드와 연결된 노드들 체크
			for(int i=0; i<graph[nodeIndex].length; i++) {
				int temp = graph[nodeIndex][i];
                
				// 방문하지 않았으면 방문처리 후 큐에 넣기
				if(!visited[temp]) {
					visited[temp] = true;
					q.offer(temp);
				}
			}
		}
		// 탐색순서 리턴
		return sb.toString() ;
	}

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

    /**
     * arr : 탐색 대상
     * out : 결과
     * visited : 탐색 여부
     * depth : 현재 값
     * r : 결과 목표 값
     *
     */
    public static void permutation(int[] arr, int[] out, boolean[] visited, int depth, int r) {

        if(depth == r) {
            for(int num: out) System.out.print(num);
            System.out.println();
            return;
        }

        for(int i=0; i<arr.length; i++) {

            // 탐색 하지 않은 경우 에만
            if(!visited[i]){
                visited[i] = true;

                // 결과 등록
                out[depth] = arr[i];
                permutation(arr, out, visited, depth+1, r);
                visited[i] = false;
            }
        }
    }

    // 반복문을 이용
    public static int binarySearch_loop(int[] arr, int target) {
        Arrays.sort(arr);		// 0번 과정 : 오름차순 정렬

        int low = 0;
        int high = arr.length-1;
        int mid = 0;

        // 제일 작은수가 큰수보다 커지면 탐색 종료
        while(low <= high) {
            mid = (low + high) /2;		// 1번 과정 : 중앙값 찾기

            if(arr[mid] == target) {
                return mid;
            }else if(arr[mid] > target) {	// 현재의 중앙값보다 작으면,
                high = mid-1;		// 왼쪽요소를 선택하기 위해 high = mid -1로 설정
            }else {
                low = mid+1;		// 현재의 중앙값보다 크면, 오른쪽 요소를 선택하기 위해 low = mid+1로 설정
            }
        }
        // 탐색해도 결과가 없는 경우
        return -1;

    }


    public static void main2(String[] args) {
        // 근접 노드 표현
		int[][] graph = {{}, {2,3,8}, {1,6,8}, {1,5}, {5,7}, {3,4,7}, {2}, {4,5}, {1,2}};

		// 방문처리를 위한 boolean배열 선언
		boolean[] visited = new boolean[9];

		System.out.println(bfs(1, graph, visited));

        int n = 10;
        int result = fibonacci(n);
        System.out.println("Fibonacci(" + n + ") = " + result);
    }

    
    public static void main(String[] args) {

    }
}