import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

tobe_replace = ['\r', '\t', '\n', '\xa0', '\u3000', '&nbsp;', '&amp']


def filter_tags(htmlstr):
    """
    去除html的格式

    @param htmlstr: 处理的html string
    @type foo: string
    @return: 处理完成的string
    @rtype: string
    """
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    re_br = re.compile('<br\s*?/?>')
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_nt = re.compile('\n\t')
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = re_nt.sub('', s)
    return s


def process(strl):
    """
    文字处理'\r', '\t' 等字符，变为lowercase

    @param strl: 处理的string
    @type foo: string
    @return: 处理完成的string
    @rtype: string
    """
    _str = strl
    for char in tobe_replace:
        _str = _str.replace(char, '')
    return _str.strip().lower()


def top_tfidf_feats(row, features, top_n=25):
    """
    得到tfidf数据组，默认每篇文章的前25个词语

    @param row: 对应文章的顺序
    @type row: int
    @param features: tfidf关键词
    @type features: string
    @param top_n: 定义提取前几个关键词，默认前25个
    @type top_n: int
    @return: 所有文章tfidf数据组
    @rtype: dataframe
    """
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df


def top_feats_in_doc(Xtr, features, row_id, top_n=25):
    """
    得到tfidf数据组，默认每篇文章的前25个词语

    @param Xtr: tfidf的vector结果
    @type Xtr: vector
    @param features: tfidf关键词
    @type features: string
    @param row_id: 对应文章的顺序
    @type row_id: int
    @param top_n: 定义提取前几个关键词，默认前25个
    @type top_n: int
    @return: 所有文章tfidf数据组
    @rtype: dataframe
    """
    row = np.squeeze(Xtr[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)


def find_match(first_frame, second_frame):
    """
    得到任意两篇文章的相同关键词的数量

    @param first_frame: 第一篇文章的前25个关键词
    @type first_frame: list
    @param second_frame: 第二篇文章的前25个关键词
    @type second_frame: list
    @return: 相同关键词的set
    @rtype: set
    """

    set_a = set(first_frame['feature'][:25])
    set_b = set(second_frame['feature'][:25])
    set_c = set_a & set_b
    return set_c


def compute_similarity(arg):
    """
    计算两篇文章的相似度

    @param arg: 包含文章的index，用来比较的文章的原始数据，tfidf的vector以及关键词库
    @type arg: arg
    @return: none或者相似度达到要求的文章的index
    @rtype: int
    """
    base_id, compare_doc, X, features = arg
    first_frame = top_feats_in_doc(X, features, base_id, 25)
    second_frame = top_feats_in_doc(X, features, compare_doc['id'], 25)
    match_set = find_match(first_frame, second_frame)
    beta = len(match_set)/25
    if beta > 0.15:
        return compare_doc['id']
    return None


def get_true_key(Xtr, features, row_id, top_n=25):
    """
    得到tfidf数据组前25个词语中权重大于0.2的词语

    @param Xtr: tfidf的vector结果
    @type Xtr: vector
    @param features: tfidf关键词
    @type features: string
    @param row_id: 对应文章的顺序
    @type row_id: int
    @param top_n: 定义提取前几个关键词，默认前25个
    @type top_n: int
    @return: 对应文章的大于0.2的关键词
    @rtype: list
    """
    row = np.squeeze(Xtr[row_id].toarray())
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_keys = [features[i] for i in topn_ids if row[i] > 0.2]
    return top_keys


def filter_with_truekeys(base_keys, compare_keys):
    """
    比较两个文章的truekey是否有重合的

    @param base_keys: 第一篇文章的truekeys
    @type base_keys: list
    @param compare_keys: 第二篇文章的truekeys
    @type compare_keys: list
    @return: true or false
    @rtype: bool
    """
    return any(i in base_keys for i in compare_keys)


def get_cluster_news(full_data):
    """
    聚类核心算法，处理数据，tfidf，一次聚类，二次聚类

    @param full_data: 所有文章的原始数据
    @type full_data: list
    @return: row_data（原始数据）, top_20_cluster（聚类结果),
    X（tfidf vector）, features（关键词）
    @rtype: tuple
    """
    # data processing start
    row_data = [
        {
            'id': i,
            'title': d['title'],
            'content': process(filter_tags(d['content'])),
            'source': d['source'],
            'url': d['url'],
            'date': d['date']
        }
        for i, d in enumerate(full_data)
    ]
    data = [
        d['title'] + '. ' + d['content']
        for d in row_data
    ]

    for i in range(len(data)):
        data[i] = data[i].translate(str.maketrans('', '', string.punctuation))

    # tfidf calculation
    vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
    X = vectorizer.fit_transform(data)
    features = vectorizer.get_feature_names()

    # data with id number
    data = [
        {
            'id': i,
            'text': d
        }
        for i, d in enumerate(data)
    ]

    clusters = []
    # first step: using simple similarity
    while data:
        base_id = data[0]['id']
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            futures = executor.map(
                compute_similarity, [(base_id, d, X, features)
                                     for d in data[1:]]
            )
        c = [base_id]
        for f in futures:
            if f:
                c.append(f)
        data = [
            d
            for d in data
            if d['id'] not in c
        ]
        clusters.append(c)

    clusters = sorted(clusters, key=len, reverse=True)
    # second cluster using truekeys
    final_cluster = []
    for topic in clusters:
        remain = topic.copy()
        for item in topic[1:]:
            base_keys = get_true_key(X, features, topic[0], 25)
            compare_keys = get_true_key(X, features, item, 25)
            remove = filter_with_truekeys(base_keys, compare_keys)
            if remove is False:
                remain.remove(item)
        final_cluster.append(remain)

    final_cluster = sorted(final_cluster, key=len, reverse=True)

    return row_data, final_cluster, X, features

# todo: third cluster - check base article are different -
# combine cluster with similar base article
