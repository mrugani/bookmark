
def get_public_links_count(myDB, id):
	query_5 = myDB.link.user_id == id
	query_6 = (myDB.link.visibility == 'public')
	public_links = myDB(query_5 & query_6).count()
	return public_links


def get_private_links_count(myDB, id):
	query_5 = myDB.link.user_id == id
	query_6 = (myDB.link.visibility == 'private')
	public_links = myDB(query_5 & query_6).count()
	return public_links

def get_is_following(myDB, id1, id2):
	query_3 = myDB.follow.follower==id2
	query_4 = myDB.follow.followee==id1
	follow_details = myDB(query_3 & query_4).select()
	return follow_details

def get_followers(myDB, id):
	query_1 = myDB.follow.follower == id
	cnt = myDB(query_1).count()
	return cnt;

def get_followees(myDB, id):
	query_1 = myDB.follow.followee == id
	cnt = myDB(query_1).count()
	return cnt;



