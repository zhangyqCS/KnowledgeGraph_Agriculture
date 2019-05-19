# -*- coding: UTF-8 -*-
from py2neo import Graph, Node, Relationship, cypher,NodeMatcher
from pandas import DataFrame
import pandas as pd

#从结构化数据中创建三元组
def createKG(input_path, output_path):
    records = pd.read_csv(input_path)
    titles = records['title']
    datas = records['struct_data']
    file = open(output_path, 'a+', encoding='UTF-8')
    #file.write('玉米'+' '+'是'+'植物'+'\n')

    #test_graph = Graph('http://localhost:7474', username='neo4j', password='yaqiang3289')
    #matcher = NodeMatcher(test_graph)

    for i in range(titles.last_valid_index()):
        #print('datas[i]=' + str(datas[i]))
        print(i)
        if str(datas[i]) != 'nan' :
            #按照'#'进行分句
            key_values = datas[i][1:].split('#')
            #print(key_value)

            for j in range(len(key_values)):
                #按照':'进行分句,key_value[0]对应关系，key_value[1]对应另一个实体
                key_value = key_values[j].split(':')
                #
                # #检查该节点是否已经存在
                # #node1 = matcher.match('plants_name', name=titles[i]).first()
                # #print(node1)
                # if node1 == None:
                #     #print('Node1 is None...')
                #     node1 = Node('plants_name', name=titles[i])
                #     test_graph.create(node1)
                #     # print(node1)
                #
                # #检查该节点是否已经存在
                # node2 = matcher.match('plants_rela', name=key_value[1]).first()
                # #print(node2)
                # if node2 == None:
                #     #print('Node2 is None...')
                #     node2 = Node('plants_rela', name=key_value[1])
                #     test_graph.create(node2)
                #
                # r = Relationship(node1, key_value[0], node2)
                # test_graph.create(r)

                rint([titles[i][:-3],key_value[0],key_value[1]])
                file.write(titles[i][:-2]+' '+key_value[0]+' '+key_value[1]+'\n')
            file.write('\n')

    file.close()

def main():
    #createKG()
    #input_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_struct_datas.csv'
    #output_path = 'D:\\Python\\MyTest\\KG_Agriculture\\my_triple_datas.txt'
    input_path = 'C:\\Users\\zhangyq\\Desktop\\newdatas.csv'
    output_path = 'C:\\Users\\zhangyq\\Desktop\\newtripes.txt'
    createKG(input_path=input_path, output_path=output_path)

if __name__ =='__main__':
    main()