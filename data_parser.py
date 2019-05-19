# -*- coding: UTF-8 -*-
import pandas as pd

def get_datas_parser(input_path, output_path, title1):

    records = pd.read_csv(input_path)
    file = open('D:\\Python\\MyTest\\KG_Agriculture\\Plants\\lexicon.txt', 'w', encoding='UTF-8')

    titles = records['title']
    openTypeLists = records['openTypeList']
    details = records['detail']
    new_datas = []
    i=0

    # print(openTypeLists[0])
    # print(titles[0])
    # print(details[0])
    #
    # print(output_title in openTypeLists[0])

    #print(i)
    while i <= titles.last_valid_index():
        if title1 in str(openTypeLists[i]):
            data = {"title": titles[i], "openTypeList":openTypeLists[i], "detail":details[i] }
            new_datas.append(data)
            file.write(titles[i]+' 5000'+'\n')
        i=i+1
        print(i)

    new_records = pd.DataFrame(new_datas, columns=["title", "openTypeList", "detail"])
    #print(new_recodes)
    new_records.to_csv(output_path, index=False, encoding='utf_8_sig')
    print("end...")

    file.close()



def main():
    input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_datas.csv'
    title1 = '植物'
    output_path = 'D:\\Python\\MyTest\\KG_Agriculture\\Plants\\my_datas_plants.csv'
    get_datas_parser(input_path=input_path, output_path=output_path, title1=title1)

if __name__ == '__main__':
    main()