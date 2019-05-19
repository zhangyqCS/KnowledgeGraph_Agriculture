# -*- coding: UTF-8 -*-
import pandas as pd
from getData_from_baike import start

def get_struct_datas(input_path, output_path):
    # records = pd.read_csv(input_path)
    # titles = records['title']
    # new_datas = []
    #
    # for i in range(titles.last_valid_index()):
    #     print(i)
    #
    #     key_value = start(titles[i])
    #     data = {"title":titles[i], "struct_data":key_value}
    #     new_datas.append(data)
    new_datas = []
    file1 = open(input_path,'r', encoding='UTF-8')
    sents = file1.readline()

    while sents:
        print(sents)
        key_value = start(sents)
        data = {"title":sents, "struct_data":key_value}
        new_datas.append(data)
        sents = file1.readline()

    new_records = pd.DataFrame(new_datas, columns=["title", "struct_data"])
    #print(new_recodes)
    new_records.to_csv(output_path, index=False, encoding='utf_8_sig')
    file1.close()
    print("end...")

def main():
    # input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_datas.csv'
    # output_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_struct_datas.csv'
    input_path = 'C:\\Users\\zhangyq\\Desktop\\new.txt'
    output_path = 'C:\\Users\\zhangyq\\Desktop\\newdatas.csv'
    get_struct_datas(input_path=input_path, output_path=output_path)

if __name__ == '__main__':
    main()