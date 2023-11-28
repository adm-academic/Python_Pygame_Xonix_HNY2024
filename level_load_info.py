import pygame
import random
import os
import inspect
import sys

class Level_Load_Info():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        pass
    def read_level_with_number_from_db(self, level_number):
        query_next_level = """
                            SELECT *
                            FROM  Possible_Level pl
                            where pl.id =%s
                            """ % level_number
        cursor = self.settings.db_connection.cursor()  # получим курсор БД
        cursor.execute(query_next_level)  # выполним курсор с запросом
        rows = cursor.fetchall()  # получим все строки результата
        cursor.close()
        self.settings.db_connection.commit()
        # -----
        row = rows[0]
        self.level_id = row[0]
        self.enemies_count = row[1]
        self.enemies_delay = row[2]
        self.image_filename = row[3]
        self.score = 200
        query_playing_level = """   select  p.id player_id, p.name name,
                                            cl.score score, 
                                            pl.id level_id, pl.backround_image image
                                    from    Player p inner join  
                                            Completed_Level cl on p.id = cl.player_id inner join
                                            Possible_Level pl ON cl.possible_level_id = pl.id 
                                    WHERE   p.id  = %s and
        	                                pl.id = %s 
                             """ % ( self.game.player.id, self.level_id )
        cursor = self.settings.db_connection.cursor()  # получим курсор БД
        cursor.execute( query_playing_level )  # выполним курсор с запросом
        rows = cursor.fetchall()  # получим все строки результата
        cursor.close()
        self.settings.db_connection.commit()
        if len(rows)<=0:
            self.old_score = 0
        elif len(rows)==1:
            self.old_score = rows[0][2]
        else:
            self.old_score = 0

    def player_win_in_level_write_to_db(self,level_number,score):
        already_win_level = """
                            SELECT *
                            FROM Completed_Level cl 
                            WHERE cl.player_id = %s
                                  and possible_level_id = %s;
                            """ % ( self.game.player.id, level_number )
        cursor = self.settings.db_connection.cursor()  # получим курсор БД
        cursor.execute(already_win_level)  # выполним курсор с запросом
        rows = cursor.fetchall()  # получим все строки результата
        cursor.close()
        self.settings.db_connection.commit()
        if len(rows)<= 0: # сделаем INSERT в БД. игрок первый раз прошёл уровень!
            insert_win_level =  """
                                INSERT INTO Completed_Level (player_id,possible_level_id,score,pl_datetime)
                                VALUES (%s,%s,%s,%s);
                                """ % (self.game.player.id,level_number,0,"datetime('now','localtime')")
            cursor = self.settings.db_connection.cursor()  # получим курсор БД
            cursor.execute(insert_win_level)  # выполним курсор с запросом
            self.settings.db_connection.commit()
            cursor.close()
            pass
        else: # игрок уже проходил этот уровень, сделаем UPDATE !
            update_win_level =  """
                                UPDATE Completed_Level 
                                SET pl_datetime=datetime('now','localtime'),
                                    score=%s
                                WHERE player_id = %s
                                      and possible_level_id = %s;
                                """ % ( score, self.game.player.id, level_number )
            cursor = self.settings.db_connection.cursor()  # получим курсор БД
            cursor.execute(update_win_level)  # выполним курсор с запросом
            cursor.close()
            self.settings.db_connection.commit()
            update_player_score = ( """
                                    UPDATE Player as tp
                                    set score = 
                                    (
                                    select  sum( cl.score )
                                    from    Player p inner join  
                                            Completed_Level cl on p.id = cl.player_id inner join
                                            Possible_Level pl ON cl.possible_level_id = pl.id 
                                    WHERE   p.id  = %s
                                    )
                                    WHERE tp.id = %s
                                   """
                               ) % ( self.game.player.id, self.game.player.id )
            cursor = self.settings.db_connection.cursor()  # получим курсор БД
            cursor.execute(update_player_score)  # выполним курсор с запросом
            cursor.close()
            self.settings.db_connection.commit()

    def player_reached_finish(self):
        query_player_last_level =   """
                                    select  p.id player_id, p.name name,
                                            cl.score score, 
                                            pl.id level_id, pl.backround_image image
                                    from    Player p inner join  
                                            Completed_Level cl on p.id = cl.player_id inner join
                                            Possible_Level pl ON cl.possible_level_id = pl.id 
                                    WHERE   p.id  = %s and
                                            pl.id =16
                                    """ % self.game.player.id
        cursor = self.settings.db_connection.cursor()  # получим курсор БД
        cursor.execute(query_player_last_level)  # выполним курсор с запросом
        rows = cursor.fetchall()  # получим все строки результата
        cursor.close()
        if len(rows) <=0:
            return False
        elif len(rows)==1:
            return True
