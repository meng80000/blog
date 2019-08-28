

def comment_tree(comment_list):
    """
    评论楼--递归函数
    :param comment_list:
    :return:
    """
    comment_str="<div class='comment'>"
    for row in comment_list:
        tpl="<div class='content'>%s"%(row["content"])
        comment_str+=tpl
        if row["child"]:
            child_str=comment_tree(row["child"])
            comment_str+=child_str
    comment_str+="</div>"
    return comment_str