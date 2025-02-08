
from flask import Flask, request, render_template, redirect, url_for
import datetime
app = Flask(__name__)


posts = [ { "pid":1, "title": "good day" , "category": "Technology", "content":"hahaha", "date_published":"01/15/2025"} ,
          { "pid":2, "title": "snow day" , "category": "Bussiness", "content":"hohoho", "date_published":"01/16/2025"},
          { "pid":3, "title": "windy day" , "category": "Food", "content":"hihihi", "date_published":"01/17/2025"} ]

globle_max_post_id = 3



@app.route('/', methods=['GET'])
def homepage():
    msg = request.args.get("errorMsg")
    if msg == None:
        msg = ""

    return render_template("index.html", posts = posts, errorMsg = msg)



def get_list_item( listItem, idNmae, targetId):
    for index, item in enumerate( listItem):
        if item[idNmae] == targetId:
            return listItem[ index]
    return None


@app.route('/post/<pid>', methods=['GET'])
def get_one_posts(pid):
    pid = int(pid)
    global posts
    post = get_list_item( posts, "pid", pid)
    if post:
        return render_template("post.html", post = post)
    
    errorMsg = f"post id: {pid} not found !! pls try again" 
    return render_template("post.html", errorMsg = errorMsg)


def get_now_time_with_format():
    timeNow = datetime.datetime.now()
    month = str (timeNow.month) 
    month = "0" + month  if len( month) == 1 else  month
    day = str (timeNow.day)
    day = "0" + day  if len( day) == 1 else  day 
    timeFormat = f"{month}/{day}/{timeNow.year}"
    return timeFormat

def add_to_db_posts(title, category, content):
    global posts
    global globle_max_post_id

    timeFormat = get_now_time_with_format()

    postDict = { "pid":globle_max_post_id + 1, "title": title, "category": category, "content": content, "date_published":timeFormat}
    posts.append(postDict)
    globle_max_post_id += 1
    return None


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    global posts
    if request.method == 'POST':
        add_to_db_posts(request.form["title"], request.form["category"], request.form["content"])
        return redirect(url_for("homepage", errorMsg = "post added successfull!! post id: " + str(globle_max_post_id)))
    return render_template("add_post.html")

@app.route('/update_post/<pid>' , methods=['GET', 'PUT'])
def update_post(pid):
    global posts
    pid = int(pid)
    post = get_list_item( posts, "pid", pid)
    if post == None:
        return render_template("update_post.html", errorMsg = f"post id: {pid} not found !! pls try again")

    if request.method == 'PUT':
        # print('got PUT!!')
        json_data = request.json
 
        post["title"]= json_data["title"]
        post["category"]= json_data["category"]
        post["content"]= json_data["content"]
        post["date_published"]= get_now_time_with_format() 

        return redirect(url_for("homepage", errorMsg = f"post update successfull!! post id: {pid} " ))
   
    return render_template("update_post.html", post = post)



def get_all_category_list():
    global posts
    category_list = []
    for post in posts:
        category_list.append(post["category"])
    return list(set(category_list))

@app.route('/category', methods=['GET'])
def get_post_by_category():
    global posts
    category_list = get_all_category_list()
    category_require = request.args.getlist("category") 
    if category_require == []: 
        return render_template("category.html", category_list = category_list, errorMsg = "pls select category, multi-select is supported!!")
    
    if len( category_require)>0: 
        postAns = []
        for c in posts:
            if c["category"] in category_require:
                postAns.append(c)
        
        msg = "filter by category: " + str(category_require)
        return render_template("category.html", posts =postAns, category_list = category_list,errorMsg =msg)    
    
    return render_template("category.html")

if __name__ == "__main__":
    app.run(debug=True)

