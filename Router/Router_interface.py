from Router.User import login
from Router.User import register
from Router.Router_basic_func import get_index
from Router.TW import TW_index
from Router import check_login2
from Router.TW import TW_add
from Router.TW import TW_all
from Router.TW import TW_del
from Router.TW import TW_edit
from Router.Comment import TW_comment
from Router.Comment import TW_comment_all
from Router.Comment import TW_comment_add
from Router.Comment import TW_comment_del

Router_dict = {
    '/login': login,
    '/register': register,
    '/': get_index,
    '/TW': check_login2(TW_index),
    '/TW/add': check_login2(TW_add),
    '/TW/all': check_login2(TW_all),
    '/TW/del': check_login2(TW_del),
    '/TW/edit': check_login2(TW_edit),
    '/TW/comment': check_login2(TW_comment),
    '/TW/Comment/all':check_login2(TW_comment_all),
    '/TW/comment/add':check_login2(TW_comment_add),
    '/TW/comment/del':check_login2(TW_comment_del),
}
