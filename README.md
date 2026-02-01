# python-playground

このリポジトリはPython環境で様々な技術やライブラリを試すためのプレイグラウンドです。

## 環境構築

### uv（Pythonパッケージマネージャー）

このプロジェクトでは[uv](https://github.com/astral-sh/uv)を使用してPython依存関係を管理しています。

#### uvのインストール

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv
```

#### uvの使用方法

```bash
# 依存関係のインストール
uv sync

# パッケージの追加
uv add <package-name>

# パッケージの削除
uv remove <package-name>

# スクリプトの実行
uv run python main.py
```

#### uvの特徴

- **高速**: Rustで実装されており、pipやpip-toolsより10-100倍高速
- **ロックファイル**: `uv.lock`で再現可能な環境を保証
- **pyproject.toml対応**: 標準的なPythonプロジェクト設定ファイルを使用

### mise（ツールバージョンマネージャー）

[mise](https://mise.jdx.dev/)を使用してプロジェクトで必要なツールのバージョン管理を行っています。

#### miseのインストール

```bash
curl https://mise.run | sh
```

#### 現在の設定

`mise.toml`で以下のツールを管理しています：

```toml
[tools]
etcd = "3.6.7"
```

#### etcdのインストールについて

etcdは`asdf:particledecay/asdf-etcd`プラグイン経由でインストールされます。

**注意**: asdf-etcdプラグインのmacOS版にはバグがあり、デフォルトでは`etcdctl`のみがインストールされ、`etcd`本体と`etcdutl`がインストールされません。

この問題は以下のファイルを修正することで解決できます：

```bash
# プラグインのダウンロードスクリプトを修正
~/.local/share/mise/plugins/etcd/bin/download
```

修正内容（27-29行目）：

```bash
# 修正前: etcdctlのみ展開
(unzip "$release_file" -d "$ASDF_DOWNLOAD_PATH" "${dir_name}/${tool_cmd}" &&
  mv "${ASDF_DOWNLOAD_PATH}/${dir_name}/${tool_cmd}" "$ASDF_DOWNLOAD_PATH/" &&
  rmdir "${ASDF_DOWNLOAD_PATH}/${dir_name}") ||
  fail "Could not extract $release_file"

# 修正後: 全バイナリを展開
(unzip "$release_file" -d "$ASDF_DOWNLOAD_PATH" "${dir_name}/etcd" "${dir_name}/etcdctl" "${dir_name}/etcdutl" &&
  mv "${ASDF_DOWNLOAD_PATH}/${dir_name}"/* "$ASDF_DOWNLOAD_PATH/" &&
  rmdir "${ASDF_DOWNLOAD_PATH}/${dir_name}") ||
  fail "Could not extract $release_file"
```

修正後、再インストール：

```bash
mise uninstall etcd@3.6.7
mise install etcd@3.6.7
```

#### 確認

```bash
etcd --version
etcdctl version
etcdutl version
```

すべてのコマンドが正常に動作することを確認してください。

## 依存関係

- Python 3.9以上
- etcd3
- protobuf < 3.21

## 開発

```bash
# 環境のセットアップ
mise install
uv sync

# スクリプトの実行
uv run python main.py
```

## ライセンス

このプロジェクトは実験・学習目的のプレイグラウンドです。
