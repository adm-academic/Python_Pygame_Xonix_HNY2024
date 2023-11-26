import pygame
import random
import os
import inspect
import sys

class Player():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        self.name = None
        self.score = 0
        self.registration_date = None
        self.last_name = self.settings.get_player_last_name()
        if self.in_db_alreay_exists(self.last_name):
            self.load_from_db(self.last_name)

    def load_from_db(self, name): # читает параметры в объект из БД по указанному имени
        query_get = " select * from Player where name='%s'; " % ( name )
        cursor = self.settings.db_connection.cursor()
        cursor.execute( query_get )
        rows = cursor.fetchall()
        if len(rows) <=0:
            return
        row = rows[0]
        self.name = row[1]
        self.score = row[2]
        self.registration_date = row[3]
        print("####", self.name )
        self.settings.set_player_last_name( self.name )

    def in_db_alreay_exists(self,name): # возвращает истину если игрок с таким именем уже есть в таблице БД
        query_check = " select * from Player where name='%s'; " % ( name )
        cursor = self.settings.db_connection.cursor()
        cursor.execute(query_check)
        rows = cursor.fetchall()
        return len(rows) > 0
    def save_to_db(self): # записывает текущий объект в БД
        if self.in_db_alreay_exists( self.name ):
            query_save = "update Player set score=%s, registration_date='%s' where name='%s' ;" % \
                         (self.score,self.registration_date,self.name)
        else:
            query_save = "insert into Player(name,score,registration_date) values ('%s',%s,'%s');" % \
                         (self.name,self.score,self.registration_date)
        cursor = self.settings.db_connection.cursor()
        cursor.execute(query_save)
        self.settings.db_connection.commit()

    def create_new_player(self,name):
        if self.in_db_alreay_exists(name):
            self.load_from_db(name)
            return
        query_create_new = "insert into Player(name,score,registration_date) " + \
                              "values ('%s',0,datetime('now','localtime')); " %name
        cursor = self.settings.db_connection.cursor()
        cursor.execute(query_create_new)
        self.settings.db_connection.commit()
        self.load_from_db(name)

