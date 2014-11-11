# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import time
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(error=T(''))

def user():
    return dict()


def login():
    """
    DB changes 
    """
    name = request.vars.username
    password = request.vars.password
    #myDB = DAL('mysql://root:Admin123@localhost/bookmarks')
    query_1 = myDB.credentials.username == name
    query_2 = myDB.credentials.password == password   
    rows = myDB(query_1 & query_2).select()
    if rows:
        #redirect to home page
        session.uid=rows[0].user_id
        response.view = "default/user.html"
        return dict(error=T("Successful login"))
    else:
        response.view = 'default/index.html'
        return dict(error=T("Username/Password is wrong"))

def register():

    email = request.vars.email
    fname = request.vars.firstname
    lname = request.vars.lastname
    username = request.vars.uname
    password = request.vars.passwd
    myDB.credentials.insert(username=username, password=password)
    query_1 = myDB.credentials.username == username
    query_2 = myDB.credentials.password == password
    rows = myDB(query_1 & query_2).select()
    if rows:
        uid = rows[0].user_id
        myDB.personal_details.insert(user_id=uid, first_name=fname, last_name=lname, email=email)
    return "Success"

def signup():
    return dict()

def chpassword():

    if request.vars.old_password:
        old = request.vars.old_password
        new = request.vars.new_passwd
        uid = session.uid;
        query_1 = myDB.credentials.user_id == uid;
        rows = myDB(query_1).select();
        if rows:
            if rows[0].password != old:
                return dict(error=T(''))
        myDB(query_1).update(password=new)
        return dict(message=T(''))        

    return dict()

def addlink():

    if request.vars.url:

        url = request.vars.url;
        desc = request.vars.description;
        tags = request.vars.tags
        vis = request.vars.vis;
        tm = int(time.time())
        myDB.link.insert(user_id=1, url=url, visibility=vis, tags=tags, description=desc, date=tm)
        return dict(message=T(''))

    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
