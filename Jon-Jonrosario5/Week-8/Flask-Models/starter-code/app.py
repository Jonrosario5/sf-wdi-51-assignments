from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import models
from forms import SubForm
from forms import PostForm
from forms import CommentForm



DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'adkjfalj.adflja.dfnasdf.asd'

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/', methods=['GET','POST'])
def index():
    # the form variable we send down to the template needs to be added here
    form = SubForm()
    if form.validate_on_submit():
        models.Sub.create(name=form.name.data.strip(),
        description=form.description.data.strip())
        flash("New sub registered. Called: {}".format(form.name.data))

        return redirect('/r')

    return render_template("new_sub.html", title="New Sub", form=form)

@app.route('/r')
@app.route('/r/<sub>', methods=['GET','POST'])
def r(sub=None):
    if sub == None:
        subs= models.Sub.select().limit(100)
        return render_template('subs.html', subs=subs)
    else:
        #find the right sub
        sub_id = int(sub)
       
        #Send the found Sub to the template
        sub = models.Sub.get(models.Sub.id == sub_id)

        #setting posts to equal sub.posts
        posts= sub.posts

        form = PostForm()
        if form.validate_on_submit():
            models.Post.create(
                user=form.user.data.strip(),
                title = form.title.data.strip(),
                text= form.text.data.strip(),
                sub=sub)
            flash("New Post Created")
            #Redirect the user to the sub where it was created.
            return redirect('/r/{}'.format(sub_id))
        return render_template('sub.html',sub=sub, form=form,posts=posts)


@app.route('/posts')
@app.route('/posts/<id>',methods=['GET','POST'])
def posts(id=None):
      if id == None:
        posts = models.Post.select().limit(100)
        return render_template('posts.html', posts=posts)
      else:
        post_id = int(id)
        post = models.Post.get(models.Post.id == post_id)
        comments = post.comments
        form = CommentForm()
        if form.validate_on_submit():
            models.Comment.create(
                user=form.user.data.strip(),
                text = form.text.data.strip(),
                post=post)
            flash("New Comment Added")
            return redirect('/posts/{}'.format(post_id))
            
        return render_template('post.html', post=post, form=form, comments=comments)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
