#!/usr/bin/python3.6
"""Converter Tool from txt file to html for BSA"""

from time import localtime, strftime
from unidecode import unidecode
import sys
import csv
import os
import codecs
import yaml

def print_error(msg):
    """
    prints custom error messages

    :input:
            message (string)
    """
    sys.stderr.write(msg)
    sys.exit(1)


def add_p(msg):
    """
    returns message wrapped in paragraph tags and adds new lines

    :input:
            message (string)
    """
    return '<p>{}</p>\n\n'.format(msg)


def print_cover(title, authors, my_date, cov_par):
    """
    runs front matter to html post

    :input:
            title (string)
            author (currently just one)
            date (gathered from txt doc)
            cover_paragraph (string)
    """
    body = '---\n'\
        'layout: post\n'\
        'title:  \"{}\"\n'\
        'date:   {} -0700\n'\
        'authors:\n'.format(title, my_date)

    # gather current authors in case we don't need to create a new author page
    with open('_data/authors.yaml','r') as stream:
        try:
            myYaml = yaml.load(stream)
            bsa_authors = myYaml.keys()
        except yaml.YAMLError as exc:
            print(exc)

    for author in authors:
        body += '- {}\n'.format(author)
        if author not in bsa_authors:
            create_profile(author)

    body += 'categories: jekyll update\n'\
        'excerpt_separator: <!-- end excerpt here -->\n'\
        'excerpt: '
    body += '<center><img class=\"excerptpics\" src =\"/assets\" alt=\"cover photo\"></center>'
    body += '<p>{}</p>\n'.format(cov_par)
    body += '---\n'
    return body


def add_pic(num):
    """
    adds appropriate picture tags and marks the picture number

    :input:
            picture number (int)
    """
    return '<figure>\n\t<center><img class=\"materialboxed responsive-img\" src =\"/assets/pic_folder/pic_{}\" alt=\"picture {}\" style=\"max-width: 95%;\"><figcaption></figcaption></center>\n</figure>\n\n'.format(num, num)



def add_video():
    """
    adds appropriate video tags and marks the video number

    :input:
            video number (int)
    """
    return '<div class=\"video-container\"><iframe width=\"1425\" height=\"641\" src=\"embed_link\" frameborder=\"0\" allow=\"autoplay; encrypted-media\" allowfullscreen></iframe></div>\n\n'


def add_profile_content(name):
    return "<head>\n\
      <meta charset=\"utf-8\">\n\
      <meta content=\"width=device-width,initial-scale=1.0\" name=\"viewport\">\n\
      <meta content=\"description\" name=\"\">\n\
      <link rel=\"stylesheet\" href=\"/css/blog.css\">\n\
      <!-- css -->\n\
      <link rel=\"stylesheet\" href=\"http://fonts.googleapis.com/css?family=Roboto+Slab\">\n\
      <link rel=\"stylesheet\" href=\"/css/style.css\" type=\"text/css\">\n\
      <script src=\"https://code.jquery.com/jquery-2.1.4.min.js\"></script>\n\
      <script src=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js\"></script>\n\
      <style>\n\
      p.ex1 {{\npadding-left: 50px;\n}}\n\
      div.ex1 {{\npadding-top: 50px;\npadding-right: 15%;\npadding-left: 15%;\npadding-bottom: 5px;\n}}\n\
      </style>\n\n\
      </head>\n\n\
      {{% assign author = site.data.authors[page.author] %}}\n\n\
      <center><h4 style=\"font-family: Roboto slab, serif;\">{{ author.name }}</h4></center>\n\n\
      {{% assign author = site.posts | where: 'authors', '{}' %}}\n\n\
      <div class=\"ex1\">\n\
	  <main>\n<section class=\"module_content\">\n\
			<b><h5 style=\"font-family: Roboto slab, serif;\">Articles: </h5></b>\n\
			{{% for post in author %}}\n\
			<h2 style=\"font-family: Roboto slab, serif;\"><a href=\"{{ post.url }}\">{{ post.title }}</a></h2>\n\
            <h6 style=\"font-family: Roboto slab, serif;\">{{ post.date | date_to_string }} • {{% assign words = post.content | number_of_words %}}\n\
                    {{% if words < 360 %}}\n\
                      1 min read\n\
                    {{% else %}}\n\
                      {{ words | divided_by:200 }} min read\n\
                    {{% endif %}}</h6>\n\
            {{ post.excerpt }}\n\
			{{% endfor %}}\n\
		</section>\n\
	</main>\n\
    </div>".format(name)


def create_profile(underscore_name):
    """
    creates new authors page, and updates _data/authors.yaml

    :input:
        underscore_name
    """
    name = ''.join(underscore_name.split('_')) # bring together
    if name[0] == ' ':
        name = name[1:]
    
    # add content
    body = '---\n'\
        'author: {}\n'\
        'layout: default\n'\
        'permalink: /{}\n'\
        '---\n'.format(underscore_name, name)
    body += add_profile_content(underscore_name)

    # create author page
    author_page = open('{}.html'.format(name), 'w')
    author_page.write(body)

    # create author in yaml
    myAuthor = {
        underscore_name : {
            'name': ' '.join(underscore_name.split('_')),
            'web' : 'http://www.bruinsportsanalytics.com/{}'.format(name),
            'bio' : ''
        }
    }
    with open('_data/authors.yaml', 'r') as yamlFile:
        cy = yaml.load(yamlFile)
        cy.update(myAuthor)
    
    with open('_data/authors.yaml', 'w') as yamlFile:
        yaml.safe_dump(cy, yamlFile)
    
    author_page.close()

def main():
    """
    Converts txt file to html

    :input:
            txt file (file)
            number of pictures (int)
            number of videos (int)

    ex:
            ./convert.py ucla_gym.txt 7 1
    """
    if (len(sys.argv) != 4):
        print_error("Incorrect number of arguments\n")

    # read in unicode
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]  # get rid of \n
    content[0] = content[0].replace(u'\ufeff', '')  # get rid of \ufeff

    # TODO: get rid of '' inside content

    # gather titles
    title = content[0].split("Title:")[1].strip()
    authors = content[1].strip().split("Authors: ")[1].split(',')
    my_date = strftime("%Y-%m-%d %H:%M:%S", localtime())
    file_name = f.name.split(".txt", 1)[0]

    # get cover paragraph
    for i in range(3, len(content)):
        if content[i]:
            cov_par = unidecode(content[i])
            break

    body = print_cover(title, authors, my_date, cov_par)

    # add cover photo
    body += '<figure>\n\t<center><img class=\"materialboxed responsive-img\" src =\"/assets/pic_folder/photo\" alt=\"cover photo\"><figcaption></figcaption></center>\n</figure>\n\n'
    # wrap the rest
    for i in range(3, len(content)):
        if content[i]:
            body += add_p(unidecode(content[i]))

    # set up picture frames
    num_pics = int(sys.argv[2])
    for i in range(1, num_pics + 1):
        body += add_pic(i)

    # num of video frames
    num_videos = int(sys.argv[3])
    for i in range(num_videos):
        body += add_video()

    # write changes to new html file
    # format: date-articlename.html
    out = open('{}-{}.html'.format(my_date.split(' ')[0], file_name), 'w')
    out.write(body)

    # close file descriptors
    f.close()
    out.close()


if __name__ == '__main__':
    main()
