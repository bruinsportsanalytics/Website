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
    body += '<center><img class=\"materialboxed responsive-img\" src =\"/assets\" alt=\"cover photo\"></center>'
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
    return '<div class=\"video-container\"><iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/<put end of embed link here>\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe></div>\n\n'

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

    # create author page
    author_page = open('{}.html'.format(name), 'w')
    author_page.write(body)

    # create author in yaml
    myAuthor = {
        underscore_name : {
            'name': ' '.join(underscore_name.split('_')),
            'web' : 'http://www.bruinsportsanalytics.com/{}'.format(name),
            'bio' : None
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
    for i in range(2, num_pics + 1):
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
