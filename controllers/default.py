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
from display import *
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
   
    if auth.user:
        #print "auth: " , auth.user_id
        redirect(URL('default', 'user'))
    else:
        redirect(URL('default', 'login'))
    

def old_index():
    return dict(error=T(''))

def user():
    """Home page of the user to display public links of people followed"""
    #print "user id", auth.user_id
    if not auth.user:
        redirect(URL("default", "login", args=["login"]));
    #Mrugani---
    q0 = myDB.auth_user.id == auth.user_id
    user_info = myDB(q0).select()
    public_links = get_public_links_count(myDB, auth.user_id)
    private_links = get_private_links_count(myDB, auth.user_id)
    followers =get_followees(myDB, auth.user_id)
    following = get_followers(myDB, auth.user_id)
    #Taking last entry as private link
    logged_in = user_details(user_info[0].id, user_info[0].first_name, user_info[0].last_name, user_info[0].username, 0,followers,following,public_links,private_links);
    logged_in.set_joining_date(int(user_info[0].Joining_date))

    #Siji------
    q1 = myDB.follow.follower == auth.user_id
    q2 = myDB.follow.followee == myDB.link.user_id
    q3 = myDB.link.visibility == "public"
    q4 = myDB.follow.followee == myDB.auth_user.id
    q5 = myDB.follow.followee == myDB.auth_user.id
    rows = myDB(q1 & q2 & q3 & q4 & q5).select(orderby="link.created_date DESC")
    L=[]
    for l in rows:
        tags = []   
        tags = l.link.tags.split(",")
        q6 = myDB.link.user_id == auth.user_id
        q7 = myDB.link.url == l.link.url
        check = myDB(q6 & q7).select()
        if len(check)==0:
            exist=0
        else:
            exist=1
        #print "exist " ,exist
        link_display=link(l.link.url, l.link.lid, tags, l.link.description, l.link.created_date, "public")
        user_display=user_details(l.link.user_id,l.auth_user.first_name,l.auth_user.last_name,l.auth_user.username,exist)
        user_display.set_link_details(link_display)
        #print "user_display.exist", user_display.exist
        L.append(user_display)
        #print user_display.firstname,user_display.lastname,user_display.username,user_display.link_details.url
    return dict(following=L, user=logged_in)

@auth.requires_login() 
def edit_profile():

    return dict(form=auth.profile())

@auth.requires_login() 
def search():

    """ Search by username, tags and url """

    if request.vars.keyword:
        keyword = request.vars.keyword
        option = request.vars.option

        """Search by user"""
        if option == "Users":
            keyword = "%"+keyword+"%"
            query = myDB.auth_user.username.like(keyword)
            rows = myDB(query).select()
            user_list = []
            for user in rows:
                id = user.id;
                
                followers =get_followees(myDB, id)

                following = get_followers(myDB, id)

                query_2 = myDB.auth_user.id == id;
                details = myDB(query_2).select()
                
                public_links = get_public_links_count(myDB, id)
                
                follow_details = get_is_following(myDB, id, auth.user_id)

                if follow_details:
                    follow = 1;
                else:
                    follow = 0;
                #Remaining- counts
                user_det = user_details(id,details[0].first_name, details[0].last_name, user.username, 0, followers, following, public_links, follow)
                user_det.set_joining_date(int(details[0].Joining_date))
                user_list.append(user_det)
            search_query = "Users="+keyword[1:-1]
            return dict(users=user_list, query=search_query)
        
        #Search by tags

        elif option == "Tags":
            
            keyword = "%"+keyword+"%"
            #check if keyword contains comma..
            query_1 = myDB.link.user_id == auth.user_id
            query_2 = myDB.link.tags.like(keyword)
            rows = myDB(query_1 & query_2).select()
            L = []
            for l in rows:
                tags = []
                tags = l.tags.split(",")
                link_save = link(l.url, l.lid, tags, l.description, l.created_date, l.visibility)
                L.append(link_save)
                
            query = "Tags="+keyword[1:-1]
            return dict(links=L, query=query)


        #search by URL
        elif option == "URL":
            keyword = "%"+keyword+"%"
            #check if keyword contains comma..
            query_1 = myDB.link.user_id == auth.user_id
            query_2 = myDB.link.url.like(keyword)
            rows = myDB(query_1 & query_2).select()
            L = []
            for l in rows:
                tags = []
                tags = l.tags.split(",")
                link_save = link(l.url, l.lid, tags, l.description, l.created_date, l.visibility)
                L.append(link_save)
                
            query = "URL="+keyword[1:-1]
            return dict(links=L, query=query)

    return dict()

@auth.requires_login() 
def show_links():

    """Retrieve links saved by the user from DB"""
    query_1 = myDB.link.user_id == auth.user_id
    rows = myDB(query_1).select()
    L = []
    size = len(rows)
    for l in rows:
        tags = []
        tags = l.tags.split(",")
        link_save = link(l.url, l.lid, tags, l.description, l.created_date, l.visibility)
        L.append(link_save)
   
    return dict(links=L)

@auth.requires_login() 
def follow():
    """Add entry in follow table """
    follower = request.vars.id1;
    followee = request.vars.id2;
    myDB.follow.insert(follower=follower, followee=followee)
    email_id = myDB(myDB.auth_user.id == followee).select(myDB.auth_user.email)
    subject = "Bookmarks "+auth.user.username + " is following you on this.save app"
    content = ""+ "\n\n\n\n\nRegards,\n"+"Admin\nthis.save\n";
    mail.send(email_id[0].email, subject, content)

@auth.requires_login() 
def unfollow():
    """Remove association from follow table """
    follower = request.vars.id1;
    followee = request.vars.id2;
    query = myDB.follow.follower==follower
    query_1 = myDB.follow.followee==followee
    myDB(query & query_1).delete()

@auth.requires_login() 
def delete():

    """delete the link with this id"""
    #print request.env.request_method
    query = myDB.link.lid == request.vars.id;
    myDB(query).delete()

@auth.requires_login() 
def check_if_url_exists():

    id = auth.user_id;
    url = request.vars.url;
    query_1 = myDB.link.user_id == id
    query_2 = myDB.link.url == url
    rows = myDB(query_1 & query_2).select()
    if rows:
        response.flash="Link already exists"
    else:
        response.flash=""
        return ""
         

def login():
    """
    DB changes 
    """
    if auth.user and request.args(0)=="change_password":
        return dict(form=auth())
    if auth.user:
        redirect(URL('default', 'user'))
    #print "In login:"
    return dict(form=auth())

@auth.requires_login() 
def logout():
    auth.logout()
    
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

@auth.requires_login() 
def chpassword():
        
    return dict(form=auth.change_password())

@auth.requires_login() 
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
        l = link(r[0].url, r[0].lid, r[0].tags, r[0].description, r[0].created_date, r[0].visibility)
        return dict(link=l,update_current=1)
        
    """ Add new link else """
    if request.vars.url:

        url = request.vars.url;
        desc = request.vars.description;
        tags = request.vars.tags
        vis = request.vars.vis;
        tm = int(time.time())
        id = auth.user_id;
        query_1 = myDB.link.user_id == id
        query_2 = myDB.link.url == url
        rows = myDB(query_1 & query_2).select()
        if rows:
            myDB(query_1 & query_1).update(visibility=vis, description=desc, tags=tags)
            return dict(message=T('Link has been updated Successfully')) 
        myDB.link.insert(user_id=auth.user_id, url=url, visibility=vis, tags=tags, description=desc, created_date=tm)
        return dict(message=T('Link has been added Successfully'))

    """ Add a link from followed user """
    if request.vars.follow_lid:
        q1 = myDB.link.lid == request.vars.follow_lid
        r = myDB(q1).select()
        l = link(r[0].url,r[0].lid, r[0].tags, r[0].description, r[0].created_date, "private")
        return dict(link=l,update_current=0)

    return dict()

@auth.requires_login() 
def trends():
    count = myDB.link.url.count()
    q1 = myDB.link.visibility == "public"
    result = myDB(q1).select(myDB.link.url, count, groupby = myDB.link.url, orderby=~count ,limitby=(0,10))
    q2 = myDB.auth_user.id
    no_of_users = myDB(q2).count()
    return dict(topten=result,users=float(no_of_users))


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
