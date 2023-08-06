# pylint: disable=no-self-use
import rethinkdb
import rethinkdb.ast

from ...core import QueryRow, BaseTransformationQueryParser
from .utils import _build_row

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.11.6"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['RethinkDBTransformationQueryParser']


class RethinkDBTransformationQueryParser(BaseTransformationQueryParser[rethinkdb.ast.RqlQuery]):

    def process_group_statement(self, db_query: rethinkdb.ast.RqlQuery, group_row: QueryRow) -> rethinkdb.ast.RqlQuery:
        return db_query.group(_build_row(group_row))
