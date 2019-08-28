

def comment_tree(comment_list):
    """
    评论楼--递归函数
    :param comment_list:
    :return:
    """
    comment_str="<div class='comment'>"
    for row in comment_list:
        tpl="<div class='content'><a href='/blog/%s/'>%s</a> ：%s<a onclick='come()'>回复</a></div>"%(row["user__blog__site"],row["user__nickname"],row["content"])
        comment_str+=tpl
        if row["child"]:
            child_str=comment_tree(row["child"])
            comment_str+=child_str
    comment_str+="</div>"
    return comment_str