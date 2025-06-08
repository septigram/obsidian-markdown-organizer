# Obsidianファイル振り分けツール

## 概要

本ツールは、カレントディレクトリ内のMarkdown（.md）ファイルを、ファイル先頭のYAMLヘッダに記載されたタグ情報と、指定したルール（rules.yaml）に基づいて自動的にフォルダへ振り分けるツールです。

## 特徴
- .mdファイルのYAMLヘッダ（tags）をもとに柔軟なルールで自動仕分け
- ルールはyaml形式で記述し、and/or/not等の論理式に対応
- 実際のファイル移動は `obsidian-cli` コマンドを利用
- 移動前に処理内容を一覧表示し、ユーザー確認後に実行

## rules.yamlの文法

`rules.yaml` には、以下のような形式でルールを記述します。

```yaml
rules:
  - name: rule-1
    when: tag:Ai and not tag:Business
    then: move to 技術/技術-AI
  - name: rule-2
    when: tag:Graphics and not tag:Business
    then: move to 技術/技術-CG
  # ...
```

### 各フィールドの意味
- `name`: ルールの識別名（任意の文字列）
- `when`: 適用条件。タグの有無を論理式（and, or, not, 括弧）で記述します。
    - 例: `tag:Ai and not tag:Business`
    - 例: `tag:Software or tag:Electronics`
    - 例: `tag:Crafts and (tag:Art or tag:Handmade)`
- `then`: マッチ時の処理。`move to フォルダ名` の形式で記述します。

### when式の記法
- `tag:タグ名` でタグの有無を判定
- `and`, `or`, `not` で論理演算
- 括弧 `()` でグループ化

#### 例
- `tag:Ai and not tag:Business`
- `tag:Graphics or tag:Software`
- `tag:Crafts and (tag:Art or tag:Handmade)`

## 使い方
1. 必要なパッケージをインストール
   ```sh
   pip install -r requirements.txt
   ```
2. ルールファイル（rules.yaml）を編集
3. カレントディレクトリに.mdファイルを配置
4. ツールを実行
   ```sh
   python obsidian-folder-organizer.py
   ```
5. 移動内容を確認し、`y` で実行

## 依存パッケージ
- pyyaml
- lark

## 注意
- ファイル移動には `obsidian-cli` コマンドが必要です。事前にインストールしてください。

## ライセンス
- MIT License
