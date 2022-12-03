button_all=None
while (button_all==None):
    
    from ast import While, keyword
    import timeit
    from PIL import Image, ImageEnhance
    from numpy import sort
    import pyocr
    import PySimpleGUI as sg

    layout= [
        [sg.Text('検索に使う新聞記事の選択をしてください')],
        [sg.Text('画像ファイル(PNG形式のみ対応)'), sg.InputText(), sg.FileBrowse(key='file')],
        [sg.Button('選択')]
    ]

    window=sg.Window('画像ファイル選択', layout)

    #文字を抽出したい画像のパスを選ぶ

    while True:
        event, values= window.read()
        if event == '選択':
            if values['file'].endswith('png')==True:
                img=values['file']
                print(img)
                break
            else:
                continue
        else:
            continue

    window.close()



    #環境変数「PATH」にTesseract-OCRのパスを設定。
    #Windowsの環境変数に設定している場合は不要。


    #pyocrにTesseractを指定する。
    pyocr.tesseract.TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    tools = pyocr.get_available_tools()
    tool = tools[0]



    # 画像の文字を抽出
    text_layout = pyocr.builders.TextBuilder(tesseract_layout=5)#テキストの読み取り方法の指定
    img = Image.open(img)


    text = tool.image_to_string(img, lang="jpn_vert", builder=text_layout)#縦書きの日本語の読み取り用の辞書を指定


    from janome.tokenizer import Tokenizer
    import collections

    t = Tokenizer()
    counter={}#名詞カウント用の辞書


    # トークン列に分解
    for tok in t.tokenize(text):
        pos = tok.part_of_speech.split(',')  # 品詞を分解
        if '名詞' in pos:  # 品詞に名詞が含まれていれば
            if tok.surface in counter.keys():  # 統計にトークンの表層形が含まれていれば
                counter[tok.surface] += 1  # カウントする
            else:
                counter[tok.surface] = 1  # 新規カウントする


    # 結果を出力

    word_list=[]
    word_time_list=[]
    for string in counter:
        word_list.append(string)
        word_time_list.append(counter[string])

    # print(word_list)
    # print(word_time_list)

    word_time=0
    for time in word_time_list:
        word_time+=time

    tf_num=0
    tf=[]
    for timeof_word in word_time_list:
        timeof_word/=word_time
        tf.append(timeof_word)

    tf_dict={}
    for tf_count in range(len(tf)):
        tf_dict[word_list[tf_count]]=tf[tf_count]

    print(tf_dict)

    import requests
    from bs4 import BeautifulSoup
    from janome.tokenizer import Tokenizer
    import math
    dict_before_IDF={}
    for dic00apend in tf_dict:
        dict_before_IDF[dic00apend]=0


    dict_words={}
    news_top_url='https://news.yahoo.co.jp/topics'

    response=requests.get(news_top_url)

    soup=BeautifulSoup(response.text ,'html.parser')


    all_urls=[]
    for element in soup.find_all("a" , attrs={'class' :"sc-jnlKLf gYAwpP"}):
        url=element.get("href")
        all_urls.append(url)









    all_url2=[]
    # print(dict_news_articles)
    sum=1
    for news_articles in all_urls:
        response_data=requests.get(news_articles)
        soup_article=BeautifulSoup(response_data.text, 'html.parser')
        content=soup_article.find("a", attrs={"class" : "sc-kvjbNB lpeELo"})
        url2=content.get("href")
        all_url2.append(url2)

        
    # print(dict_news_articles)
    sum=1
    for news_articles in all_url2:
        response_data=requests.get(news_articles)
        soup_article=BeautifulSoup(response_data.text, 'html.parser')
        content=soup_article.find("div", attrs={"class" : "article_body highLightSearchTarget"})
        if content==None:
            content="No contents was written in this articles!!"
            pass
        else:
            content=content.text.strip()



        for gg in dict_before_IDF:
            if(gg in content)==True:
                dict_before_IDF[gg]=dict_before_IDF[gg]+1


    idf_dict={}
    for fin in dict_before_IDF:
        idf=math.log(len(all_urls)/(1+dict_before_IDF[fin]))
        print(idf)
        idf_dict[fin]=idf

    # print(idf_dict)


    tfidf={}
    import re
    ignores = re.compile("[\\.,/\"'>()&;:-]|")#無視したい文字列


    for tfidf_data in tf_dict:
        #tfidf[tfidf_data]=tf_dict[tfidf_data]*idf_dict[tfidf_data]
        tfidf[tfidf_data]=tf_dict[tfidf_data]*idf_dict[tfidf_data]


    tfidf = sorted(tfidf.items(), key=lambda x:x[1], reverse=True)#値が大きい順にソート, ラムダは無名関数
    # print(tfidf)
    x=0
    keyword=[]

    askinum=[]
    for num in range(32,65):
        askinum.append(num)
    for num in range(91,96):
        askinum.append(num)
    for num in range(123,128):
        askinum.append(num)


    for sort_tfidf in tfidf:
        tf=None
        for num in askinum:
            if (chr(num) in sort_tfidf[0])==True:
                tf=True
        print(tf, sort_tfidf[0])
        if tf==None:
            pass
            response_proto=requests.get(f'https://news.yahoo.co.jp/search?p={sort_tfidf[0]}&ei=utf-8')
            proto_soup=BeautifulSoup(response_proto.text, 'html.parser')
            numofsearch=(proto_soup.find('div', attrs={'class':"sc-dBPazb kNepAL"})).get_text()
            numofsearch=numofsearch.replace("件","")
            numofsearch=numofsearch.replace(",","")
            if int(numofsearch)>1000:
                pass
                keyword.append(sort_tfidf[0])
                x+=1
        if x==5:
            break

    print(keyword)
    keyword_a=tuple(keyword)
    keyword_re="+".join(keyword_a)
    keyword_aa=",".join(keyword_a)

    import requests
    from bs4 import BeautifulSoup


    response=requests.get(f'https://news.yahoo.co.jp/search?p={keyword_re}&ei=utf-8')#keyword検索をしてレスポンスを得る

    soup=BeautifulSoup(response.text ,'html.parser')

    dict_news_articles={}
    for element in soup.find_all("a" , attrs={'class' :"sc-cstzgH iAWHLA newsFeed_item_link"}):
        url = element.get("href")#検索結果の記事のurl取得
        title=(element.find('div', attrs={'class':'newsFeed_item_title'})).get_text()
        title=title.replace("\u3000", "")
        dict_news_articles[title]=url

        

    print(dict_news_articles)
    dict_news_alllist={}






    sum=1
    # print(dict_news_articles)
    for news_articles in dict_news_articles:
        url_article=dict_news_articles[news_articles]
        response_data=requests.get(url_article)
        soup_article=BeautifulSoup(response_data.text, 'html.parser')
        contents=[]
        for news_content in soup_article.find_all("div", attrs={"class" : "article_body highLightSearchTarget"}):#記事のコンテンツを取得
            news_content=news_content.text.strip()
            contents.append(news_content)
        contents="/".join(contents)
        contents=contents.replace("\n", "")
        contents=contents.replace("\u3000", "")

        article_num="article"+str(sum)
        list=[news_articles, dict_news_articles[news_articles], contents]
        dict_news_alllist[article_num]=list
        sum+=1
        list=[]


    print(dict_news_alllist)
    artilceslist=[]
    for ddd in dict_news_alllist:
        strings=ddd+":"+dict_news_alllist[ddd][0]
        artilceslist.append(strings)


    button=None
    while (button==None):
        sg.theme('SystemDefault')   # デザインテーマの設定


        # ウィンドウに配置するコンポーネント
        layout = [  [sg.Text("こちらのキーワードで検索れました"),sg.Text(keyword_aa)],
                    [sg.Text("関連するニュースの記事のタイトル一覧はこちらです↓")],
                    [sg.Combo(values=artilceslist, size=(150, 1), key=True, enable_events=True)],            
                    #sg.VerticalSeparator(),

                    [sg.Submit(key='-submit-')]]

        # ウィンドウの生成
        window = sg.Window('検索結果一覧', layout)

        # イベントループ
        while True:             # Event Loop
            event, values = window.Read()
            choose_articles=values[True]
            print(choose_articles)
            if event == sg.WIN_CLOSED:
                break
            if event == "-submit-":
                break

            
        window.close()

        for dddd in dict_news_alllist:
            if dddd in choose_articles:
                artilce_key=dddd





        img_resize = img.resize((500, 500))
        img_resize.save('C:/Users/hollo/work/prog_kadai/image/news.png')

        import PySimpleGUI as sg

        print(dict_news_alllist[artilce_key][2])
        import textwrap
        text_wrap_list=textwrap.wrap(dict_news_alllist[artilce_key][2] , 40)
        text='\n'.join(text_wrap_list)
        print(text)

        sg.theme('SystemDefault')
        layout = [
        [sg.Text("ニュース記事のタイトル"),sg.Text(dict_news_alllist[artilce_key][0])],
        [sg.Image('C:/Users/hollo/work/prog_kadai/image/news.png', key='image'),sg.Column([[sg.Text(text)]], scrollable=True)],
        [sg.Button("ニュース記事のサイトへ飛ぶ"), sg.Button("次へ")]
        
        ]

        window = sg.Window('画像',layout, size=(1200,600))
        # イベントループ
        while True:
            event, values = window.Read()
            if event == "ニュース記事のサイトへ飛ぶ":
                import webbrowser
                webbrowser.open(dict_news_alllist[artilce_key][1])
            if event == '次へ' :
                break
            if event == sg.WIN_CLOSED:
                break

        window.close()

        layout=[
        [sg.Text("""他の記事を検索する場合は「はい」、
                    プログラムを中断する場合は「いいえ」を
                    選択してください""")],
        [sg.Button('はい'), sg.Button('いいえ')]
        ]

        window = sg.Window('プログラムを終了しますか?', layout)


        while True:
            event, values = window.Read()
            if event== 'いいえ':
                button=True
                break
            if event== 'はい'  or sg.WIN_CLOSED:
                button=None
                break
        window.close()

    layout=[
        [sg.Text("""他の画像を用いて検索する場合は「はい」、
                    プログラムを中断する場合は「いいえ」を
                    選択してください""")],
        [sg.Button('はい'), sg.Button('いいえ')]
        ]

    window = sg.Window('プログラムを終了しますか?', layout)


    while True:
        event, values = window.Read()
        if event== 'いいえ':
            button_all=True
            break
        if event== 'はい'  or sg.WIN_CLOSED:
            button_all=None
            break
    window.close()
    
    
    
    