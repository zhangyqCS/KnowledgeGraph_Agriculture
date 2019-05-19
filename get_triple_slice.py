# -*- coding: UTF-8 -*-
import pandas as pd

def get_slice(input_path, output_path):
    file1 = open(input_path, 'r', encoding='UTF-8')
    file2 = open(output_path, 'a+', encoding='UTF-8')

    lines = file1.readline()
    #print(lines)

    while lines:
        #print(lines[:-1])

        sents = lines[:-1].split(' ', 2)
        #print(len(sents))

        if len(sents) == 3:
            words1 = sents[2].split('、')
            words2 = sents[2].split('，')
            words3 = sents[2].split(',')

            #print([words1, words2])

            if len(words1) >= len(words2) and len(words1)>=len(words3):
                #print(words1)
                for word in words1:
                    file2.write(sents[0]+' '+sents[1]+' '+word+'\n')

            elif len(words2) >= len(words1) and len(words2)>=len(words3):
                #print(words2)
                for word in words2:
                    file2.write(sents[0] + ' ' + sents[1] + ' ' + word + '\n')
            else:
                #print(words3)
                for word in words3:
                    file2.write(sents[0] + ' ' + sents[1] + ' ' + word + '\n')
        else:
            file2.write('\n')

        lines = file1.readline()

    file1.close()
    file2.close()


def main():
    #input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_triple_datas.txt'
    #input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_tmp.txt'
    #output_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_triple_datas3.txt'
    input_path = 'C:\\Users\\zhangyq\\Desktop\\newtripes.txt'
    output_path = 'C:\\Users\\zhangyq\\Desktop\\newtrip.txt'
    get_slice(input_path=input_path, output_path=output_path)

if __name__ =='__main__':
    main()