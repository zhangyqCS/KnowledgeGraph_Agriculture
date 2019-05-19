# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

def start(title):
    #存放视频信息
    key_value=""
    page=0
    requests_fail=0
    names = []
    values = []

    while 1:
        try:
            is_next= 0
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
            headers = {'User-Agent': user_agent}
            #url = 'https://search.bilibili.com/all?keyword=F1&from_source=banner_search&page='+str(page)
            url = 'https://baike.baidu.com/item/' + title
            print('url=' + str(url))

            requests_obj = requests.get(url, headers=headers, timeout=10, allow_redirects=False)

            #判断请求是否成功
            if(requests_obj.status_code== 200):
                requests_obj.encoding='utf-8'
                html = requests_obj.text
                html_bs = BeautifulSoup(html,'html.parser')
                #print(html_bs)

                if(html_bs!=None):
                    #获取信息DOM节点
                    content_list1 = html_bs.select('.basic-info .name')
                    content_list2 = html_bs.select('.basic-info .value')

                    if content_list1!= None and len(content_list1)!=0 :
                        for content1 in content_list1 :
                            name = content1.get_text()
                            names.append(name)
                            #print(name)
                            #movies.append([href+' ', name])
                            #is_next=1;
                            #print('finish '+ str(page))
                    if content_list2!= None and len(content_list2)!=0 :
                        for content2 in content_list2 :
                            value = content2.get_text()[1:-1]
                            values.append(value)
                            #print(value)
                    for i in range( len(names) ):
                        key_value+= '#'+ names[i] +':'+ values[i]

            else:
                print('request fail error code is ' + str(requests_obj.status_code))
                if(requests_fail<4):
                    requests_fail+=1

        except:
            print("error! ")
            traceback.print_exc()

        else:
            #if is_next==1:
            #    page+=1
            #else:
                break
    print(key_value)
    return key_value
    # file = open('bilibili.txt', 'w', encoding='utf-8')
    # for movie in movies:
    #     file.write(movie[0]+'\t' + movie[1]+'\n')
    # file.close()
    # print('end...')

def main():
    start()

if __name__ == '__main__':
    main()