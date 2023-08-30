## 정리

### DFS (모든 거리)

(깊이 우선 탐색)의 사용 경우:

- 그래프의 모든 경로를 탐색하고자 할 때 사용합니다.
- 해를 찾는 것이 목적이 아니라, 그래프 전체를 탐색하고자 할 때 유용합니다.
- 더 깊은 단계로 탐색하고자 할 때 사용합니다.
- 재귀 호출을 사용하므로 스택 공간을 더 많이 사용할 수 있습니다.

```java
import java.util.*;

public class Solution {

	// 방문처리에 사용 할 배열선언
	public static boolean[] vistied = new boolean[9];

	// 그림예시 그래프의 연결상태를 2차원 배열로 표현
	// 인덱스가 각각의 노드번호가 될 수 있게 0번인덱스는 아무것도 없는 상태라고 생각하시면됩니다.
	static int[][] graph = {{}, {2,3,8}, {1,6,8}, {1,5}, {5,7}, {3,4,7}, {2}, {4,5}, {1,2}};

	public static void dfs(int nodeIndex) {
		// 방문 처리
		vistied[nodeIndex] = true;

		// 방문 노드 출력
		System.out.print(nodeIndex + " -> ");

		// 방문한 노드에 인접한 노드 찾기
		for (int node : graph[nodeIndex]) {
			// 인접한 노드가 방문한 적이 없다면 DFS 수행
			if(!vistied[node]) {
				dfs(node);
			}
		}
	}

	public static void main(String[] args) {
		dfs(1);
	}

}
```

---

### BFS (최단 거리)

(너비 우선 탐색)의 사용 경우:

- 그래프에서 최단 경로를 찾고자 할 때 사용합니다.
- 해를 찾는 것이 목적이며, 최단 경로를 찾는 문제에 적합합니다.
- 시작 노드로부터 레벨별로 탐색하고자 할 때 사용합니다.
- 큐를 사용하므로 메모리를 더 많이 사용할 수 있습니다.

```java
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

    public static void main(String[] args) {
		// 그래프를 2차원 배열로 표현해줍니다.
		// 배열의 인덱스를 노드와 매칭시켜서 사용하기 위해 인덱스 0은 아무것도 저장하지 않습니다.
		// 1번인덱스는 1번노드를 뜻하고 노드의 배열의 값은 연결된 노드들입니다.

        // 근접 노드 표현
		int[][] graph = {{}, {2,3,8}, {1,6,8}, {1,5}, {5,7}, {3,4,7}, {2}, {4,5}, {1,2}};

		// 방문처리를 위한 boolean배열 선언
		boolean[] visited = new boolean[9];

		System.out.println(bfs(1, graph, visited));
		//출력 내용 : 1 -> 2 -> 3 -> 8 -> 6 -> 5 -> 4 -> 7 ->

        // dfs(1);
    }
}

```

---

### REF

https://codingnojam.tistory.com/41
