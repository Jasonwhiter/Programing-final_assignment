# Programing-final_assignment<br>
こちらは土方ゼミのプログラミング発表会で作成したプログラム

## プログラミング言語<br>
Python

## プログラムの概要<br>
新聞記事の画像を用いてその記事の内容に似た記事の内容をスクレイピングで抽出し、
記事を50種返すプログラム

## プログラムの実際の実行動画<br>
https://drive.google.com/drive/folders/1RAXdJESHyZkk5jftNJNyCtpuHveskkgP?usp=share_link

## プログラムに用いたTF-IDFの説明についての記事
https://atmarkit.itmedia.co.jp/ait/articles/2112/23/news028.html


## プログラムの動作フロー<br>
1.新聞記事をOCRソフト(teserract)とPyocr(OCRへpythonでアクセスするためのライブラリ)を用いて新聞記事から画像に映るテキストを文字列して抽出
<br><br>

2.janome(形態素解析ツール)を用いて画像から抽出した記事に含まれる名詞の数をカウント
<br>
　ex)日本:3回, 防衛:4回, 中国:3回, ミサイル:4回...→辞書に保存
<br>  
3.IDFの抽出…ヤフーの主要トピックスの主要64記事を用いる<br>
Topic…国内、国際、経済、エンタメ、スポーツなど8カテゴリ<br>
記事抽出に使用したライブラリ…<br>
-BeautifulSoup…スクレイピングを行う<br>
-Requests…HTTP通信ライブラリ<br>

3の動作内容<br>
topicの8カテゴリの記事の詳細のリンク先に飛び文章の本文を抽出<br>
↓<br>
1で読み込んだ新聞の画像記事に単語が
含まれるかどうかを確かめる<br>

※を64回分繰り返して下の式を求める<br>

4.2で計算した画像に含まれる単語数と、で計算したIDFの値を<br>
　　TFIDF(画像に含まれる単語の重要度を表すデータ)を計算し、<br>
　　単語をkeyとしてTFIDFをvalueとして辞書型に保管する<br>

5.TFIDFの大きい単語6つを取り出し、検索キーワードとしてヤフーでrequestsモジュールを用いて記事を検索し、上位50件の検索結果にあたる記事の「タイトル、URL、記事の文章」を抽出<br>


6.GUIを用いて関連記事のタイトルと文章のコンテンツを表示

