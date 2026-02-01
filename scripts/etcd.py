import etcd3
import time
import sys

# etcdクライアントの初期化
etcd = etcd3.client()

def lead_election(node_name):
    print(f"{node_name}: リーダー選挙に挑戦します...")

    while True:
        # 1. 10秒間の有効期限を持つ「リース」を作成
        lease = etcd.lease(10)

        try:
            # 2. キー '/service/leader' を作成（すでに存在すれば失敗する）
            # 成功したノードが「リーダー」となる
            is_leader = etcd.put_if_not_exists(
                key='/service/leader', 
                value=node_name, 
                lease=lease
            )

            if is_leader:
                print(f"★ {node_name} はリーダーになりました！")
                # リーダーであり続ける間、リースを更新（Keep-alive）し続ける
                for _ in range(10):
                    time.sleep(1)
                    lease.refresh()
            else:
                # すでにリーダーがいる場合は、現在のリーダー名を取得して待機
                leader_name = etcd.get('/service/leader')[0].decode()
                print(f"現在、{leader_name} がリーダーです。待機中...")
                time.sleep(5)

        except Exception as e:
            print(f"エラー発生: {e}")
            time.sleep(1)

if __name__ == "__main__":
    node_name = sys.argv[1] if len(sys.argv) > 1 else "node-1"
    lead_election(node_name)
