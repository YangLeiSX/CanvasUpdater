# -*- coding: utf-8 -*-
# @author: YangLeiSX
# @data: 2020-04-06

from bs4 import BeautifulSoup
import json
import os
import sys
from time import sleep
from PyQt5.QtCore import qDebug
from PyQt5.QtCore import QThread


class CanvasUpdate(QThread):
    def __init__(self, parent, session=None):
        super(CanvasUpdate, self).__init__()
        '''login and open session'''
        self.login_url = "https://oc.sjtu.edu.cn/login/openid_connect"
        self.base_url = "https://oc.sjtu.edu.cn/"
        self.course_url = "https://oc.sjtu.edu.cn/courses"
        self.session = session
        self.parent = parent
        self.status = False

        self.log_dir = os.path.join(
                       os.path.split(os.path.abspath(__file__))[0],
                       "log")
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

    def run(self):
        self.parent.LogInfo.emit("[MSG]Getting course information...")
        self.courses = self.get_course()
        with open(os.path.join(self.log_dir, 'courses.json'), 'w') as f:
            f.write(json.dumps(self.courses))
        self.parent.LogInfo.emit("Done.\n")

        self.parent.LogInfo.emit("[MSG]Getting files' root...")
        self.courses_root = self.get_all_root()
        with open(os.path.join(self.log_dir, 'courses_root.json'), 'w') as f:
            f.write(json.dumps(self.courses_root))
        self.parent.LogInfo.emit("Done.\n")

        self.parent.LogInfo.emit("[MSG]Getting all files...\n")
        self.file_tree = self.get_file_tree()
        with open(os.path.join(self.log_dir, 'file_tree.json'), 'w') as f:
            f.write(json.dumps(self.file_tree))
        self.parent.LogInfo.emit("[MSG]Getting all files Successfully!\n")
        self.parent.FetchFinish.emit()

    def get_course(self):
        '''parse the page and get courses'''
        course_page = self.session.get(self.course_url)
        soup = BeautifulSoup(course_page.text, "html.parser")
        courses = soup.find_all('td',
                                {'class': 'course-list-course-title-column'})
        courses = [c.find_all('a') for c in courses]
        # get course id and course name
        course_pair = {}
        for course in courses:
            try:
                line = str(course[0])
            except IndexError:
                continue
            else:
                pass  # 未开课课程
            line = line.split(' ')
            while '' in line:
                line.remove('')
            path = line[1].split('=')[-1].split('"')[1]
            cid = path.split('/')[-1]
            name = line[2].split('"')[1]
            course_pair[cid] = name
        return course_pair

    def get_root(self, course_id):
        root_url = "{}{}{}".format("https://oc.sjtu.edu.cn/api/v1/courses/",
                                   course_id, "/folders/root")
        files_root = self.session.get(root_url)
        files_root = json.loads(files_root.text[9:])
        try:
            files_url = files_root['files_url']
            folders_url = files_root['folders_url']
            files_count = files_root['files_count']
            folders_count = files_root['folders_count']
        except KeyError:
            qDebug("weishouquan")
            return
        return {
                'name': self.courses[course_id],
                'files_url': files_url,
                'folders_url': folders_url,
                'files_count': files_count,
                'folders_count': folders_count
                }

    def get_all_root(self):
        all_root = {}
        for k, v in self.courses.items():
            qDebug(k)
            result = self.get_root(k)
            if result:
                all_root[k] = result
                qDebug("get {}".format(k))
            else:
                qDebug("no files")
            sleep(1)
        return all_root

    def get_file_tree(self):
        file_tree = {}
        for k, v in self.courses_root.items():
            # qDebug(v['name'])
            self.parent.LogInfo.emit("[MSG]Getting ")
            self.parent.LogInfo.emit(v['name'])
            self.parent.LogInfo.emit("...")
            folders_list = self.get_folders(v['folders_url'])
            files_list = self.get_files(v['files_url'])
            file_tree["{}".format(k)] = folders_list+files_list
            self.parent.LogInfo.emit("Done\n")
            sleep(1)
        return file_tree

    def get_folders(self, url):
        qDebug("folders_url is {}".format(url))
        content = self.session.get(url)
        sleep(0.5)
        content = json.loads(content.text[9:])
        folders_list = []
        for item in content:
            folder = {}
            folder['name'] = item['name']
            if item['folders_count'] != 0:
                subfolder = self.get_folders(item['folders_url'])
            else:
                subfolder = []
            if item['files_count'] != 0:
                subfiles = self.get_files(item['files_url'])
            else:
                subfiles = []
            folder['content'] = subfolder + subfiles
            folders_list.append(folder)
            sleep(1)
        return folders_list

    def get_files(self, url):
        qDebug("file_url is {}".format(url))
        files = self.session.get(url)
        sleep(0.5)
        files = json.loads(files.text[9:])
        files_list = []
        for item in files:
            name = item['display_name']
            url = item['url']
            files_list.append({'name': name, 'url': url})
        return files_list


if __name__ == "__main__":
    main = CanvasUpdate()
    main.run()
