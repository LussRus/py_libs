import configparser
import sqlite3
import requests
import utils
import json
from flask import Flask, render_template, request, url_for, flash, redirect, json, jsonify

class STOCKS:
    def __init__(self):
        sprint = utils.DEBUG()

        ini = configparser.ConfigParser()
        ini.read('./config.ini')

        self.ini = ini['stocks']
        self.db_name = self.ini['db_file']
        self.finviz_temp_files = self.ini['finviz_temp_files']
        self.url = self.ini['url_to_tradernet_functions']
        connection = sqlite3.connect(self.db_name)

        with open(self.ini['schema']) as f:
            connection.executescript(f.read())
        connection.commit()
        connection.close()

        self.json_db = utils.JSON_DB(self.ini['watch_param_list'])

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def get_stock_list(self, conn=None):
        been_closed = False
        if conn is None:
            conn = conn = self.get_db_connection()
            been_closed = True
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM stock_list")

        rows = cur.fetchall()
        res_arr = []
        for item in rows:
            res_arr.append({k: item[k] for k in item.keys()})
        if been_closed:
            conn.close()
        return res_arr

    def update_stock_list(self):
     #   d = requests.post(self.url, data={'action':'us_list'} )
        dt = json.loads( requests.post(self.url, data={'action':'us_list'} ).text )

        conn = self.get_db_connection()
        rows = self.get_stock_list(conn)

        if len(rows):
            for row in rows:
                if row['ticker'] not in dt['data']:
                    print(f'New ticker: {row["ticker"]}')
                    t_info = self.get_share_info(row["ticker"])
                    self.insert_new_share(t_info)
                    print(f'Has been added')
        else:
            for ticker in dt['data']:
                answ = self.get_share_info(ticker)
                self.insert_new_share(answ, conn)
        conn.commit()
        conn.close()

    def get_share_info(self, ticker):
        dt = json.loads( requests.post(self.url, data={'action':'get_share_info', 'ticker':ticker}).text )
        return dt['data']

    def prepare_insert(self, table, row):
        cols = ', '.join('"{}"'.format(col) for col in row.keys())
        vals = ', '.join('"{}"'.format(val) for val in row.values())
        sql = 'INSERT INTO "{0}" ({1}) VALUES ({2});'.format(table, cols, vals)
        return sql

    def insert_new_share(self, share_info, conn = None):
        been_closed = False
        if conn is None:
            conn = conn = self.get_db_connection()
            been_closed = True
        cur = conn.cursor()
        sql = self.prepare_insert('stock_list', share_info)
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as err:
            print(f'INSERT ERROR:{err}')

        if been_closed:
            conn.close()

    def delete_all_from_table(self, table, conn = None):
        been_closed = False
        if conn is None:
            conn = conn = self.get_db_connection()
            been_closed = True
        cur = conn.cursor()

        cur.execute(f'DELETE FROM {table}')

        conn.commit()

        if been_closed:
            conn.close()

# INTERFACE to FLASK request PART
    def get_finviz_data(self, ticker = 'AAPL'):
        fn = f'{self.finviz_temp_files}{ticker}_details.json'
        arr = []
        try:
            with open(fn, 'r') as file:
                arr = json.load(file)
        except Exception as err:
            print(err)
        return arr
    
    def tables(self, ticker = 'AAPL'):
        arrs = self.get_finviz_data(ticker)
        diff = arrs['diff']
        new_a = arrs['new']
        old_a = arrs['old']
        marked_flds = []
        for e in self.json_db.list():
            marked_flds.append(e['name'])
        arr = []
        for k in diff:
            arr.append( [k, diff[k], new_a[k], old_a[k] ])
        return render_template('stocks.html', ticker=ticker, arr=arr, marked_flds=marked_flds) # .items(), arr['new'].items(), arr['old'].items()] )

    # Формируем список контролируемых показателей
    def td_sel(self, req):
        act = req.args.get('action')
        if act is None:
            return jsonify(answer='false')
        cell_text = request.args.get('cell_text')
        if cell_text is None:
            return jsonify(answer='false')
        else:
            if act == 'mark':
                self.json_db.put({'name':cell_text})
            if act == 'unmark':
                self.json_db.delete('name',cell_text)
        return jsonify(answer=act, cell_text = cell_text)

    def stock_all_calls(self, r):
        ajax = '_ajax' in r.form
        return jsonify({'answer':'too_bad'})
