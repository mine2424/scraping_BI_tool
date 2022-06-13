# scraping_BI_tool

## 概要

これは価格.com の自動車データを取得することを初期の目標とし、最終的にはコードを書かずに UI ベースで web ページからデータをスクレイピングするシステムを構築します。

## 仕様

以下のページの「メーカから探す」へ遷移し、「タイプから探す」に遷移してそれぞれのグレードの主要諸元からスペック・仕様を取得しています。
https://kakaku.com/kuruma/maker/

## 導入

### packages

```sh
# command
pip3 install requests
pip3 install BeautifulSoup4
pip3 install selenium

# version
requests 2.28.0
BeautifulSoup4 4.11.1
selenium 4.2.0
```
