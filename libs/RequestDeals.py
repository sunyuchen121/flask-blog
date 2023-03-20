from views.blog import blog_bp
from flask import request, g


@blog_bp.before_request
def deal_page_param():
    def deal_minus(num, default=1):
        if num < 0:
            return -num
        elif num == 0:
            return default
        return num

    if request.method == "GET":
        page_index, page_size = deal_minus(request.args.get("page_index", 1, int)), deal_minus(
            request.args.get("page_size", 10, int), 10)
    else:
        page_index, page_size = deal_minus(request.form.get("page_index", 1, int)), deal_minus(
            request.form.get("page_size", 10, int), 10)
    g.d_page_size, g.d_page_index = page_size, page_index
