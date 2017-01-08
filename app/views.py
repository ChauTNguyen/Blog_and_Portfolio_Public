from flask import render_template, request, flash, redirect, url_for, jsonify

from .config import ADMINS
from .forms import ContactForm, SubscribeForm, CommentForm
from .utils import *
from collections import namedtuple

ips_and_nop = {}


# TODO: ADD SPAM FILTERS FOR ALL FORMS
@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify(ips_and_nop), 200


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


Project = namedtuple('Project', ['filename', 'display_title', 'title', 'img_url', 'description'])

projects_info = [
    Project(
        'this_site', 'Portfolio & Blog', '{ this website }',
        'flask_portfolio.png',
        'Completely responsive Portfolio/Blog Site powered by Flask.'
        ),
    Project(
        'grader', 'Grader', '{ grader }',
        'grader.png',
        'Django Gradebook web application with a convenient grading workflow (through urls and proper form handling), simple UI by MaterializeCSS, and graphs by C3.js.'
        ),
    Project(
        'mean_bookstore', 'MEAN Bookstore', '{ mean_bookstore }',
        'mean_bookstore.png',
        'RESTful & CRUDDY bookstore application for a mock bookstore.'
        ),
    Project(
        'sf_crime_viewer', 'SF Crime Viewer', '{ sf crime viewer }',
        'sf_crime_viewer.png',
        'Simple React-driven web application to view crime incidents in San Francisco as plot points using the Google Maps API and marker clusterer library.'
        ),
    Project(
        'terminal_chat', 'Terminal-themed Chat', '{ terminal-themed chat }',
        'terminal_chat.png',
        'Simple terminal-themed chat application using the Socket.IO library.'
        ),
    Project(
        'reddit_cli_email', 'Reddit Email CLI Tool', '{ reddit CLI email newsfeed tool }',
        'terminal_and_email.png',
        'Some random one-off Reddit utility (Python script) using PRAW.'
        ),
    Project(
        'league_dpm_grapher', 'LoL DPM Grapher', '{ league dpm grapher }',
        'riot_api_dpm_grapher.png',
        'Another one-off Python script using Riot\'s API.'
        )
]


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', projects=projects_info, img_base_link='images/project_thumbnails/')


@app.route('/portfolio/<int:project_id>')
def projects(project_id):
    return render_template(
        'tech/projects/' + projects_info[project_id - 1].filename + '.html',
        project_id=project_id, title=projects_info[project_id - 1].title
    )


@app.route('/portfolio/resume')
def resume():
    return render_template('tech/resume.html')


@app.route('/blog/0')
def blog():
    blog_posts_info = get_blog_info()
    num_of_blog_posts = len(blog_posts_info['posts'][0])

    # Get blog post titles.
    blog_post_titles = []
    for i in range(0, num_of_blog_posts):
        blog_post_titles.append(blog_posts_info['posts'][0][str(i + 1)]['title'])

    # Get the number of comments per blog post.
    # Note, this for loop starts at 1 and ends on len+1.
    # This is because the blog_post_ids are 1-indexed and not 0-indexed.
    num_of_comments_per_post = []
    for i in range(1, num_of_blog_posts + 1):
        try:
            num_of_comments_per_post.append(
                db.session.query(models.Comment).filter(models.Comment.blog_post_id == i).count()
            )
        except TypeError:
            num_of_comments_per_post.append(0)

    # Get the last five comments posted.
    recent_comments = db.session.query(models.Comment).order_by(models.Comment.id.desc())[0:5]

    # Get all tags.
    all_tags = set()
    for i in range(0, num_of_blog_posts):
        for j in range(0, len(blog_posts_info['posts'][0][str(i + 1)]['tags'])):
            all_tags.add(blog_posts_info['posts'][0][str(i + 1)]['tags'][j])

    sorted_all_tags = sorted(all_tags)

    return render_template(
        'blog/0.html',
        blog_post_titles=blog_post_titles,
        num_of_comments_per_post=num_of_comments_per_post,
        recent_comments=recent_comments,
        all_tags=sorted_all_tags
    )


@app.route('/blog/tags/<string:tag_name>')
def tags(tag_name):
    blog_posts_info = get_blog_info()

    posts_ids_and_titles = {}

    for i in range(0, len(blog_posts_info['posts'][0])):
        for j in range(0, len(blog_posts_info['posts'][0][str(i + 1)]['tags'])):
            if blog_posts_info['posts'][0][str(i + 1)]['tags'][j] == tag_name:
                posts_ids_and_titles[blog_posts_info['posts'][0][str(i + 1)]['post-id']] = \
                    blog_posts_info['posts'][0][str(i + 1)]['title']

    return render_template(
        'blog/tags.html',
        tag_name=tag_name,
        posts_ids_and_titles=posts_ids_and_titles
    )


@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    blog_posts_info = get_blog_info()

    if post_id > len(blog_posts_info['posts'][0]):
        return render_template('error_pages/404.html')

    title = blog_posts_info['posts'][0][str(post_id)]['title']

    subscribe_form = SubscribeForm()
    comment_form = CommentForm()

    # Tags for all blog posts
    tags = []
    for i in range(0, len(blog_posts_info['posts'][0])):
        tags.append(blog_posts_info['posts'][0][str(i + 1)]['tags'])

    if request.method == 'POST':
        form_name = request.form['form-name']

        if form_name == 'form1':
            if subscribe_form.validate_on_submit():
                subscribe(subscribe_form.email.data)
            else:
                flash_all_errors_from_form(subscribe_form)

        elif form_name == 'form2':
            if comment_form.validate_on_submit():
                if request.remote_addr in ips_and_nop:
                    if ips_and_nop[request.remote_addr] > 3:
                        flash('You have posted too many times today.')
                        return redirect(url_for('show_post', post_id=post_id))

                post_comment(app, post_id, comment_form.nickname.data, comment_form.message.data)

                if request.remote_addr not in ips_and_nop:
                    ips_and_nop[request.remote_addr] = 1
                else:
                    ips_and_nop[request.remote_addr] += 1
                    # add here
            else:
                flash_all_errors_from_form(comment_form)

        return redirect(url_for('show_post', post_id=post_id))

    if request.method == 'GET':
        return render_template(
            'blog/' + str(post_id) + '.html', post_id=post_id, title=title,
            last_updated=blog_posts_info['posts'][0][str(post_id)]['last_updated'],
            subscribe_form=subscribe_form, comment_form=comment_form,
            comments=get_comments_for_blog_post(post_id), tags=tags[post_id - 1]
        )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if not form.validate():
            flash_all_errors_from_form(form)
            return redirect(url_for('contact'))
        else:
            if request.remote_addr in ips_and_nop:
                if ips_and_nop[request.remote_addr] > 3:
                    flash('You have posted too many times today.')
                    return redirect(url_for('contact'))

            send_contact_email(
                form.subject.data,
                'ChauTNguyen96@gmail.com',
                recipients=ADMINS,
                email=form.email.data,
                message=form.message.data
            )

            if request.remote_addr not in ips_and_nop:
                ips_and_nop[request.remote_addr] = 1
            else:
                ips_and_nop[request.remote_addr] += 1

            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@app.route('/unsubscribe/<int:id>/<string:email>')
def unsubscribe(id, email):
    try:
        e = models.Subscriber.query.filter_by(id=id).first()
        db.session.delete(e)
        db.session.commit()
    except:
        return render_template('error_pages/404.html')
    return "You have unsubscribed from the blog."


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404
