import pymysql
import os

from utils import get_count_from_cursor_execution

class UserPlaylistResource:
    def __init__(self):
        pass

    @staticmethod
    def _get_connection(db=None):
        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        if db:
            conn = pymysql.connect(
                user=usr,
                password=pw,
                host=h,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
                database=db
            )
        else:
            conn = pymysql.connect(
                user=usr,
                password=pw,
                host=h,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        return conn

    @staticmethod
    def addUserToPlaylist(newUserId, playlistId):
        """
        elevateduserId grants permission for newUserId to add songs
        to playlist

        :param newUserId: new user ID being added
        :param playlistId: playlist ID
        :return: True if user is added, False otherwise
        """

        sql = """
        insert into PlaylistAccess.UserPlaylist (userId, playlistId, ownerId)
        values (%s, %s, %s);
        """

        # ownerId = UserPlaylistResource.__getOwner(playlistId)

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            # cursor.execute(sql, (newUserId, playlistId, ownerId, elevatedUserId, playlistId))
            cursor.execute(sql, (newUserId, playlistId, 'COFFEE'))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def removeUserFromPlaylist(userIdToRemove, playlistId):
        """
        Attempts to remove a user from a playlist

        :param userIdToRemove: user ID that will be removed
        :param playlistId: playlist ID
        :return: True if the user can and is removed, False otherwise
        """

        # if UserPlaylistResource.__isPlaylistOwner(userIdToRemove, playlistId):
        #     return False  # Don't remove the owner
        if not UserPlaylistResource.doesUserPlaylistExist(userIdToRemove, playlistId):
            return False  # User doesn't have access
        # if not UserPlaylistResource.doesUserPlaylistExist(elevatedUserId, playlistId):
        #     return False  # Elevated User doesn't have access

        sql = """
        DELETE u.*
        FROM UserPlaylist u
        where userId=%s and playlistId=%s
        """

        try:
            before = UserPlaylistResource.__get_count_from_db('PlaylistAccess.UserPlaylist')
            conn = UserPlaylistResource._get_connection('PlaylistAccess')
            cursor = conn.cursor()
            cursor.execute(sql, (userIdToRemove, playlistId))
            after = UserPlaylistResource.__get_count_from_db('PlaylistAccess.UserPlaylist')
            conn.commit()
            return after < before
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def createPlaylistForUser(userId, playlistId):
        """
        Creates a playlist for a user.

        :param userId: user ID to create for
        :param playlistId: playlist ID
        :return: True if successful, False otherwise
        """

        # If we already have a userId/playlistId combo there's nothing to do
        if UserPlaylistResource.doesUserPlaylistExist(userId, playlistId):
            return False

        # If the playlist exists then we can't create one
        if UserPlaylistResource.doesPlaylistExist(playlistId):
            return False

        sql = """
        insert into PlaylistAccess.UserPlaylist
        values (%s, %s, %s)
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            before = UserPlaylistResource.__get_count_from_db('PlaylistAccess.UserPlaylist')
            # cursor.execute(sql, (userId, playlistId, userId))
            cursor.execute(sql, (userId, playlistId, 'COFFEE'))
            after = UserPlaylistResource.__get_count_from_db('PlaylistAccess.UserPlaylist')
            conn.commit()
            ret = after > before
            return ret
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def info(userId=None):
        import pandas as pd
        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        sql = """
            select *
            from PlaylistAccess.UserPlaylist
            """

        if userId:
            sql += """
            where userId=%s
            """

        try:
            if userId:
                cursor.execute(sql, (userId,))
            else:
                cursor.execute(sql)
            r = cursor.fetchall()
            df = pd.DataFrame(r)
            ret = df.to_json()
            # cursor.close()
            return ret
        except:
            return ''

    @staticmethod
    def doesUserPlaylistExist(userId, playlistId):
        sql = """
        select count(*)
        from PlaylistAccess.UserPlaylist
        where userId=%s and playlistId=%s
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId, playlistId))
            count = get_count_from_cursor_execution(cursor)
            return count != 0
        except:
            return False

    
    @staticmethod
    def __get_count_from_db(db: str):
        """
        Get the number of items in a database table

        :param db: Database.Table name
        :return: number of items in the table
        """
        sql = f"""
        select count(*)
        from {db}
        """
    
        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            ret = get_count_from_cursor_execution(cursor)
        except:
            ret = None
        
        return ret

    @staticmethod
    def __isPlaylistOwner(userId, playlistId):
        """
        Determine if a user is the owner of a playlist

        :param userId: User ID to check
        :param playlistId:  Playlist ID to check
        :return: True if they are, False otherwise
        """
        sql = f"""
        select count(*)
        from PlaylistAccess.UserPlaylist
        where ownerId=%s and playlistId=%s
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId, playlistId))
            ret = get_count_from_cursor_execution(cursor)
            return ret != 0
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def __getOwner(playlistId):
        sql = """
        select ownerId
        from PlaylistAccess.UserPlaylist
        where playlistId=%s
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (playlistId, ))
            ret = cursor.fetchone()['ownerId']
            return ret
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def doesPlaylistExist(playlistId):
        sql = """
        select count(*)
        from PlaylistAccess.UserPlaylist
        where playlistId=%s
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (playlistId, ))
            count = get_count_from_cursor_execution(cursor)
            return count != 0
        except Exception as e:
            print(e)
            return False