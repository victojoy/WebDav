import os
from flask import Flask
from flask import request
from flask import json
from flask import send_file

app = Flask(__name__)


@app.route('/root/')
def index():
    print('root')
    folder = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    goToRoot()
    if (folder == 1) & (name != None):
        createFolder(name)
    elif (folder == 2) & (name != None):
        deleteEmptyFolder(name)
    if (file == 1) & (name != None):
        print('zashel')
        return send_file('root/'+name, as_attachment=True)
    return makeList()


@app.route('/root/<path:path>')
def dir(path):
    print('dir')
    folder = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    goToRoot()
    os.chdir('./'+path)
    if (folder == 1) & (name != None):
        createFolder(name)
    elif (folder == 2) & (name != None):
        deleteEmptyFolder(name)
    if (file == 1) & (name != None):
        return send_file('root/'+path+'/'+name, as_attachment=True)
    return makeList()

#метод, который переносит в папку root
def goToRoot():
    try:
        os.chdir('./root')
    except FileNotFoundError:
        while os.path.basename(os.getcwd()) != 'root':
            os.chdir('..')

def createFolder(name):
    os.mkdir(name)

def deleteEmptyFolder(name):
    try:
        os.rmdir(name)
    except OSError:
        print('Folder is not empty')

def makeList():
    list = []
    for name in os.listdir():
        newPath = './' + name
        if os.path.isfile(newPath):
            type = 'file'
        else:
            type = 'folder'
        obj = {'name': name, 'type': type}
        list.append(obj)
    return json.dumps(list, ensure_ascii=False)

if __name__ == '__main__':
    app.run()