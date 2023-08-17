from flask import Flask, render_template, request

app = Flask(__name__)


def quick_sort_special_struct(lists, i=None, j=None, target=None):  # 快速排序
    if i >= j:
        return list
    pivot = lists[i]
    low = i
    high = j
    while i < j:
        while i < j and lists[j][target] >= pivot[target]:
            j -= 1
        lists[i] = lists[j]
        while i < j and lists[i][target] <= pivot[target]:
            i += 1
        lists[j] = lists[i]
    lists[j] = pivot
    quick_sort_special_struct(lists, low, i - 1, target=target)
    quick_sort_special_struct(lists, i + 1, high, target=target)
    return lists


def read_user_data(file_name, sort_data: bool = False, cover_file: bool = True):
    user_info = []
    with open(file_name, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            user_info_dict = {}
            for info, value_ in (tuple(iter_item.split('=')) for iter_item in line.split(',')):
                user_info_dict.update({info: value_})
            user_info.append(user_info_dict)

    def sort_user_data(user_info_sort):
        user_info_sort = quick_sort_special_struct(user_info_sort, 0, len(user_info_sort) - 1, target='user_id')
        with open(file_name, 'w', encoding='utf-8') as file_sort:
            for info_sort in user_info_sort:
                begin_flag: bool = True
                for key, value in info_sort.items():
                    head = ',' if not begin_flag else ''
                    if begin_flag:
                        begin_flag = False
                    file_sort.write(head + key + '=' + value)
                file_sort.write('\n')

    if sort_data:
        user_info = quick_sort_special_struct(user_info, 0, len(user_info) - 1, target='user_id')
        if cover_file:
            sort_user_data(user_info)
    return user_info


def turing_type_join(*args, turing_type):
    items = map(turing_type, list(args))
    if turing_type == str:
        return ''.join(items)
    else:
        return items


def form_args_get(*args_name: str, obj=None) -> tuple:
    if obj is None:
        raise IOError('the obj is missing')
    try:
        for name in args_name:
            yield obj.get(name)
    except KeyError:
        return 'Error!the key not in form'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        user_info = read_user_data('user_data.txt', sort_data=True, cover_file=False)
        account, password, operation = form_args_get('account', 'password', 'operation', obj=request.form)
        if operation == 'L':
            for info_iter in user_info:
                if info_iter['account'] == account and \
                        info_iter['password'] == password:
                    return f"欢迎回来！user:{info_iter['user_id']}"
            return '账号或密码错误'
        elif operation == 'R':
            max_id = 0
            for info_iter in user_info:
                if account == info_iter['account']:
                    return f'Error!{account}已被注册'
                iter_id = int(info_iter['user_id'])
                max_id = iter_id if iter_id > max_id else max_id
            with open('user_data.txt', 'a+') as file:
                file.writelines(f'user_id={max_id + 1},account={account},password={password}\n')
            return f'注册成功！account:{account},password={password}'


if __name__ == '__main__':
    # read_user_data('user_data.txt', sort_data=True)
    app.run(host='127.0.0.1', port=5000)
    pass
    # info = read_user_data('user_data.txt', sort_data=True, cover_file=False)
    # print(info)
