import pandas as pd

"""
以.csv文件作为输入，实现数据的正负样本比接近1:1
path为输入文件路径
batch_size为每个bug_id对应的正负样本总和
"""

def re_sampling(input_path, batch_size, output_path):

    recodes = pd.read_csv(input_path)

    bug_id = recodes['bug_id']
    rawCorpus = recodes['rawCorpus']
    file = recodes['file']
    match = recodes['match']

    #print(bug_id.last_valid_index())
    batch=0
    new_recodes = []
    while 1:
        is_next =0
        match_1=0

        num_1=0 #match=1的样本数目
        num_0=0 #match=0的样本数目

        if (batch * batch_size + 1) <=bug_id.last_valid_index():
            print('batch = '+ str(batch))

            for i in range(batch_size):
                # 先统计batch中match=1的样本数目，若数目小于(batch_size)/2，则对正样本重复采样,否则不做处理
                if match[batch*batch_size+i]==1:
                    match_1+=1

            if(match_1< (batch_size/2) ):
                while num_1<(batch_size/2):
                    for i in range(batch_size):
                        #遍历
                        if num_1<(batch_size/2) and match[batch*batch_size+i]==1:
                            recode = {"bug_id": bug_id[batch*batch_size+i], "rawCorpus":rawCorpus[batch*batch_size+i],
                                      "file":file[batch*batch_size+i], "match":match[batch*batch_size+i] }
                            new_recodes.append(recode)
                            num_1+=1
                while num_0<(batch_size/2):
                    for i in range(batch_size):
                        #遍历
                        if num_0<(batch_size/2) and match[batch*batch_size+i]==0:
                            recode = {"bug_id": bug_id[batch*batch_size+i], "rawCorpus":rawCorpus[batch*batch_size+i],
                                      "file":file[batch*batch_size+i], "match":match[batch*batch_size+i] }
                            new_recodes.append(recode)
                            num_0+=1
                #print(bug_id[batch*50+i], rawCorpus[batch*50+i], file[batch*50+i], match[batch*50+i])

            else:
                for i in range(batch_size):
                    recode = {"bug_id": bug_id[batch *batch_size + i], "rawCorpus": rawCorpus[batch * batch_size + i],
                              "file": file[batch * batch_size + i], "match": match[batch * batch_size + i]}
                    new_recodes.append(recode)
            is_next=1

        if is_next == 1:
            batch+=1
        else:
            break

    new_recodes = pd.DataFrame(new_recodes, columns=["bug_id", "rawCorpus", "file", "match"])
    #print(new_recodes)
    new_recodes.to_csv(output_path, index=False)
    print("end...")


def main():
    input_path = 'C:\\Users\\zhangyq\\Desktop\\data\\AspectJTest.csv'
    output_path = 'C:\\Users\\zhangyq\\Desktop\\Test.csv'
    batch_size = 50
    re_sampling(input_path=input_path, batch_size=batch_size, output_path=output_path)

if __name__ == '__main__':
    main()