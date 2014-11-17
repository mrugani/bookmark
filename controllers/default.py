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
from link import *
from user_details import *
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
    """Home page of the user to display public links of people followed"""
    q1 = myDB.follow.follower == session.uid
    q2 = myDB.follow.followee == myDB.link.user_id
    q3 = myDB.link.visibility == "public"
    q4 = myDB.follow.followee == myDB.personal_details.user_id
    q5 = myDB.follow.followee == myDB.credentials.username
    rows = myDB(q1 & q2 & q3 & q4 & q5).select()
    L=[]
    for l in rows:
        print l.credentials.username
        '''
        tags = []   
        tags = l.link.tags.split(",")
        link_display=link(l.link.url, l.link.lid, tags, l.link.description, l.link.date, "public")
        user_display=user_details(l.)
        '''
    return dict()


def search():

    """ Search by username, tags and url """

    if request.vars.keyword:
        keyword = request.vars.keyword
        option = request.vars.option

        """Search by user"""
        if option == "Users":
            print "User selected ", keyword
            keyword = "%"+keyword+"%"
            query = myDB.credentials.username.like(keyword)
            rows = myDB(query).select()
            user_list = []
            for user in rows:
                id = user.user_id;
                query_2 = myDB.personal_details.user_id == id;
                details = myDB(query_2).select()
                query_3 = myDB.follow.follower==session.uid
                query_4 = myDB.follow.followee==id

                follow_details = myDB(query_3 & query_4).select()

                if follow_details:
                    follow = 1;
                else:
                    follow = 0;

                #Remaining- counts
                user_det = user_details(id,details[0].first_name, details[0].last_name, user.username, 0, 0, 0, follow)
                user_list.append(user_det)
            search_query = "Users="+keyword[1:-1]
            return dict(users=user_list, query=search_query)
        
        #Search by tags

        elif option == "Tags":
            
            keyword = "%"+keyword+"%"
            #check if keyword contains comma..
            query_1 = myDB.link.user_id == session.uid
            query_2 = myDB.link.tags.like(keyword)
            rows = myDB(query_1 & query_2).select()
            L = []
            for l in rows:
                tags = []
                tags = l.tags.split(",")
                link_save = link(l.url, l.lid, tags, l.description, l.date, l.visibility)
                L.append(link_save)
                
            query = "Tags="+keyword[1:-1]
            return dict(links=L, query=query)


        #search by URL
        elif option == "URL":
            print "OPtion selected URL"
            keyword = "%"+keyword+"%"
            #check if keyword contains comma..
            query_1 = myDB.link.user_id == session.uid
            query_2 = myDB.link.url.like(keyword)
            rows = myDB(query_1 & query_2).select()
            L = []
            for l in rows:
                tags = []
                tags = l.tags.split(",")
                link_save = link(l.url, l.lid, tags, l.description, l.date, l.visibility)
                L.append(link_save)
                
            query = "URL="+keyword[1:-1]
            return dict(links=L, query=query)

    return dict()


def show_links():

    """Retrieve links saved by the user from DB"""
    query_1 = myDB.link.user_id == session.uid
    rows = myDB(query_1).select()
    L = []
    size = len(rows)
    for l in rows:
        tags = []
        tags = l.tags.split(",")
        link_save = link(l.url, l.lid, tags, l.description, l.date, l.visibility)
        L.append(link_save)
   
    return dict(links=L)

def follow():
    """Add entry in follow table """
    follower = request.vars.id1;
    followee = request.vars.id2;
    myDB.follow.insert(follower=follower, followee=followee)

def unfollow():
    """Remove association from follow table """
    follower = request.vars.id1;
    followee = request.vars.id2;
    query = myDB.follow.follower==follower
    query_1 = myDB.follow.followee==followee
    myDB(query & query_1).delete()

def delete():

    """delete the link with this id"""
    #print request.env.request_method
    print "deleting " , request.vars.id
    query = myDB.link.lid == request.vars.id;
    myDB(query).delete()

    
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
        redirect('user')
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

    """ Check for update link """

    if request.vars.lid:
        url = request.vars.url;
        desc = request.vars.description;
        tags = request.vars.tags
        vis = request.vars.vis;
        query = myDB.link.lid == request.vars.lid
        myDB(query).update(url=url, visibility=vis, description=desc, tags=tags)
        return dict(message=T('Link updated Successfully'))

    if request.vars.id:
        query = myDB.link.lid == request.vars.id;
        r = myDB(query).select();
        l = link(r[0].url, r[0].lid, r[0].tags, r[0].description, r[0].date, r[0].visibility)
        return dict(link=l)
        
    """ Add new link else """
    if request.vars.url:

        url = request.vars.url;
        desc = request.vars.description;
        tags = request.vars.tags
        vis = request.vars.vis;
        tm = int(time.time())
        myDB.link.insert(user_id=session.uid, url=url, visibility=vis, tags=tags, description=desc, date=tm)
        return dict(message=T('Link has been added Successfully'))

    return dict()





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
