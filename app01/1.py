msg_list = [
    {'id':1,'content':'1','parent_id':None},
    {'id':2,'content':'2','parent_id':None},
    {'id':3,'content':'3','parent_id':None},
    {'id':4,'content':'1-4','parent_id':1},
    {'id':5,'content':'4-5','parent_id':4},
    {'id':6,'content':'2-6','parent_id':2},
    {'id':7,'content':'5-7','parent_id':5},
    {'id':8,'content':'3-8','parent_id':3},
    {'id':9,'content':'7-9','parent_id':7},
    {'id':10,'content':'3-10','parent_id':3},
    {'id':11,'content':'3-11','parent_id':3},
]



msg_list_dict={}
result=[]
for i in msg_list:
    i["child"]=[]
    msg_list_dict[i["id"]]=i
# print(msg_list_dict)
for i in msg_list:
    pid=i["parent_id"]
    if pid:
        msg_list_dict[pid]["child"].append(i)
    else:
        result.append(i)
# print(result)
# print(msg_list_dict)
# result=[]
# for i in msg_list:
#     if not i["parent_id"]:
#         result.append(i)
# for i in result:
#     print(i)
# for i in result:
#     print(i["content"])
#     for k in i["child"]:
#         print("---",k["content"])
#         for v in k["child"]:
#             print("------",v["content"])

def fk(k):
    for i in k:
        if i["child"]==[]:
            print("---"*k,i["content"])
        else:
            print("-"*i["id"],i["content"])
            k = i["child"]
            fk(k)
# def fk(k):
#     for i in k:
#             if i["parent_id"]==None:
#                 print("-",i["content"])
#                 for v in i["child"]:
#                     if i["id"]==v["parent_id"]:
#                         print("---"*i["id"],v["content"])
#                         k=i["child"]
#                         fk(k)
#             else:
#                 for v in i["child"]:
#                     if i["id"] == v["parent_id"]:
#                         print("--"*v["id"], v["content"])
#                         k = i["child"]
#                         fk(k)


msg_list_dict={}
result=[]
for i in msg_list:
    i["child"]=[]
    msg_list_dict[i["id"]]=i
# print(msg_list_dict)
for i in msg_list:
    pid=i["parent_id"]
    if pid:
        msg_list_dict[pid]["child"].append(i)
    else:
        result.append(i)
print(result)
# fk(result)




{
 1: {'id': 1, 'content': 'xxx', 'parent_id': None, 'child': []},
 2: {'id': 2, 'content': 'xxx', 'parent_id': None, 'child': []},
 3: {'id': 3, 'content': 'xxx', 'parent_id': None, 'child': []},
 4: {'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': []},
 5: {'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': []},
 6: {'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []},
 7: {'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []},
 8: {'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}
 }


{
1: {'id': 1, 'content': 'xxx', 'parent_id': None, 'child':
    [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child':
            [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child':
                [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]},
2: {'id': 2, 'content': 'xxx', 'parent_id': None, 'child':
    [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]},
3: {'id': 3, 'content': 'xxx', 'parent_id': None, 'child':
    [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]},
4: {'id': 4, 'content': 'xxx', 'parent_id': 1, 'child':
    [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child':
        [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]},
5: {'id': 5, 'content': 'xxx', 'parent_id': 4, 'child':
    [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]},
6: {'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []},
7: {'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []},
8: {'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}
}


{'id': 1, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]}
{'id': 2, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]}
{'id': 3, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]}

l=["a","b","c","d"]
print(l.index("c"))