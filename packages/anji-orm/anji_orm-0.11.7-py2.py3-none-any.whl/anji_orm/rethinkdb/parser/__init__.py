from typing import Type

import rethinkdb
import rethinkdb.ast
import rethinkdb.query

from ...core import BaseQueryParser, Model, QueryAst
from .filter_parser import RethinkDBFilterQueryParser
from .transformation_parser import RethinkDBTransformationQueryParser
from .operation_parser import RethinkDBOperationQueryParser

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.11.7"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = ['RethinkDBQueryParser']


class RethinkDBQueryParser(BaseQueryParser[rethinkdb.ast.RqlQuery]):  # pylint: disable=too-few-public-methods

    __filter_parser__ = RethinkDBFilterQueryParser
    __transformation_parser__ = RethinkDBTransformationQueryParser
    __operation_parser__ = RethinkDBOperationQueryParser

    def initial_query(self, model_class: Type[Model], _query: QueryAst) -> rethinkdb.ast.RqlQuery:  # pylint: disable=no-self-use
        return rethinkdb.query.table(model_class._table)
