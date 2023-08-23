import sys

sys.path.append("/home/dungnguyen/work/Neo4j-social-network/iclib")

import re

from iclib.ic_sqlserver import DatabaseIO

dbio = DatabaseIO(
    server="10.9.3.34",
    user="viet.le",
    password="G6pT6u9y",
    database="msocial",
    driver="ODBC Driver 17 for SQL Server",
    port="1433",
)


def clean_text(text):
    """
    Remove special characters except Vietnamese alphabet and punctuation
    """

    cleaned_text = re.sub(
        r"[^\w\s.!?,áàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴ\n]",
        "",
        text,
    )
    return cleaned_text


def get_user_top_comments(uid: str, no_cmt=20, norm_text=True):
    """
    Retrieves the top comments made by a user on Facebook.

    Parameters:
        uid (str): The user's Facebook ID.
        no_cmt (int, optional): The number of top comments to retrieve.

    Returns:
        ls_comments: Content of the user's top comments.
    """

    cur = dbio.query_db(
        f"""
        SELECT TOP {no_cmt} Content
        FROM FBComments
        WHERE FBid = {uid}
        ORDER BY Date DESC
    """
    )

    ls_comments = [record[0] for record in cur]
    if norm_text:
        ls_comments = [clean_text(comment) for comment in ls_comments]
    ls_comments= list(set(ls_comments))

    return ls_comments


def get_user_top_posts(uid: str, no_post=5, norm_text=True):
    """
    Retrieves the top posts made by a user on Facebook.

    Parameters:
        uid (str): The user's Facebook ID.
        no_post (int, optional): The number of top posts to retrieve.

    Returns:
        ls_posts: Content of the user's top posts.
    """

    cur = dbio.query_db(
        f"""
        SELECT TOP {no_post} Content
        FROM FBFeeds
        WHERE FBid = {uid}
        ORDER BY CreatedDate DESC
    """
    )

    ls_posts = [record[0] for record in cur]
    if norm_text:
        ls_posts = [clean_text(post) for post in ls_posts if post]
    ls_posts = list(set(ls_posts))

    return ls_posts


def get_user_basic_info(uid: str):
    """
    Retrieves user basic information .

    Parameters:
        uid (str): The user's Facebook ID.

    Returns:
        has_info (bool): Indicates whether information for the user was found.
        user_info (dict): A dictionary containing user information if available.
    """

    cur = dbio.query_db(
        f"""
        SELECT TOP 200 FBPublicName, UserEmail
        FROM AccountEmailInfo
        WHERE FBId = {uid}
    """
    )

    has_info = False
    user_info = {}

    for record in cur:
        user_info = {"uid": uid, "fb_public_name": record[0], "user_email": record[1]}
        has_info = True

        return has_info, user_info

    return has_info, user_info


def get_user_data(uid, no_post=10, no_cmt=20, norm_text=True):
    """
    Retrieves various data about a user on Facebook, including basic info, top posts, and top comments.

    Parameters:
        uid (str): The user's Facebook ID.
        no_post (int, optional): The number of top posts to retrieve. Default is 5.
        no_cmt (int, optional): The number of top comments to retrieve. Default is 20.

    Returns:
        dict: A dictionary containing user-related data.
    """

    _, user_info = get_user_basic_info(uid)
    top_posts = get_user_top_posts(uid, no_post, norm_text)
    top_comments = get_user_top_comments(uid, no_cmt, norm_text)

    res = {"user_info": user_info, "top_comments": top_comments, "top_posts": top_posts}
    return res
