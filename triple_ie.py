# -*- coding: utf-8 -*-

import os
import re
import logging
import sys

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding("utf8")

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer,SentenceSplitter
from tqdm import tqdm
import utils as U

LTP_DATA_DIR='D:\LTP\ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')	 # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')	# 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。


segmentor = Segmentor()
segmentor.load(cws_model_path)

postagger = Postagger()
postagger.load(pos_model_path)

parser = Parser()
parser.load(par_model_path)

recognizer = NamedEntityRecognizer()
recognizer.load(ner_model_path)

class TripleIE(object):
    def __init__(self, sentence, out_file_path, words, postags, ner, clean_output=False):
        self.logger = logging.getLogger("TripleIE")

        #self.in_file_path = in_file_path
        #self.input_text = input_text
        self.sentence = sentence
        self.out_file_path = out_file_path
        #self.model_path = model_path
        self.words = words
        self.postags = postags
        self.ner = ner
        self.clean_output = clean_output  # 输出是否有提示

        self.out_handle = None

        #self.sentences = SentenceSplitter.split(self.sentences)

        # self.segmentor = Segmentor()
        # self.segmentor.load(os.path.join(self.model_path, "cws.model"))
        # self.postagger = Postagger()
        # self.postagger.load(os.path.join(self.model_path, "pos.model"))
        # self.parser = Parser()
        # self.parser.load(os.path.join(self.model_path, "parser.model"))
        # self.recognizer = NamedEntityRecognizer()
        # self.recognizer.load(os.path.join(self.model_path, "ner.model"))

    def run(self, input_text=None, out_file_path=None):
        # if in_file_path is not None:
        #     self.in_file_path = in_file_path
        if out_file_path is not None:
            self.out_file_path = out_file_path

        self.out_handle = open(self.out_file_path, 'a', encoding='UTF-8')

        # with open(self.in_file_path, "r", encoding="utf-8") as rf:
        #     self.logger.info("loadding input file {}...".format(self.in_file_path))
        #     text = ""
        #     for line in rf:
        #text = input_text.strip()

        #self.logger.info("done with loadding file...")

        #text = U.rm_html(input_text)
        #sentences = U.split_by_sign(input_text)

        #self.logger.info("detect {} sentences".format(len(self.sentences)))

        #self.logger.info("start to extract...")
        self.extract(self.sentence)

        #self.logger.info("done with extracting...")
        #self.logger.info("output to {}".format(self.out_file_path))

        # close handle
        self.out_handle.close()

    def extract(self, sentence):
        #words = self.segmentor.segment(sentence)
        #postags = self.postagger.postag(words)
        #ner = self.recognizer.recognize(words, postags)
        self.arcs = parser.parse(self.words, self.postags)

        sub_dicts = self._build_sub_dicts(self.words, self.postags, self.arcs)
        for idx in range(len(self.postags)):

            if self.postags[idx] == 'v':
                sub_dict = sub_dicts[idx]
                # 主谓宾
                if 'SBV' in sub_dict and 'VOB' in sub_dict:
                    e1 = self._fill_ent(self.words, self.postags, sub_dicts, sub_dict['SBV'][0])
                    r = self.words[idx]
                    e2 = self._fill_ent(self.words, self.postags, sub_dicts, sub_dict['VOB'][0])
                    # if self.clean_output:
                    #     self.out_handle.write("%s, %s, %s\n" % (e1, r, e2))
                    # else:
                    #     self.out_handle.write("主谓宾\t(%s, %s, %s)\n" % (e1, r, e2))
                    self.out_handle.write("(%s, %s, %s); " % (e1, r, e2))
                    self.out_handle.flush()
                # 定语后置，动宾关系
                if self.arcs[idx].relation == 'ATT':
                    if 'VOB' in sub_dict:
                        e1 = self._fill_ent(self.words, self.postags, sub_dicts, self.arcs[idx].head - 1)
                        r = self.words[idx]
                        e2 = self._fill_ent(self.words, self.postags, sub_dicts, sub_dict['VOB'][0])
                        temp_string = r + e2
                        if temp_string == e1[:len(temp_string)]:
                            e1 = e1[len(temp_string):]
                        if temp_string not in e1:
                            # if self.clean_output:
                            #     self.out_handle.write("%s, %s, %s\n" % (e1, r, e2))
                            # else:
                            #     self.out_handle.write("动宾定语后置\t(%s, %s, %s)\n" % (e1, r, e2))
                            self.out_handle.write("(%s, %s, %s); " % (e1, r, e2))

                            self.out_handle.flush()

            # 抽取命名实体有关的三元组
            try:
                if self.ner[idx][0] == 'S' or self.ner[idx][0] == 'B':
                    ni = idx
                    if self.ner[ni][0] == 'B':
                        while len(self.ner) > 0 and len(self.ner[ni]) > 0 and self.ner[ni][0] != 'E':
                            ni += 1
                        e1 = ''.join(self.words[idx:ni + 1])
                    else:
                        e1 = self.words[ni]
                    if self.arcs[ni].relation == 'ATT' and self.postags[self.arcs[ni].head - 1] == 'n' and self.ner[
                        self.arcs[ni].head - 1] == 'O':
                        r = self._fill_ent(self.words, self.postags, sub_dicts, self.arcs[ni].head - 1)
                        if e1 in r:
                            r = r[(r.idx(e1) + len(e1)):]
                        if self.arcs[self.arcs[ni].head - 1].relation == 'ATT' and self.ner[self.arcs[self.arcs[ni].head - 1].head - 1] != 'O':
                            e2 = self._fill_ent(self.words, self.postags, sub_dicts, self.arcs[self.arcs[ni].head - 1].head - 1)
                            mi = self.arcs[self.arcs[ni].head - 1].head - 1
                            li = mi
                            if self.ner[mi][0] == 'B':
                                while self.ner[mi][0] != 'E':
                                    mi += 1
                                e = ''.join(self.words[li + 1:mi + 1])
                                e2 += e
                            if r in e2:
                                e2 = e2[(e2.idx(r) + len(r)):]
                            if r + e2 in self.sentence:
                                # if self.clean_output:
                                #     self.out_handle.write("%s, %s, %s\n" % (e1, r, e2))
                                # else:
                                #     self.out_handle.write("人名/地名/机构\t(%s, %s, %s)\n" % (e1, r, e2))
                                self.out_handle.write("(%s, %s, %s); " % (e1, r, e2))

                                self.out_handle.flush()
            except:
                pass

    """
    :decription: 为句子中的每个词语维护一个保存句法依存儿子节点的字典
    :args:
        words: 分词列表
        postags: 词性列表
        arcs: 句法依存列表
    """

    def _build_sub_dicts(self, words, postags, arcs):
        sub_dicts = []
        for idx in range(len(words)):
            sub_dict = dict()
            for arc_idx in range(len(arcs)):
                if arcs[arc_idx].head == idx + 1:
                    if arcs[arc_idx].relation in sub_dict:
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
                    else:
                        sub_dict[arcs[arc_idx].relation] = []
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
            sub_dicts.append(sub_dict)
        return sub_dicts

    """
    :decription:完善识别的部分实体
    """

    def _fill_ent(self, words, postags, sub_dicts, word_idx):
        sub_dict = sub_dicts[word_idx]
        prefix = ''
        if 'ATT' in sub_dict:
            for i in range(len(sub_dict['ATT'])):
                prefix += self._fill_ent(words, postags, sub_dicts, sub_dict['ATT'][i])

        postfix = ''
        if postags[word_idx] == 'v':
            if 'VOB' in sub_dict:
                postfix += self._fill_ent(words, postags, sub_dicts, sub_dict['VOB'][0])
            if 'SBV' in sub_dict:
                prefix = self._fill_ent(words, postags, sub_dicts, sub_dict['SBV'][0]) + prefix

        return prefix + words[word_idx] + postfix
