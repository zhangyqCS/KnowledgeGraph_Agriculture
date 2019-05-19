# -*- coding: UTF-8 -*-
import pandas as pd
import os
import jieba
import triple_ie
from pyltp import SentenceSplitter,Segmentor,Postagger,NamedEntityRecognizer,Parser,SementicRoleLabeller

LTP_DATA_DIR='D:\LTP\ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')	 # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')	# 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。

#创建停用词表
def stopwordslist(filepath):
	stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
	return stopwords


# 分句，也就是将一片文本分割为独立的句子
def sentence_splitter(sentence):
	sents = SentenceSplitter.split(sentence)  # 分句
	#print('\n'.join(sents))


# 分词
def segmentor(sentence):
	segmentor = Segmentor()	 # 初始化实例
	segmentor.load(cws_model_path)	# 加载模型
	#segmentor.load_with_lexicon('cws_model_path', 'D:\pyprojects\LTP\ltp_data\dict.txt') #加载模型	  使用用户自定义字典的高级分词
	words = segmentor.segment(sentence)	 # 分词
	# 默认可以这样输出
	#print('/'.join(words))
	# 可以转换成List 输出
	words_list = list(words)
	segmentor.release()	 # 释放模型
	return words_list


# 词性标注
def posttagger(words):
	postagger = Postagger()	 # 初始化实例
	postagger.load(pos_model_path)	# 加载模型
	postags = postagger.postag(words)  # 词性标注
	#for word, tag in zip(words, postags):
		#print(word + '/' + tag)
	postagger.release()	 # 释放模型
	return postags


# 命名实体识别
def e_recognize(words, postags):
	recognizer = NamedEntityRecognizer()  # 初始化实例
	recognizer.load(ner_model_path)	 # 加载模型
	netags = recognizer.recognize(words, postags)  # 命名实体识别
	#for word, ntag in zip(words, netags):
		#print(word + '/' + ntag)
	recognizer.release()  # 释放模型
	return netags




#利用LTP实现对输入的.csv文件的分句、分词、词性标注、命名实体识别和三元组抽取
def myltp(input_path, output_path):
    records = pd.read_csv(input_path)

    titles = records['title']
    openTypeLists = records['openTypeList']
    details = records['detail']

    # for i in range(20):
    #     #分句
    #     sents = SentenceSplitter.split(details[i])
    #     #print(sents)
    #     sub_sents= list(sents)
    #
    #     #初始化实例
    #     segmentor = Segmentor()
    #     segmentor.load_with_lexicon(cws_model_path, 'lexicon')
    #
    #     postagger = Postagger()
    #     postagger.load(pos_model_path)
    #
    #     recognizer = NamedEntityRecognizer()
    #     recognizer.load(ner_model_path)
    #
    #     for i in range(len(sub_sents)):
    #         #print('sub_sents[i]=' +sub_sents[i])
    #
    #         #分词
    #         words = segmentor.segment(sub_sents[i])
    #         #print(type(words))
    #         #print('\t'.join(words))
    #         old_sub_words = list(words)
    #         print(old_sub_words)
    #
    #         # forceSegmentor = ForceSegmentor()
    #         # forceSegmentor.load('D:\\Python\\MyTest\\KG_Agriculture\\lexicon.txt')
    #         # words = forceSegmentor.merge(sub_sents[i], old_sub_words)  # 强制分词以后的结果
    #         # new_sub_words = list(words)
    #         # print(new_sub_words)
    #
    #         # 词性标注
    #         postags = postagger.postag(old_sub_words)
    #         postags_result = list(postags)
    #
    #         print(old_sub_words)
    #         print(postags_result)
    #
    #         #命名实体识别
    #         netags = recognizer.recognize(old_sub_words, postags_result)
    #         netags_result = list(netags)
    #         print(netags_result)
    #
    #     segmentor.release()
    #     postagger.release()
    #     recognizer.release()

    stopwords = stopwordslist('D:\\Python\\MyTest\\KG_Agriculture\\stopwords\\ltp_stopwords.txt')
    jieba.load_userdict('D:\\Python\\MyTest\\KG_Agriculture\\Plants\\lexicon.txt')
    file1 = open(output_path, 'w', encoding='UTF-8')
    triple_path = 'D:\\Python\\MyTest\\KG_Agriculture\\Plants\\triple_results_plants2.txt'

    for i in range(20):
        sentences = SentenceSplitter.split(details[i])
        file2 = open(triple_path, 'a', encoding='UTF-8')
        file2.write(titles[i]+': \t')
        file1.write(titles[i]+': \t')
        file2.close()

        for sentence in sentences:

            final = []
            segs = jieba.cut(sentence, cut_all=False)
            for seg in segs:
                #print(seg + '/ ')
                #if seg not in stopwords:
                final.append(seg)

            #print(final)
            #words = segmentor(details[i])
            #print(words)

            postags = posttagger(final)
            netags = e_recognize(final, postags)

            IE = triple_ie.TripleIE(sentence, triple_path, final, postags, netags)
            IE.run()

            tags = []
            dict = []

            #file.write(str(i) + '\n')
            #tmp=""
            for word, ntag in zip(final, netags):
                if (ntag != 'O'):  # 过滤非命名实体
                    #print(word, ntag)
                    tags.append(ntag)
                    if (ntag not in dict):
                        dict.append(ntag)
                    file1.write(word +':'+ ntag+ ' ')

        file2 = open(triple_path, 'a', encoding='UTF-8')
        file1.write('\n')
        file2.write('\n')
        file2.close()

        print(i)

    file1.close()
    print('end...')


def main():
    input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\Plants\\my_datas_plants.csv'
    output_path = 'D:\\Python\\MyTest\\KG_Agriculture\\Plants\\ner_results_plants2.txt'
    myltp(input_path=input_path, output_path=output_path)

if __name__ == '__main__':
    main()