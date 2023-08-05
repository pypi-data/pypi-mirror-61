"""
The MIT License (MIT)

Copyright (c) 2014-2019 William Ivanski
Copyright (c) 2018-2019 Israel Barth Rubio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
import decimal
import json
import math
import uuid
import sqlparse
import select
from collections import OrderedDict
from abc import ABC, abstractmethod
from tabulate import tabulate
from urllib.parse import urlparse

import Spartacus

v_supported_rdbms = []
try:
    import sqlite3

    v_supported_rdbms.append("SQLite")
    v_supported_rdbms.append("Memory")
except ImportError:
    pass
try:
    import psycopg2
    import psycopg2.extras
    import psycopg2.extensions
    from pgspecial.main import PGSpecial
    from pgspecial.namedqueries import NamedQueries
    from pgspecial.help.commands import helpcommands as HelpCommands

    v_supported_rdbms.append("PostgreSQL")
except ImportError:
    pass
try:
    import pymysql

    v_supported_rdbms.append("MySQL")
    v_supported_rdbms.append("MariaDB")
except ImportError:
    pass
try:
    import fdb

    v_supported_rdbms.append("Firebird")
except ImportError:
    pass
try:
    import cx_Oracle

    v_supported_rdbms.append("Oracle")
except ImportError:
    pass
try:
    import pymssql

    v_supported_rdbms.append("MSSQL")
except ImportError:
    pass
try:
    import ibm_db
    import ibm_db_dbi

    v_supported_rdbms.append("IBMDB2")
except ImportError:
    pass


class Exception(Exception):
    pass


class DataTable(object):
    def __init__(self, p_name=None, p_alltypesstr=False, p_simple=False):
        self.Name = p_name
        self.Columns = []
        self.Rows = []
        self.AllTypesStr = p_alltypesstr
        self.Simple = p_simple

    def AddColumn(self, p_columnname):
        self.Columns.append(p_columnname)

    def AddRow(self, p_row):
        if len(self.Columns) > 0 and len(p_row) > 0:
            if len(self.Columns) == len(p_row):
                if not isinstance(p_row, OrderedDict):
                    v_rowtmp2 = p_row
                    if self.AllTypesStr:
                        for j in range(0, len(v_rowtmp2)):
                            if v_rowtmp2[j] != None:
                                v_rowtmp2[j] = str(v_rowtmp2[j])
                            else:
                                v_rowtmp2[j] = ""
                    v_rowtmp = OrderedDict(zip(self.Columns, tuple(v_rowtmp2)))
                    if self.Simple:
                        v_row = []
                        for c in self.Columns:
                            v_row.append(v_rowtmp[c])
                    else:
                        v_row = v_rowtmp
                else:
                    v_row = p_row
                self.Rows.append(v_row)
            else:
                raise Spartacus.Database.Exception(
                    "Can not add row to a table with different columns."
                )
        else:
            raise Spartacus.Database.Exception(
                "Can not add row to a table with no columns."
            )

    def Select(self, p_key, p_value):
        if isinstance(p_key, list):
            v_key = p_key
        else:
            v_key = [p_key]
        if isinstance(p_value, list):
            v_value = p_value
        else:
            v_value = [p_value]
        if len(v_key) == len(v_value):
            try:
                v_table = Spartacus.Database.DataTable(
                    None, p_alltypesstr=self.AllTypesStr, p_simple=self.Simple
                )
                for c in self.Columns:
                    v_table.AddColumn(c)
                if self.Simple:
                    v_keytmp = v_key
                    v_key = []
                    for x in v_keytmp:
                        k = 0
                        found = False
                        while not found and k < len(self.Columns):
                            if self.Columns[k] == x:
                                found = True
                                v_key.append(k)
                            else:
                                k = k + 1
                for r in self.Rows:
                    v_match = True
                    for k in range(len(v_key)):
                        if not self.Equal(r[v_key[k]], v_value[k]):
                            v_match = False
                    if v_match:
                        v_table.Rows.append(r)
                return v_table
            except Exception as exc:
                raise Spartacus.Database.Exception(str(exc))
        else:
            raise Spartacus.Database.Exception(
                "Can not select with different key-value dimension."
            )

    def Merge(self, p_datatable):
        if len(self.Columns) > 0 and len(p_datatable.Columns) > 0:
            if self.Columns == p_datatable.Columns:
                for r in p_datatable.Rows:
                    self.Rows.append(r)
            else:
                raise Spartacus.Database.Exception(
                    "Can not merge tables with different columns."
                )
        else:
            raise Spartacus.Database.Exception("Can not merge tables with no columns.")

    def Equal(self, p_val1, p_val2):
        if type(p_val1) is float:
            v_val1 = decimal.Decimal(repr(p_val1))
        else:
            v_val1 = p_val1
        if type(p_val2) is float:
            v_val2 = decimal.Decimal(repr(p_val2))
        else:
            v_val2 = p_val2
        if v_val1 is None and v_val2 == "":
            v_val1 = ""
        elif v_val1 == "" and v_val2 is None:
            v_val2 = ""
        return v_val1 == v_val2

    def Compare(
        self,
        p_datatable,
        p_pkcols,
        p_statuscolname,
        p_diffcolname,
        p_ordered=False,
        p_keepequal=False,
        p_debugupdates=False,
    ):
        if len(self.Columns) > 0 and len(p_datatable.Columns) > 0:
            if self.Columns == p_datatable.Columns:
                v_table = DataTable()
                for c in self.Columns:
                    v_table.AddColumn(c)
                v_table.AddColumn(p_statuscolname)
                v_table.AddColumn(p_diffcolname)
                v_pkcols = []
                if len(p_pkcols) > 0:
                    for c in p_pkcols:
                        v_pkcols.append(c)
                else:
                    for c in self.Columns:
                        v_pkcols.append(c)
                if p_ordered:
                    k1 = 0
                    k2 = 0
                    while k1 < len(self.Rows) and k2 < len(p_datatable.Rows):
                        r1 = self.Rows[k1]
                        r2 = p_datatable.Rows[k2]
                        pklist1 = []
                        pklist2 = []
                        for pkcol in v_pkcols:
                            pklist1.append(str(r1[pkcol]))
                            pklist2.append(str(r2[pkcol]))
                        pk1 = "_".join(pklist1)
                        pk2 = "_".join(pklist2)
                        if pk1 == pk2:
                            v_allmatch = True
                            v_row = []
                            v_diff = []
                            for c in self.Columns:
                                if not self.Equal(r1[c], r2[c]):
                                    if p_debugupdates:
                                        v_row.append(
                                            "[{0}]({1}) --> [{2}]({3})".format(
                                                repr(r1[c]),
                                                type(r1[c]),
                                                repr(r2[c]),
                                                type(r2[c]),
                                            )
                                        )
                                    else:
                                        v_row.append(
                                            "{0} --> {1}".format(
                                                repr(r1[c]), repr(r2[c])
                                            )
                                        )
                                    v_diff.append(c)
                                    v_allmatch = False
                                else:
                                    v_row.append(r1[c])
                            if v_allmatch:
                                v_row.append("E")
                                v_row.append("")
                                if p_keepequal:
                                    v_table.AddRow(v_row)
                            else:
                                v_row.append("U")
                                v_row.append(",".join(v_diff))
                                v_table.AddRow(v_row)
                            k1 = k1 + 1
                            k2 = k2 + 1
                        elif pk1 < pk2:
                            v_row = []
                            for c in self.Columns:
                                v_row.append(r1[c])
                            v_row.append("D")
                            v_row.append("")
                            v_table.AddRow(v_row)
                            k1 = k1 + 1
                        else:
                            v_row = []
                            for c in p_datatable.Columns:
                                v_row.append(r2[c])
                            v_row.append("I")
                            v_row.append("")
                            v_table.AddRow(v_row)
                            k2 = k2 + 1
                    while k1 < len(self.Rows):
                        r1 = self.Rows[k1]
                        v_row = []
                        for c in self.Columns:
                            v_row.append(r1[c])
                        v_row.append("D")
                        v_row.append("")
                        v_table.AddRow(v_row)
                        k1 = k1 + 1
                    while k2 < len(p_datatable.Rows):
                        r2 = p_datatable.Rows[k2]
                        v_row = []
                        for c in p_datatable.Columns:
                            v_row.append(r2[c])
                        v_row.append("I")
                        v_row.append("")
                        v_table.AddRow(v_row)
                        k2 = k2 + 1
                else:
                    for r1 in self.Rows:
                        v_pkmatch = False
                        for r2 in p_datatable.Rows:
                            v_pkmatch = True
                            for pkcol in v_pkcols:
                                if not self.Equal(r1[pkcol], r2[pkcol]):
                                    v_pkmatch = False
                                    break
                            if v_pkmatch:
                                break
                        if v_pkmatch:
                            v_allmatch = True
                            v_row = []
                            v_diff = []
                            for c in self.Columns:
                                if not self.Equal(r1[c], r2[c]):
                                    v_row.append("{0} --> {1}".format(r1[c], r2[c]))
                                    v_diff.append(c)
                                    v_allmatch = False
                                else:
                                    v_row.append(r1[c])
                            if v_allmatch:
                                v_row.append("E")
                                v_row.append("")
                                if p_keepequal:
                                    v_table.AddRow(v_row)
                            else:
                                v_row.append("U")
                                v_row.append(",".join(v_diff))
                                v_table.AddRow(v_row)
                        else:
                            v_row = []
                            for c in self.Columns:
                                v_row.append(r1[c])
                            v_row.append("D")
                            v_row.append("")
                            v_table.AddRow(v_row)
                    for r2 in p_datatable.Rows:
                        v_pkmatch = False
                        for r1 in self.Rows:
                            v_pkmatch = True
                            for pkcol in v_pkcols:
                                if not self.Equal(r1[pkcol], r2[pkcol]):
                                    v_pkmatch = False
                                    break
                            if v_pkmatch:
                                break
                        if not v_pkmatch:
                            v_row = []
                            for c in p_datatable.Columns:
                                v_row.append(r2[c])
                            v_row.append("I")
                            v_row.append("")
                            v_table.AddRow(v_row)
                return v_table
            else:
                raise Spartacus.Database.Exception(
                    "Can not compare tables with different columns."
                )
        else:
            raise Spartacus.Database.Exception(
                "Can not compare tables with no columns."
            )

    def Jsonify(self):
        if self.Simple:
            if len(self.Rows) > 0:
                if isinstance(self.Rows[0], OrderedDict):
                    return json.dumps(self.Rows)
                else:
                    v_table = []
                    for r in self.Rows:
                        v_row = []
                        for c in range(0, len(self.Columns)):
                            v_row.append(r[c])
                        v_table.append(OrderedDict(zip(self.Columns, tuple(v_row))))
                    return json.dumps(v_table)
            else:
                return json.dumps(self.Rows)
        else:
            if len(self.Rows) > 0:
                if isinstance(self.Rows[0], OrderedDict):
                    return json.dumps(self.Rows)
                else:
                    v_table = []
                    for r in self.Rows:
                        v_row = []
                        for c in self.Columns:
                            v_row.append(r[c])
                        v_table.append(OrderedDict(zip(self.Columns, tuple(v_row))))
                    return json.dumps(v_table)
            else:
                return json.dumps(self.Rows)

    def Pretty(self, p_transpose=False):
        if self.Simple:
            if p_transpose:
                v_maxc = 0
                for c in self.Columns:
                    if len(c) > v_maxc:
                        v_maxc = len(c)
                if v_maxc < (14 + len(str(len(self.Rows)))):
                    v_maxc = 14 + len(str(len(self.Rows)))
                else:
                    v_maxc = v_maxc + 1
                k = 0
                s = 0
                v_maxf = 0
                for r in self.Rows:
                    for c in range(0, len(self.Columns)):
                        for v_snippet in str(r[c]).split("\n"):
                            k = k + 1
                            s = s + len(v_snippet)
                            if len(str(r[c])) > v_maxf:
                                v_maxf = len(v_snippet)
                if v_maxf > 30:
                    v_maxf = int(s / k) + int((v_maxf - int(s / k)) / 2)
                v_maxf = v_maxf + 10
                v_string = ""
                v_row = 1
                for r in self.Rows:
                    v_aux = "-[ RECORD {0} ]".format(v_row)
                    for k in range(len(v_aux), v_maxc):
                        v_aux = v_aux + "-"
                    v_string = v_string + v_aux + "+"
                    for k in range(0, v_maxf):
                        v_string = v_string + "-"
                    v_string = v_string + "\n"
                    for c in range(0, len(self.Columns)):
                        v_first = True
                        for v_snippet in str(r[c]).split("\n"):
                            n = math.ceil(len(v_snippet) / (v_maxf - 2))
                            j = 0
                            for i in range(0, n):
                                if v_first:
                                    x = c.ljust(v_maxc)
                                    v_first = False
                                else:
                                    x = " ".ljust(v_maxc)
                                if i < n - 1:
                                    y = " " + v_snippet[j : j + v_maxf - 2] + "+"
                                    j = j + v_maxf - 2
                                else:
                                    y = " " + v_snippet[j:]
                                v_string = v_string + "{0}|{1}\n".format(x, y)
                    v_row = v_row + 1
                return v_string
            else:
                v_rows = []
                for r in self.Rows:
                    v_row = []
                    for c in range(0, len(self.Columns)):
                        v_row.append(r[c])
                    v_rows.append(v_row)
                return tabulate(v_rows, self.Columns, tablefmt="psql")

        else:
            if p_transpose:
                v_maxc = 0
                for c in self.Columns:
                    if len(c) > v_maxc:
                        v_maxc = len(c)
                if v_maxc < (14 + len(str(len(self.Rows)))):
                    v_maxc = 14 + len(str(len(self.Rows)))
                else:
                    v_maxc = v_maxc + 1
                k = 0
                s = 0
                v_maxf = 0
                for r in self.Rows:
                    for c in self.Columns:
                        for v_snippet in str(r[c]).split("\n"):
                            k = k + 1
                            s = s + len(v_snippet)
                            if len(str(r[c])) > v_maxf:
                                v_maxf = len(v_snippet)
                if v_maxf > 30:
                    v_maxf = int(s / k) + int((v_maxf - int(s / k)) / 2)
                v_maxf = v_maxf + 10
                v_string = ""
                v_row = 1
                for r in self.Rows:
                    v_aux = "-[ RECORD {0} ]".format(v_row)
                    for k in range(len(v_aux), v_maxc):
                        v_aux = v_aux + "-"
                    v_string = v_string + v_aux + "+"
                    for k in range(0, v_maxf):
                        v_string = v_string + "-"
                    v_string = v_string + "\n"
                    for c in self.Columns:
                        v_first = True
                        for v_snippet in str(r[c]).split("\n"):
                            n = math.ceil(len(v_snippet) / (v_maxf - 2))
                            j = 0
                            for i in range(0, n):
                                if v_first:
                                    x = c.ljust(v_maxc)
                                    v_first = False
                                else:
                                    x = " ".ljust(v_maxc)
                                if i < n - 1:
                                    y = " " + v_snippet[j : j + v_maxf - 2] + "+"
                                    j = j + v_maxf - 2
                                else:
                                    y = " " + v_snippet[j:]
                                v_string = v_string + "{0}|{1}\n".format(x, y)
                    v_row = v_row + 1
                return v_string
            else:
                v_rows = []
                for r in self.Rows:
                    v_row = []
                    for c in self.Columns:
                        v_row.append(r[c])
                    v_rows.append(v_row)
                return tabulate(v_rows, self.Columns, tablefmt="psql")

    def Transpose(self, p_column1, p_column2):
        if len(self.Rows) == 1:
            v_table = Spartacus.Database.DataTable()
            v_table.AddColumn(p_column1)
            v_table.AddColumn(p_column2)
            if self.Simple:
                for k in range(len(self.Columns)):
                    v_table.AddRow([self.Columns[k], self.Rows[0][k]])
            else:
                for c in self.Columns:
                    v_table.AddRow([c, self.Rows[0][c]])
            return v_table
        else:
            raise Spartacus.Database.Exception(
                "Can only transpose a table with a single row."
            )

    def Distinct(self, p_pkcols):
        v_table = Spartacus.Database.DataTable(
            None, p_alltypesstr=self.AllTypesStr, p_simple=self.Simple
        )
        for c in self.Columns:
            v_table.AddColumn(c)
        a = 0
        for r in self.Rows:
            v_value = []
            if self.Simple:
                for x in p_pkcols:
                    k = 0
                    found = False
                    while not found and k < len(self.Columns):
                        if self.Columns[k] == x:
                            found = True
                            v_value.append(r[k])
                        else:
                            k = k + 1
            else:
                for x in p_pkcols:
                    v_value.append(r[x])
            v_tmp = v_table.Select(p_pkcols, v_value)
            if len(v_tmp.Rows) == 0:
                v_table.AddRow(r)
            a = a + 1
        return v_table


class DataField(object):
    def __init__(self, p_name, p_type=None, p_dbtype=None, p_mask="#"):
        self.v_name = p_name
        self.v_truename = p_name
        self.v_type = p_type
        self.v_dbtype = p_dbtype
        self.v_mask = p_mask


class DataTransferReturn(object):
    def __init__(self):
        self.v_numrecords = 0
        self.v_log = None
        self.v_hasmorerecords = True


class DataList(object):
    def __init__(self):
        self.v_list = []

    def append(self, p_item):
        self.v_list.append(p_item)


"""
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
"""


class Generic(ABC):
    @abstractmethod
    def GetConnectionString(self):
        pass

    @abstractmethod
    def Open(self, p_autocommit=True):
        pass

    @abstractmethod
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        pass

    @abstractmethod
    def Execute(self, p_sql):
        pass

    @abstractmethod
    def ExecuteScalar(self, p_sql):
        pass

    @abstractmethod
    def Close(self, p_commit=True):
        pass

    @abstractmethod
    def Commit(self):
        pass

    @abstractmethod
    def Rollback(self):
        pass

    @abstractmethod
    def Cancel(self, p_usesameconn=True):
        pass

    @abstractmethod
    def GetPID(self):
        pass

    @abstractmethod
    def Terminate(self, p_pid):
        pass

    @abstractmethod
    def GetFields(self, p_sql):
        pass

    @abstractmethod
    def GetNotices(self):
        pass

    @abstractmethod
    def ClearNotices(self):
        pass

    @abstractmethod
    def GetStatus(self):
        pass

    @abstractmethod
    def GetConStatus(self):
        pass

    @abstractmethod
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        pass

    @abstractmethod
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        pass

    @abstractmethod
    def Special(self, p_sql):
        pass

    def String(self, p_value):
        if type(p_value) == type(list()):
            ret = self.MogrifyArray(p_value)
        else:
            ret = str(p_value)
        return ret

    def MogrifyValue(self, p_value):
        if type(p_value) == type(list()):
            ret = self.MogrifyArray(p_value)
        elif type(p_value) == type(None):
            ret = "null"
        elif type(p_value) == type(str()):
            ret = "'{0}'".format(p_value.replace("'", "''"))
        elif type(p_value) == datetime.datetime:
            ret = "'{0}'".format(p_value)
        else:
            ret = "{0}".format(p_value)
        return ret

    def MogrifyArray(self, p_array):
        ret = "{"
        if len(p_array) > 0:
            ret = ret + self.MogrifyArrayValue(p_array[0])
            for i in range(1, len(p_array)):
                ret = ret + ", " + self.MogrifyArrayValue(p_array[i])
        ret = ret + "}"
        return ret

    def MogrifyArrayValue(self, p_value):
        if type(p_value) == type(list()):
            ret = self.MogrifyArray(p_value)
        elif type(p_value) == type(None):
            ret = "null"
        elif type(p_value) == type(str()):
            ret = '"{0}"'.format(p_value.replace('"', '""'))
        elif type(p_value) == datetime.datetime:
            ret = '"{0}"'.format(p_value)
        else:
            ret = "{0}".format(p_value)
        return ret

    def Mogrify(self, p_row, p_fields):
        if len(p_row) == len(p_fields):
            v_mog = []
            for k in range(0, len(p_row)):
                v_mog.append(
                    p_fields[k].v_mask.replace(
                        "#", self.MogrifyValue(p_row[p_fields[k].v_name])
                    )
                )
            return "(" + ",".join(v_mog) + ")"
        else:
            raise Spartacus.Database.Exception(
                "Can not mogrify with different number of parameters."
            )

    def Transfer(
        self,
        p_sql=None,
        p_table=None,
        p_targetdatabase=None,
        p_tablename=None,
        p_blocksize=1000,
        p_fields=None,
        p_alltypesstr=False,
    ):
        """Method used to transfer data from one database to another one.

            Args:
                p_sql (str): the sql query to be executed in the current database, in order to provide data to be inserted into target database. Defaults to None.
                p_table (Spartacus.Database.DataTable): the data table containing data to be inserted into target database. Defaults to None.
                p_targetdatabase (Spartacus.Database.Generic): any object that inherits from Spartacus.Database.Generic. It is the target database connection. Defaults to None.
                p_tablename (str): the target table name. Defaults to None.
                p_blocksize (int): number of rows to be read at a time from source database. Defaults to 1000.
                p_fields (list): list of fields to be considered while inserting into target database table. Defaults to None.
                p_alltypesstr (bool): if all fields should be queried as str instances.

            Notes:
                Either p_sql or p_table must be provided. If p_sql is provided, a query will be executed in source database. Otherwise, will use p_table data.
                p_tablename may also contain schema name, if target database supports it, e.g., 'my_schema.my_table'.
                p_blocksize and p_alltypesstr are used just in case of p_sql being used too.
                If p_fields is None, will consider all target table columns while transfering data.

            Returns:
                Spartacus.Database.DataTransferReturn.

            Raises:
                Spartacus.Database.Exception.
        """

        if p_sql is None and p_table is None:
            raise Spartacus.Database.Exception(
                "Either p_sql or p_table parameter must be provided."
            )
        v_return = DataTransferReturn()
        try:
            v_table = (
                self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
                if p_sql is not None
                else p_table
            )
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
            v_return.v_hasmorerecords = not self.v_start
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return

    def GetIdentifiersDML(p_sql):
        try:
            v_dict = {"all": [], "readonly": [], "writeonly": [], "readwrite": []}
            v_statement = sqlparse.split(p_sql)
            v_analysis = sqlparse.parse(p_sql)
            if len(v_statement) == len(v_analysis):
                for i in range(0, len(v_statement)):
                    v_type = v_analysis[i].get_type()
                    v_next_is_into = False
                    v_next_is_from = False
                    v_next_is_read_table = False
                    v_next_is_write_table = False
                    for v_token in v_analysis[i].flatten():
                        if v_token.ttype != sqlparse.tokens.Token.Text.Whitespace:
                            if v_next_is_into:
                                v_next_is_write_table = True
                                v_next_is_into = False
                            elif v_next_is_from:
                                v_next_is_write_table = True
                                v_next_is_from = False
                            elif v_next_is_read_table:
                                v_dict["readonly"].append(v_token.value)
                                v_next_is_read_table = False
                            elif v_next_is_write_table:
                                v_dict["writeonly"].append(v_token.value)
                                v_next_is_write_table = False
                            elif v_token.is_keyword and v_token.value.lower() in [
                                "from",
                                "join",
                                "inner join",
                                "left join",
                                "left outer join",
                                "right join",
                                "right outer join",
                                "full join",
                                "full outer join",
                                "cross join",
                                "natural join",
                            ]:
                                v_next_is_read_table = True
                            elif (
                                v_token.is_keyword and v_token.value.lower() == "insert"
                            ):
                                v_next_is_into = True
                            elif (
                                v_token.is_keyword and v_token.value.lower() == "delete"
                            ):
                                v_next_is_from = True
                            elif (
                                v_token.is_keyword and v_token.value.lower() == "update"
                            ):
                                v_next_is_write_table = True
                            elif (
                                v_token.is_keyword
                                and v_token.value.lower() == "truncate"
                            ):
                                v_next_is_write_table = True
            v_dict["readonly"] = list(dict.fromkeys(v_dict["readonly"]))
            v_dict["writeonly"] = list(dict.fromkeys(v_dict["writeonly"]))
            v_dict["readwrite"] = list(
                dict.fromkeys(
                    [
                        value
                        for value in v_dict["readonly"]
                        if value in v_dict["writeonly"]
                    ]
                    + [
                        value
                        for value in v_dict["writeonly"]
                        if value in v_dict["readonly"]
                    ]
                )
            )
            for value in v_dict["readwrite"]:
                v_dict["readonly"].remove(value)
                v_dict["writeonly"].remove(value)
            v_dict["all"] = list(
                dict.fromkeys(
                    v_dict["readonly"] + v_dict["writeonly"] + v_dict["readwrite"]
                )
            )
            for k in list(v_dict.keys()):
                v_dict[k].sort()
            return v_dict
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetIdentifiersDDL(p_sql):
        try:
            v_dict = {"all": [], "create": [], "alter": [], "drop": []}
            v_statement = sqlparse.split(p_sql)
            v_analysis = sqlparse.parse(p_sql)
            if len(v_statement) == len(v_analysis):
                for i in range(0, len(v_statement)):
                    v_type = v_analysis[i].get_type()
                    v_class = None
                    v_next_is_class = False
                    v_next_is_object = False
                    if v_type in ["CREATE", "CREATE OR REPLACE", "ALTER", "DROP"]:
                        for v_token in v_analysis[i].flatten():
                            if v_token.ttype != sqlparse.tokens.Token.Text.Whitespace:
                                if (
                                    v_token.is_keyword
                                    and v_token.value.upper() == v_type
                                ):
                                    v_next_is_class = True
                                elif v_next_is_class:
                                    v_class = v_token.value.lower()
                                    v_next_is_class = False
                                    v_next_is_object = True
                                elif v_next_is_object:
                                    if v_type == "CREATE OR REPLACE":
                                        v_dict["create"].append(
                                            (v_class, v_token.value)
                                        )
                                    else:
                                        v_dict[v_type.lower()].append(
                                            (v_class, v_token.value)
                                        )
                                    if v_class in v_dict:
                                        v_dict[v_class].append(v_token.value)
                                    else:
                                        v_dict[v_class] = [v_token.value]
                                    v_next_is_object = False
            v_dict["create"] = list(dict.fromkeys(v_dict["create"]))
            v_dict["alter"] = list(dict.fromkeys(v_dict["alter"]))
            v_dict["drop"] = list(dict.fromkeys(v_dict["drop"]))
            v_dict["all"] = list(
                dict.fromkeys(v_dict["create"] + v_dict["alter"] + v_dict["drop"])
            )
            for k in list(v_dict.keys()):
                v_dict[k].sort()
            return v_dict
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))


"""
------------------------------------------------------------------------
SQLite
------------------------------------------------------------------------
"""


class SQLite(Generic):
    def __init__(self, p_service, p_foreignkeys=True, p_timeout=30, p_encoding=None):
        if "SQLite" in v_supported_rdbms:
            self.v_host = None
            self.v_port = None
            self.v_service = p_service
            self.v_user = None
            self.v_password = None
            self.v_con = None
            self.v_cur = None
            self.v_foreignkeys = p_foreignkeys
            self.v_timeout = p_timeout
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "SQLite is not supported. Please install it."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            if p_autocommit:
                self.v_con = sqlite3.connect(
                    self.v_service,
                    self.v_timeout,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    isolation_level=None,
                )
            else:
                self.v_con = sqlite3.connect(
                    self.v_service,
                    self.v_timeout,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    isolation_level="DEFERRED",
                )
            self.v_cur = self.v_con.cursor()
            if self.v_foreignkeys:
                self.v_cur.execute("PRAGMA foreign_keys = ON")
            self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        pass

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute("select * from ( " + p_sql + " ) t limit 1")
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k]))
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=type(None))
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        return None

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = "begin; "
            for r in p_block.Rows:
                v_insert = (
                    v_insert
                    + "insert into "
                    + p_tablename
                    + "("
                    + ",".join(v_columnames)
                    + ") values "
                    + self.Mogrify(r, v_fields)
                    + "; "
                )
            v_insert = v_insert + "commit;"
            self.v_cur.executescript(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()


"""
------------------------------------------------------------------------
Memory
------------------------------------------------------------------------
"""


class Memory(Generic):
    def __init__(self, p_foreignkeys=True, p_timeout=30, p_encoding=None):
        if "Memory" in v_supported_rdbms:
            self.v_host = None
            self.v_port = None
            self.v_service = ":memory:"
            self.v_user = None
            self.v_password = None
            self.v_con = None
            self.v_cur = None
            self.v_foreignkeys = p_foreignkeys
            self.v_timeout = p_timeout
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "SQLite is not supported. Please install it."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            if p_autocommit:
                self.v_con = sqlite3.connect(
                    self.v_service,
                    self.v_timeout,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    isolation_level=None,
                )
            else:
                self.v_con = sqlite3.connect(
                    self.v_service,
                    self.v_timeout,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                    isolation_level="DEFERRED",
                )
            self.v_cur = self.v_con.cursor()
            if self.v_foreignkeys:
                self.v_cur.execute("PRAGMA foreign_keys = ON")
            self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    while v_row is not None:
                        v_table.AddRow(list(v_row))
                        v_row = self.v_cur.fetchone()
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Execute(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def ExecuteScalar(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                if r != None:
                    s = r[0]
                else:
                    s = None
                return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        self.Close(True)

    def Rollback(self):
        self.Close(False)

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        pass

    def GetFields(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                v_fields = []
                self.v_cur.execute("select * from ( " + p_sql + " ) t limit 1")
                r = self.v_cur.fetchone()
                if r != None:
                    k = 0
                    for c in self.v_cur.description:
                        v_fields.append(
                            DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k]))
                        )
                        k = k + 1
                else:
                    k = 0
                    for c in self.v_cur.description:
                        v_fields.append(
                            DataField(c[0], p_type=type(None), p_dbtype=type(None))
                        )
                        k = k + 1
                return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        return None

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = "begin; "
            for r in p_block.Rows:
                v_insert = (
                    v_insert
                    + "insert into "
                    + p_tablename
                    + "("
                    + ",".join(v_columnames)
                    + ") values "
                    + self.Mogrify(r, v_fields)
                    + "; "
                )
            v_insert = v_insert + "commit;"
            self.v_cur.executescript(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()


"""
------------------------------------------------------------------------
PostgreSQL
------------------------------------------------------------------------
"""


class PostgreSQL(Generic):
    def __init__(
        self,
        p_host=None,
        p_port=None,
        p_service=None,
        p_user=None,
        p_password=None,
        p_application_name="spartacus",
        p_dsn="",
        p_conn_string="",
        p_encoding=None,
    ):
        if "PostgreSQL" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 5432
            else:
                self.v_port = p_port
            if p_service is None or p_service == "":
                self.v_service = "postgres"
            else:
                self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_application_name = p_application_name
            self.v_dsn = p_dsn
            self.v_conn_string = p_conn_string
            self.v_conn_string_parsed = urlparse(p_conn_string)
            self.v_con = None
            self.v_cur = None
            self.v_start = True
            self.v_cursor = None
            self.v_autocommit = True
            self.v_last_fetched_size = 0
            self.v_special = PGSpecial()
            self.v_help = Spartacus.Database.DataTable()
            self.v_help.Columns = ["Command", "Syntax", "Description"]
            self.v_help.AddRow(["\\?", "\\?", "Show Commands."])
            self.v_help.AddRow(["\\h", "\\h [pattern]", "Show SQL syntax and help."])
            self.v_help.AddRow(["\\list", "\\list", "List databases."])
            self.v_help.AddRow(["\\l", "\\l[+] [pattern]", "List databases."])
            self.v_help.AddRow(["\\du", "\\du[+] [pattern]", "List roles."])
            self.v_help.AddRow(["\\dx", "\\dx[+] [pattern]", "List extensions."])
            self.v_help.AddRow(["\\db", "\\db[+] [pattern]", "List tablespaces."])
            self.v_help.AddRow(["\\dn", "\\dn[+] [pattern]", "List schemas."])
            self.v_help.AddRow(["\\dt", "\\dt[+] [pattern]", "List tables."])
            self.v_help.AddRow(["\\dv", "\\dv[+] [pattern]", "List views."])
            self.v_help.AddRow(["\\ds", "\\ds[+] [pattern]", "List sequences."])
            self.v_help.AddRow(
                [
                    "\\d",
                    "\\d[+] [pattern]",
                    "List or describe tables, views and sequences.",
                ]
            )
            self.v_help.AddRow(
                [
                    "DESCRIBE",
                    "DESCRIBE [pattern]",
                    "Describe tables, views and sequences.",
                ]
            )
            self.v_help.AddRow(
                [
                    "describe",
                    "describe [pattern]",
                    "Describe tables, views and sequences.",
                ]
            )
            self.v_help.AddRow(["\\di", "\\di[+] [pattern]", "List indexes."])
            self.v_help.AddRow(
                ["\\dm", "\\dm[+] [pattern]", "List materialized views."]
            )
            self.v_help.AddRow(["\\df", "\\df[+] [pattern]", "List functions."])
            self.v_help.AddRow(
                ["\\sf", "\\sf[+] FUNCNAME", "Show a function's definition."]
            )
            self.v_help.AddRow(["\\dT", "\\dT[+] [pattern]", "List data types."])
            self.v_help.AddRow(["\\x", "\\x", "Toggle expanded output."])
            self.v_help.AddRow(["\\timing", "\\timing", "Toggle timing of commands."])
            self.v_helpcommands = Spartacus.Database.DataTable()
            self.v_helpcommands.Columns = ["SQL Command"]
            for s in list(HelpCommands.keys()):
                self.v_helpcommands.AddRow([s])
            self.v_expanded = False
            self.v_timing = False
            self.v_types = None
            psycopg2.extensions.register_type(
                psycopg2.extensions.new_type(
                    psycopg2.extensions.INTERVAL.values, "INTERVAL_STR", psycopg2.STRING
                ),
                self.v_cur,
            )
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "PostgreSQL is not supported. Please install it with 'pip install Spartacus[postgresql]'."
            )

    def GetConnectionString(self):
        if self.v_dsn is not None and self.v_dsn != "":
            if "application_name" not in self.v_dsn:
                self.v_dsn = "{0} application_name={1}".format(
                    self.v_dsn, self.v_application_name
                )
            return self.v_dsn
        elif self.v_conn_string is not None and self.v_conn_string != "":
            if self.v_conn_string_parsed.query == "":
                v_new_query = "?dbname={0}&port={1}".format(
                    self.v_service.replace("'", "\\'"), self.v_port
                )
            else:
                v_new_query = "&dbname={0}&port={1}".format(
                    self.v_service.replace("'", "\\'"), self.v_port
                )
            if self.v_host is None or self.v_host == "":
                None
            else:
                v_new_query = "{0}&host={1}".format(
                    v_new_query, self.v_host.replace("'", "\\'")
                )
            if self.v_password is None or self.v_password == "":
                v_return_string = "{0}{1}".format(self.v_conn_string, v_new_query)
            else:
                v_return_string = "{0}{1}&password={2}".format(
                    self.v_conn_string, v_new_query, self.v_password.replace("'", "\\'")
                )
            return v_return_string
        elif self.v_host is None or self.v_host == "":
            if self.v_password is None or self.v_password == "":
                return """port={0} dbname='{1}' user='{2}' application_name='{3}'""".format(
                    self.v_port,
                    self.v_service.replace("'", "\\'"),
                    self.v_user.replace("'", "\\'"),
                    self.v_application_name.replace("'", "\\'"),
                )
            else:
                return """port={0} dbname='{1}' user='{2}' password='{3}' application_name='{4}'""".format(
                    self.v_port,
                    self.v_service.replace("'", "\\'"),
                    self.v_user.replace("'", "\\'"),
                    self.v_password.replace("'", "\\'"),
                    self.v_application_name.replace("'", "\\'"),
                )
        else:
            return """host='{0}' port={1} dbname='{2}' user='{3}' password='{4}' application_name='{5}'""".format(
                self.v_host.replace("'", "\\'"),
                self.v_port,
                self.v_service.replace("'", "\\'"),
                self.v_user.replace("'", "\\'"),
                self.v_password.replace("'", "\\'"),
                self.v_application_name.replace("'", "\\'"),
            )

    def DateHandler(self, value, cursor):
        return value

    def Open(
        self,
        p_autocommit=True,
        p_datetime_as_string=False,
        p_json_as_string=False,
        p_async=False,
    ):
        try:
            if p_async:
                self.v_con = psycopg2.connect(
                    self.GetConnectionString(),
                    cursor_factory=psycopg2.extras.DictCursor,
                    async_=1,
                )
                self.Wait()
            else:
                self.v_con = psycopg2.connect(
                    self.GetConnectionString(),
                    cursor_factory=psycopg2.extras.DictCursor,
                )
                self.v_con.autocommit = p_autocommit
            self.v_cur = self.v_con.cursor()
            self.v_start = True
            self.v_cursor = None
            # PostgreSQL types
            if self.v_types is None:
                self.v_cur.execute("select oid, typname from pg_type")
                if p_async:
                    self.Wait()
                self.v_types = dict(
                    [(r["oid"], r["typname"]) for r in self.v_cur.fetchall()]
                )
                if p_datetime_as_string:
                    tmp = []
                    for oid, name in self.v_types.items():
                        if (
                            name == "date"
                            or name == "timestamp"
                            or name == "timestamptz"
                        ):
                            tmp.append(oid)
                    oids = tuple(tmp)
                    psycopg2.extensions.register_type(
                        psycopg2.extensions.new_type(oids, "DATE", self.DateHandler),
                        self.v_cur,
                    )
                if p_json_as_string:
                    psycopg2.extras.register_default_json(self.v_cur, loads=lambda x: x)
                    psycopg2.extras.register_default_jsonb(
                        self.v_cur, loads=lambda x: x
                    )
                if not p_autocommit and not p_async:
                    self.v_con.commit()
            self.v_con.notices = DataList()
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(
        self,
        p_sql,
        p_alltypesstr=False,
        p_simple=False,
        p_datetime_as_string=False,
        p_json_as_string=True,
    ):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open(
                    p_datetime_as_string=p_datetime_as_string,
                    p_json_as_string=p_json_as_string,
                )
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            if self.v_con.async_ == 1:
                self.Wait()
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_table.Rows = self.v_cur.fetchall()
                if p_alltypesstr:
                    for i in range(0, len(v_table.Rows)):
                        for j in range(0, len(v_table.Columns)):
                            if v_table.Rows[i][j] != None:
                                v_table.Rows[i][j] = self.String(v_table.Rows[i][j])
                            else:
                                v_table.Rows[i][j] = ""
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            if self.v_con.async_ == 1:
                self.Wait()
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql, p_datetime_as_string=False, p_json_as_string=True):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open(
                    p_datetime_as_string=p_datetime_as_string,
                    p_json_as_string=p_json_as_string,
                )
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            if self.v_con.async_ == 1:
                self.Wait()
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if self.v_con.async_ == 0:
                    if p_commit:
                        self.v_con.commit()
                    else:
                        self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                if p_usesameconn:
                    self.v_con.cancel()
                else:
                    v_con2 = psycopg2.connect(
                        self.GetConnectionString(),
                        cursor_factory=psycopg2.extras.DictCursor,
                    )
                    v_cur2 = v_con2.cursor()
                    v_pid = self.v_con.get_backend_pid()
                    v_cur2.execute("select pg_terminate_backend({0})".format(v_pid))
                    v_cur2.close()
                    v_con2.close()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.get_backend_pid()
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Terminate(self, p_pid):
        try:
            self.Execute("select pg_terminate_backend({0})".format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute("select * from ( " + p_sql + " ) t limit 1")
            r = self.v_cur.fetchone()
            v_sql = "select "
            v_first = True
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=self.v_types[c[1]])
                    )
                    if v_first:
                        v_sql = v_sql + "quote_ident('{0}')".format(c[0])
                        v_first = False
                    else:
                        v_sql = v_sql + ",quote_ident('{0}')".format(c[0])
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=self.v_types[c[1]])
                    )
                    if v_first:
                        v_sql = v_sql + "quote_ident('{0}')".format(c[0])
                        v_first = False
                    else:
                        v_sql = v_sql + ",quote_ident('{0}')".format(c[0])
                    k = k + 1
            self.v_cur.execute(v_sql)
            r = self.v_cur.fetchone()
            for k in range(0, len(self.v_cur.description)):
                v_fields[k].v_truename = r[k]
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.notices.v_list
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def ClearNotices(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                del self.v_con.notices.v_list[:]
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetStatus(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_cur.statusmessage
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                if self.v_con.closed == 0:
                    v_status = self.v_con.get_transaction_status()
                    if v_status == 4:
                        return 0
                    else:
                        return v_status + 1
                else:
                    return 0
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Parse(self, p_sql):
        try:
            v_statement = sqlparse.split(p_sql)
            v_analysis = sqlparse.parse(p_sql)
            if len(v_statement) == len(v_analysis):
                v_cursors = []
                for i in range(0, len(v_statement)):
                    if v_analysis[i].get_type() == "SELECT":
                        v_found_cte = False
                        v_found_dml = False
                        v_found_into = False
                        for v_token in v_analysis[i].flatten():
                            if v_token.ttype == sqlparse.tokens.Token.Keyword.CTE:
                                v_found_cte = True
                            if (
                                v_token.ttype == sqlparse.tokens.Token.Keyword.DML
                                and v_token.value.upper() != "SELECT"
                            ):
                                v_found_dml = True
                            if v_token.is_keyword and v_token.value.upper() == "INTO":
                                v_found_into = True
                        if not (v_found_cte and v_found_dml) and not v_found_into:
                            v_cursors.append(
                                "{0}_{1}".format(
                                    self.v_application_name, uuid.uuid4().hex
                                )
                            )
                if len(v_cursors) > 0:
                    v_sql = ""
                    j = 0
                    for i in range(0, len(v_statement)):
                        if v_analysis[i].get_type() == "SELECT":
                            if j < len(v_cursors) - 1:
                                v_sql = v_sql + v_statement[i]
                            else:
                                if self.v_autocommit:
                                    v_sql = (
                                        v_sql
                                        + " DECLARE {0} CURSOR WITH HOLD FOR {1}".format(
                                            v_cursors[j], v_statement[i]
                                        )
                                    )
                                else:
                                    v_sql = (
                                        v_sql
                                        + " DECLARE {0} CURSOR WITHOUT HOLD FOR {1}".format(
                                            v_cursors[j], v_statement[i]
                                        )
                                    )
                                self.v_cursor = v_cursors[j]
                            j = j + 1
                        else:
                            v_sql = v_sql + v_statement[i]
                    return v_sql
                else:
                    self.v_cursor = None
                    return p_sql
            else:
                self.v_cursor = None
                return p_sql
        except Exception as exc:
            self.v_cursor = None
            return p_sql

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_con.async_ == 1:
                    raise Spartacus.Database.Exception(
                        "This method is not allowed in asynchronous mode."
                    )
                else:
                    if self.v_start:
                        if self.v_cursor:
                            try:
                                self.v_cur.execute("CLOSE {0}".format(self.v_cursor))
                            except:
                                None
                        v_sql = self.Parse(p_sql)
                        if (
                            not self.v_autocommit
                            and not self.GetConStatus() == 3
                            and not self.GetConStatus() == 4
                        ):
                            self.v_cur.execute("BEGIN;")
                        self.v_cur.execute(v_sql)
                    v_table = DataTable()
                    if self.v_cursor:
                        if p_blocksize > 0:
                            self.v_cur.execute(
                                "FETCH {0} {1}".format(p_blocksize, self.v_cursor)
                            )
                        else:
                            self.v_cur.execute("FETCH ALL {0}".format(self.v_cursor))
                    if self.v_cur.description:
                        for c in self.v_cur.description:
                            v_table.AddColumn(c[0])
                        if p_blocksize > 0:
                            v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                        else:
                            v_table.Rows = self.v_cur.fetchall()
                        if p_alltypesstr:
                            for i in range(0, len(v_table.Rows)):
                                for j in range(0, len(v_table.Columns)):
                                    if v_table.Rows[i][j] != None:
                                        v_table.Rows[i][j] = self.String(
                                            v_table.Rows[i][j]
                                        )
                                    else:
                                        v_table.Rows[i][j] = ""
                    if self.v_start:
                        self.v_start = False
                    if len(v_table.Rows) < p_blocksize:
                        self.v_start = True
                        if self.v_cursor:
                            self.v_cur.execute("CLOSE {0}".format(self.v_cursor))
                            self.v_cursor = None
                    return v_table
        except Spartacus.Database.Exception as exc:
            self.v_start = True
            self.v_cursor = None
            raise exc
        except psycopg2.Error as exc:
            self.v_start = True
            self.v_cursor = None
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            self.v_start = True
            self.v_cursor = None
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_command = p_sql.lstrip().split(" ")[0].rstrip("+")
            v_title = None
            v_table = None
            v_status = None
            self.v_last_fetched_size = 0
            if v_command == "\\?":
                v_table = self.v_help
            elif v_command == "\\h" and len(p_sql.lstrip().split(" ")[1:]) == 0:
                v_title = 'Type "\h [parameter]" where "parameter" is a SQL Command from the list below:'
                v_table = self.v_helpcommands
            else:
                v_aux = self.v_help.Select("Command", v_command)
                if len(v_aux.Rows) > 0:
                    for r in self.v_special.execute(self.v_cur, p_sql):
                        v_result = r
                    if v_result[0]:
                        v_title = v_result[0]
                    if v_result[1]:
                        v_table = DataTable()
                        v_table.Columns = v_result[2]
                        if isinstance(v_result[1], type(self.v_cur)):
                            if v_result[1].description:
                                v_table.Rows = v_result[1].fetchall()
                        else:
                            for r in v_result[1]:
                                v_table.AddRow(r)
                    if v_result[3]:
                        v_status = v_result[3]
                        if v_status.strip() == "Expanded display is on.":
                            self.v_expanded = True
                        elif v_status.strip() == "Expanded display is off.":
                            self.v_expanded = False
                        elif v_status.strip() == "Timing is on.":
                            self.v_timing = True
                        elif v_status.strip() == "Timing is off.":
                            self.v_timing = False
                else:
                    if self.v_timing:
                        v_timestart = datetime.datetime.now()
                    v_table = self.QueryBlock(p_sql, 50, True, True)
                    self.v_last_fetched_size = len(v_table.Rows)
                    v_status = self.GetStatus()
                    if self.v_timing:
                        v_status = v_status + "\nTime: {0}".format(
                            datetime.datetime.now() - v_timestart
                        )
            if v_title and v_table and len(v_table.Rows) > 0 and v_status:
                return (
                    v_title + "\n" + v_table.Pretty(self.v_expanded) + "\n" + v_status
                )
            elif v_title and v_table and len(v_table.Rows) > 0:
                return v_title + "\n" + v_table.Pretty(self.v_expanded)
            elif v_title and v_status:
                return v_title + "\n" + v_status
            elif v_title:
                return v_title
            elif v_table and len(v_table.Rows) > 0 and v_status:
                return v_table.Pretty(self.v_expanded) + "\n" + v_status
            elif v_table and len(v_table.Rows) > 0:
                return v_table.Pretty(self.v_expanded)
            elif v_status:
                return v_status
            else:
                return ""
        except Spartacus.Database.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Poll(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_con.async_ == 0:
                    raise Spartacus.Database.Exception(
                        "This method should be called in the context of an asynchronous connection."
                    )
                else:
                    v_state = self.v_con.poll()
                    if v_state == psycopg2.extensions.POLL_OK:
                        return 0
                    elif v_state == psycopg2.extensions.POLL_WRITE:
                        v_poll = select.select([], [self.v_con.fileno()], [], 0)
                        if self.v_con.fileno() in v_poll[1]:
                            return 1
                        else:
                            return -1
                    elif v_state == psycopg2.extensions.POLL_READ:
                        v_poll = select.select([self.v_con.fileno()], [], [], 0)
                        if self.v_con.fileno() in v_poll[0]:
                            return 2
                        else:
                            return -2
                    else:
                        raise Spartacus.Database.Exception(
                            "Unknown poll state {0}.".format(v_state)
                        )
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Wait(self):
        x = self.Poll()
        while x != 0:
            x = self.Poll()

    def AsyncStmtStart(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_con.async_ == 0:
                    raise Spartacus.Database.Exception(
                        "This method should be called in the context of an asynchronous connection."
                    )
                else:
                    if not self.v_start:
                        raise Spartacus.Database.Exception(
                            "Can only start a single statement per asynchronous connection."
                        )
                    else:
                        self.v_cur.execute(p_sql)
                        self.v_start = False
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def AsyncStmtEnd(self):
        if self.v_con is None:
            raise Spartacus.Database.Exception(
                "This method should be called in the middle of Open() and Close() calls."
            )
        else:
            if self.v_con.async_ == 0:
                raise Spartacus.Database.Exception(
                    "This method should be called in the context of an asynchronous connection."
                )
            else:
                if self.v_start:
                    raise Spartacus.Database.Exception("No statement was started.")
                else:
                    if self.Poll() != 0:
                        raise Spartacus.Database.Exception(
                            "A statement has not finished yet."
                        )
                    else:
                        self.v_start = True

    def AsyncFetchTable(self, p_alltypesstr=False):
        try:
            v_table = None
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_con.async_ == 0:
                    raise Spartacus.Database.Exception(
                        "This method should be called in the context of an asynchronous connection."
                    )
                else:
                    if self.v_start:
                        raise Spartacus.Database.Exception("No statement was started.")
                    else:
                        if self.Poll() != 0:
                            raise Spartacus.Database.Exception(
                                "A statement has not finished yet."
                            )
                        else:
                            v_table = DataTable()
                            if self.v_cur.description:
                                for c in self.v_cur.description:
                                    v_table.AddColumn(c[0])
                                v_table.Rows = self.v_cur.fetchall()
                                if p_alltypesstr:
                                    for i in range(0, len(v_table.Rows)):
                                        for j in range(0, len(v_table.Columns)):
                                            if v_table.Rows[i][j] != None:
                                                v_table.Rows[i][j] = self.String(
                                                    v_table.Rows[i][j]
                                                )
                                            else:
                                                v_table.Rows[i][j] = ""
                            self.v_start = True
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))


"""
------------------------------------------------------------------------
MySQL
------------------------------------------------------------------------
"""


class MySQL(Generic):
    def __init__(
        self,
        p_host,
        p_port,
        p_service,
        p_user,
        p_password,
        p_conn_string="",
        p_encoding=None,
    ):
        if "MySQL" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 3306
            else:
                self.v_port = p_port
            self.v_conn_string = p_conn_string
            self.v_conn_string_parsed = urlparse(p_conn_string)
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_help = Spartacus.Database.DataTable()
            self.v_help.Columns = ["Command", "Syntax", "Description"]
            self.v_help.AddRow(["\\?", "\\?", "Show Commands."])
            self.v_help.AddRow(["\\x", "\\x", "Toggle expanded output."])
            self.v_help.AddRow(["\\timing", "\\timing", "Toggle timing of commands."])
            self.v_expanded = False
            self.v_timing = False
            self.v_status = 0
            self.v_con_id = 0
            self.v_types = {
                0: "DECIMAL",
                1: "TINY",
                2: "SHORT",
                3: "LONG",
                4: "FLOAT",
                5: "DOUBLE",
                6: "NULL",
                7: "TIMESTAMP",
                8: "LONGLONG",
                9: "INT24",
                10: "DATE",
                11: "TIME",
                12: "DATETIME",
                13: "YEAR",
                14: "NEWDATE",
                15: "VARCHAR",
                16: "BIT",
                245: "JSON",
                246: "NEWDECIMAL",
                247: "ENUM",
                248: "SET",
                249: "TINY_BLOB",
                250: "MEDIUM_BLOB",
                251: "LONG_BLOB",
                252: "BLOB",
                253: "VAR_STRING",
                254: "STRING",
                255: "GEOMETRY",
            }
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "MySQL is not supported. Please install it with 'pip install Spartacus[mysql]'."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymysql.connect(
                host=self.v_host,
                port=int(self.v_port),
                db=self.v_service,
                user=self.v_user,
                password=self.v_password,
                autocommit=p_autocommit,
                read_default_file="~/.my.cnf",
            )
            self.v_cur = self.v_con.cursor()
            self.v_start = True
            self.v_status = 0
            self.v_con_id = self.ExecuteScalar("select connection_id()")
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                v_con2 = pymysql.connect(
                    host=self.v_host,
                    port=int(self.v_port),
                    db=self.v_service,
                    user=self.v_user,
                    password=self.v_password,
                )
                v_cur2 = v_con2.cursor()
                self.v_status = v_cur2.execute("kill {0}".format(self.v_con_id))
                v_cur2.close()
                v_con2.close()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return self.v_con_id

    def Terminate(self, p_pid):
        try:
            self.Execute("kill {0}".format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_status = self.v_cur.execute(
                "select * from ( " + p_sql + " ) t limit 1"
            )
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=self.v_types[c[1]])
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=self.v_types[c[1]])
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_status
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetConStatus(self):
        try:
            if self.v_con is None or not self.v_con.open:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_status = self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_command = p_sql.lstrip().split(" ")[0].rstrip("+")
            v_title = None
            v_table = None
            v_status = None
            if v_command == "\\?":
                v_table = self.v_help
            else:
                v_aux = self.v_help.Select("Command", v_command)
                if len(v_aux.Rows) > 0:
                    if v_command == "\\x" and not self.v_expanded:
                        v_status = "Expanded display is on."
                        self.v_expanded = True
                    elif v_command == "\\x" and self.v_expanded:
                        v_status = "Expanded display is off."
                        self.v_expanded = False
                    elif v_command == "\\timing" and not self.v_timing:
                        v_status = "Timing is on."
                        self.v_timing = True
                    elif v_command == "\\timing" and self.v_timing:
                        v_status = "Timing is off."
                        self.v_timing = False
                else:
                    if self.v_timing:
                        v_timestart = datetime.datetime.now()
                    v_table = self.Query(p_sql, True)
                    v_tmp = self.GetStatus()
                    if v_tmp == 1:
                        v_status = "1 row "
                    else:
                        v_status = "{0} rows ".format(v_tmp)
                    if v_command.lower() == "select":
                        v_status = v_status + "in set"
                    else:
                        v_status = v_status + "affected"
                    if self.v_timing:
                        v_status = v_status + "\nTime: {0}".format(
                            datetime.datetime.now() - v_timestart
                        )
            if v_title and v_table and len(v_table.Rows) > 0 and v_status:
                return (
                    v_title + "\n" + v_table.Pretty(self.v_expanded) + "\n" + v_status
                )
            elif v_title and v_table and len(v_table.Rows) > 0:
                return v_title + "\n" + v_table.Pretty(self.v_expanded)
            elif v_title and v_status:
                return v_title + "\n" + v_status
            elif v_title:
                return v_title
            elif v_table and len(v_table.Rows) > 0 and v_status:
                return v_table.Pretty(self.v_expanded) + "\n" + v_status
            elif v_table and len(v_table.Rows) > 0:
                return v_table.Pretty(self.v_expanded)
            elif v_status:
                return v_status
            else:
                return ""
        except Spartacus.Database.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()


"""
------------------------------------------------------------------------
MariaDB
------------------------------------------------------------------------
"""


class MariaDB(Generic):
    def __init__(
        self,
        p_host,
        p_port,
        p_service,
        p_user,
        p_password,
        p_conn_string="",
        p_encoding=None,
    ):
        if "MariaDB" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 3306
            else:
                self.v_port = p_port
            self.v_conn_string = p_conn_string
            self.v_conn_string_parsed = urlparse(p_conn_string)
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_help = Spartacus.Database.DataTable()
            self.v_help.Columns = ["Command", "Syntax", "Description"]
            self.v_help.AddRow(["\\?", "\\?", "Show Commands."])
            self.v_help.AddRow(["\\x", "\\x", "Toggle expanded output."])
            self.v_help.AddRow(["\\timing", "\\timing", "Toggle timing of commands."])
            self.v_expanded = False
            self.v_timing = False
            self.v_status = 0
            self.v_con_id = 0
            self.v_types = {
                0: "DECIMAL",
                1: "TINY",
                2: "SHORT",
                3: "LONG",
                4: "FLOAT",
                5: "DOUBLE",
                6: "NULL",
                7: "TIMESTAMP",
                8: "LONGLONG",
                9: "INT24",
                10: "DATE",
                11: "TIME",
                12: "DATETIME",
                13: "YEAR",
                14: "NEWDATE",
                15: "VARCHAR",
                16: "BIT",
                245: "JSON",
                246: "NEWDECIMAL",
                247: "ENUM",
                248: "SET",
                249: "TINY_BLOB",
                250: "MEDIUM_BLOB",
                251: "LONG_BLOB",
                252: "BLOB",
                253: "VAR_STRING",
                254: "STRING",
                255: "GEOMETRY",
            }
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "MariaDB is not supported. Please install it with 'pip install Spartacus[mariadb]'."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymysql.connect(
                host=self.v_host,
                port=int(self.v_port),
                db=self.v_service,
                user=self.v_user,
                password=self.v_password,
                autocommit=p_autocommit,
                read_default_file="~/.my.cnf",
            )
            self.v_cur = self.v_con.cursor()
            self.v_start = True
            self.v_status = 0
            self.v_con_id = self.ExecuteScalar("select connection_id()")
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_status = self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                v_con2 = pymysql.connect(
                    host=self.v_host,
                    port=int(self.v_port),
                    db=self.v_service,
                    user=self.v_user,
                    password=self.v_password,
                )
                v_cur2 = v_con2.cursor()
                self.v_status = v_cur2.execute("kill {0}".format(self.v_con_id))
                v_cur2.close()
                v_con2.close()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return self.v_con_id

    def Terminate(self, p_pid):
        try:
            self.Execute("kill {0}".format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_status = self.v_cur.execute(
                "select * from ( " + p_sql + " ) t limit 1"
            )
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=self.v_types[c[1]])
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=self.v_types[c[1]])
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_status
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_status = self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_command = p_sql.lstrip().split(" ")[0].rstrip("+")
            v_title = None
            v_table = None
            v_status = None
            if v_command == "\\?":
                v_table = self.v_help
            else:
                v_aux = self.v_help.Select("Command", v_command)
                if len(v_aux.Rows) > 0:
                    if v_command == "\\x" and not self.v_expanded:
                        v_status = "Expanded display is on."
                        self.v_expanded = True
                    elif v_command == "\\x" and self.v_expanded:
                        v_status = "Expanded display is off."
                        self.v_expanded = False
                    elif v_command == "\\timing" and not self.v_timing:
                        v_status = "Timing is on."
                        self.v_timing = True
                    elif v_command == "\\timing" and self.v_timing:
                        v_status = "Timing is off."
                        self.v_timing = False
                else:
                    if self.v_timing:
                        v_timestart = datetime.datetime.now()
                    v_table = self.Query(p_sql, True)
                    v_tmp = self.GetStatus()
                    if v_tmp == 1:
                        v_status = "1 row "
                    else:
                        v_status = "{0} rows ".format(v_tmp)
                    if v_command.lower() == "select":
                        v_status = v_status + "in set"
                    else:
                        v_status = v_status + "affected"
                    if self.v_timing:
                        v_status = v_status + "\nTime: {0}".format(
                            datetime.datetime.now() - v_timestart
                        )
            if v_title and v_table and len(v_table.Rows) > 0 and v_status:
                return (
                    v_title + "\n" + v_table.Pretty(self.v_expanded) + "\n" + v_status
                )
            elif v_title and v_table and len(v_table.Rows) > 0:
                return v_title + "\n" + v_table.Pretty(self.v_expanded)
            elif v_title and v_status:
                return v_title + "\n" + v_status
            elif v_title:
                return v_title
            elif v_table and len(v_table.Rows) > 0 and v_status:
                return v_table.Pretty(self.v_expanded) + "\n" + v_status
            elif v_table and len(v_table.Rows) > 0:
                return v_table.Pretty(self.v_expanded)
            elif v_status:
                return v_status
            else:
                return ""
        except Spartacus.Database.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()


"""
------------------------------------------------------------------------
Firebird
------------------------------------------------------------------------
"""


class Firebird(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password, p_encoding=None):
        if "Firebird" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 3050
            else:
                self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            if p_encoding is not None:
                self.v_encoding = p_encoding
            else:
                self.v_encoding = "UTF8"
        else:
            raise Spartacus.Database.Exception(
                "Firebird is not supported. Please install it with 'pip install Spartacus[firebird]'."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            self.v_con = fdb.connect(
                host=self.v_host,
                port=int(self.v_port),
                database=self.v_service,
                user=self.v_user,
                password=self.v_password,
                charset=self.v_encoding,
            )
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        pass

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute("select first 1 * from ( " + p_sql + " )")
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k]))
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=type(None))
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        return None

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()


"""
------------------------------------------------------------------------
Oracle
------------------------------------------------------------------------
"""


class Oracle(Generic):
    def __init__(
        self,
        p_host,
        p_port,
        p_service,
        p_user,
        p_password,
        p_conn_string="",
        p_encoding=None,
    ):
        if "Oracle" in v_supported_rdbms:
            self.v_host = p_host
            if p_host is not None and (p_port is None or p_port == ""):
                self.v_port = 1521
            else:
                self.v_port = p_port
            if p_service is None or p_service == "":
                self.v_service = "xe"
            else:
                self.v_service = p_service
            self.v_conn_string = p_conn_string
            self.v_conn_string_parsed = urlparse(p_conn_string)
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_help = Spartacus.Database.DataTable()
            self.v_help.Columns = ["Command", "Syntax", "Description"]
            self.v_help.AddRow(["\\?", "\\?", "Show Commands."])
            self.v_help.AddRow(["\\x", "\\x", "Toggle expanded output."])
            self.v_help.AddRow(["\\timing", "\\timing", "Toggle timing of commands."])
            self.v_expanded = False
            self.v_timing = False
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "Oracle is not supported. Please install it with 'pip install Spartacus[oracle]'."
            )

    def GetConnectionString(self):
        if self.v_host is None and self.v_port is None:  # tnsnames.ora
            if self.v_password is None or self.v_password == "":
                return """{0}/@{1}""".format(
                    self.v_user.replace("'", "\\'"), self.v_service.replace("'", "\\'")
                )
            else:
                return """{0}/{1}@{2}""".format(
                    self.v_user.replace("'", "\\'"),
                    self.v_password.replace("'", "\\'"),
                    self.v_service.replace("'", "\\'"),
                )
        else:
            if self.v_password is None or self.v_password == "":
                return """{0}/@{1}:{2}/{3}""".format(
                    self.v_user.replace("'", "\\'"),
                    self.v_host.replace("'", "\\'"),
                    self.v_port,
                    self.v_service.replace("'", "\\'"),
                )
            else:
                return """{0}/{1}@{2}:{3}/{4}""".format(
                    self.v_user.replace("'", "\\'"),
                    self.v_password.replace("'", "\\'"),
                    self.v_host.replace("'", "\\'"),
                    self.v_port,
                    self.v_service.replace("'", "\\'"),
                )

    def Handler(self, p_cursor, p_name, p_type, p_size, p_precision, p_scale):
        if p_type == cx_Oracle.NUMBER:
            return p_cursor.var(
                str,
                size=100,
                arraysize=p_cursor.arraysize,
                outconverter=decimal.Decimal,
            )
        elif p_type == cx_Oracle.CLOB:
            return p_cursor.var(cx_Oracle.LONG_STRING, arraysize=p_cursor.arraysize)
        elif p_type == cx_Oracle.BLOB:
            return p_cursor.var(cx_Oracle.LONG_BINARY, arraysize=p_cursor.arraysize)

    def Open(self, p_autocommit=True):
        try:
            self.v_con = cx_Oracle.connect(self.GetConnectionString())
            self.v_con.outputtypehandler = self.Handler
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        try:
            self.Execute("alter system kill session '{0}' immediate".format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute("select * from ( " + p_sql + " ) t where rownum <= 1")
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=c[1].__name__)
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=c[1].__name__)
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_cur.rowcount
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                try:
                    self.v_con.ping()
                    return 1
                except:
                    return 0
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_command = p_sql.lstrip().split(" ")[0].rstrip("+")
            v_title = None
            v_table = None
            v_status = None
            if v_command == "\\?":
                v_table = self.v_help
            else:
                v_aux = self.v_help.Select("Command", v_command)
                if len(v_aux.Rows) > 0:
                    if v_command == "\\x" and not self.v_expanded:
                        v_status = "Expanded display is on."
                        self.v_expanded = True
                    elif v_command == "\\x" and self.v_expanded:
                        v_status = "Expanded display is off."
                        self.v_expanded = False
                    elif v_command == "\\timing" and not self.v_timing:
                        v_status = "Timing is on."
                        self.v_timing = True
                    elif v_command == "\\timing" and self.v_timing:
                        v_status = "Timing is off."
                        self.v_timing = False
                else:
                    if self.v_timing:
                        v_timestart = datetime.datetime.now()
                    v_table = self.Query(p_sql, True)
                    v_tmp = self.GetStatus()
                    if v_tmp == 1:
                        v_status = "1 row "
                    else:
                        v_status = "{0} rows ".format(v_tmp)
                    if v_command.lower() == "select":
                        v_status = v_status + "in set"
                    else:
                        v_status = v_status + "affected"
                    if self.v_timing:
                        v_status = v_status + "\nTime: {0}".format(
                            datetime.datetime.now() - v_timestart
                        )
            if v_title and v_table and len(v_table.Rows) > 0 and v_status:
                return (
                    v_title + "\n" + v_table.Pretty(self.v_expanded) + "\n" + v_status
                )
            elif v_title and v_table and len(v_table.Rows) > 0:
                return v_title + "\n" + v_table.Pretty(self.v_expanded)
            elif v_title and v_status:
                return v_title + "\n" + v_status
            elif v_title:
                return v_title
            elif v_table and len(v_table.Rows) > 0 and v_status:
                return v_table.Pretty(self.v_expanded) + "\n" + v_status
            elif v_table and len(v_table.Rows) > 0:
                return v_table.Pretty(self.v_expanded)
            elif v_status:
                return v_status
            else:
                return ""
        except Spartacus.Database.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()


"""
------------------------------------------------------------------------
MSSQL
------------------------------------------------------------------------
"""


class MSSQL(Generic):
    def __init__(
        self,
        p_host,
        p_port,
        p_service,
        p_user,
        p_password,
        p_conn_string="",
        p_encoding=None,
    ):
        if "MSSQL" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 1433
            else:
                self.v_port = p_port
            self.v_conn_string = p_conn_string
            self.v_conn_string_parsed = urlparse(p_conn_string)
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "MSSQL is not supported. Please install it with 'pip install Spartacus[mssql]'."
            )

    def GetConnectionString(self):
        return None

    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymssql.connect(
                host=self.v_host,
                port=int(self.v_port),
                database=self.v_service,
                user=self.v_user,
                password=self.v_password,
            )
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        pass

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute(
                "select top 1 limit_alias.* from ( " + p_sql + " ) limit_alias"
            )
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k]))
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=type(None))
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        return None

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()


"""
------------------------------------------------------------------------
IBM DB2
------------------------------------------------------------------------
"""


class IBMDB2(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password, p_encoding=None):
        if "IBMDB2" in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == "":
                self.v_port = 50000
            else:
                self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_encoding = p_encoding
        else:
            raise Spartacus.Database.Exception(
                "IBM DB2 is not supported. Please install it with 'pip install Spartacus[ibmdb2]'."
            )

    def GetConnectionString(self):
        return """DATABASE={0};HOSTNAME={1};PORT={2};PROTOCOL=TCPIP;UID={3};PWD={4}""".format(
            self.v_service.replace("'", "\\'"),
            self.v_host.replace("'", "\\'"),
            self.v_port,
            self.v_user.replace("'", "\\'"),
            self.v_password.replace("'", "\\'"),
        )

    def Open(self, p_autocommit=True):
        try:
            c = ibm_db.connect(self.GetConnectionString(), "", "")
            self.v_con = ibm_db_dbi.Connection(c)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except ibm_db.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable(None, p_alltypesstr, p_simple)
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.AddColumn(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_table.AddRow(list(v_row))
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def Close(self, p_commit=True):
        try:
            if self.v_con:
                if p_commit:
                    self.v_con.commit()
                else:
                    self.v_con.rollback()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Commit(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.commit()
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Rollback(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                return self.v_con.rollback()
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Cancel(self, p_usesameconn=True):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
                self.v_start = True
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def GetPID(self):
        return None

    def Terminate(self, p_pid):
        pass

    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute("select * from ( " + p_sql + " ) t limit 1")
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k]))
                    )
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(
                        DataField(c[0], p_type=type(None), p_dbtype=type(None))
                    )
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()

    def GetNotices(self):
        return []

    def ClearNotices(self):
        pass

    def GetStatus(self):
        return None

    def GetConStatus(self):
        try:
            if self.v_con is None:
                return 0
            else:
                return 1
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception(
                    "This method should be called in the middle of Open() and Close() calls."
                )
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable(None, p_alltypesstr, p_simple)
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.AddColumn(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_table.AddRow(list(v_row))
                            k = k + 1
                            if k < p_blocksize:
                                v_row = self.v_cur.fetchone()
                    else:
                        while v_row is not None:
                            v_table.AddRow(list(v_row))
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                if len(v_table.Rows) < p_blocksize:
                    self.v_start = True
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute(
                "insert into "
                + p_tablename
                + "("
                + ",".join(v_columnames)
                + ") values "
                + ",".join(v_values)
                + ""
            )
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()
