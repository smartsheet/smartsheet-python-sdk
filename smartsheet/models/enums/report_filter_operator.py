# pylint: disable=C0111,R0902,R0904,R0912,R0913,R0915,E1101
# Smartsheet Python SDK.
#
# Copyright 2018 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from enum import Enum


class ReportFilterOperator(str, Enum):
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    CONTAINS = 'CONTAINS'
    BETWEEN = 'BETWEEN'
    TODAY = 'TODAY'
    PAST = 'PAST'
    FUTURE = 'FUTURE'
    LAST_N_DAYS = 'LAST_N_DAYS'
    NEXT_N_DAYS = 'NEXT_N_DAYS'
    IS_BLANK = 'IS_BLANK'
    IS_NOT_BLANK = 'IS_NOT_BLANK'
    IS_NUMBER = 'IS_NUMBER'
    IS_NOT_NUMBER = 'IS_NOT_NUMBER'
    IS_DATE = 'IS_DATE'
    IS_NOT_DATE = 'IS_NOT_DATE'
    IS_CHECKED = 'IS_CHECKED'
    IS_UNCHECKED = 'IS_UNCHECKED'
    IS_ONE_OF = 'IS_ONE_OF'
    IS_NOT_ONE_OF = 'IS_NOT_ONE_OF'
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    DOES_NOT_CONTAIN = 'DOES_NOT_CONTAIN'
    NOT_BETWEEN = 'NOT_BETWEEN'
    NOT_TODAY = 'NOT_TODAY'
    NOT_PAST = 'NOT_PAST'
    NOT_FUTURE = 'NOT_FUTURE'
    NOT_LAST_N_DAYS = 'NOT_LAST_N_DAYS'
    NOT_NEXT_N_DAYS = 'NOT_NEXT_N_DAYS'
    HAS_ANY_OF = 'HAS_ANY_OF'
    HAS_NONE_OF = 'HAS_NONE_OF'
    HAS_ALL_OF = 'HAS_ALL_OF'
    NOT_ALL_OF = 'NOT_ALL_OF'
    MULTI_IS_EQUAL = 'MULTI_IS_EQUAL'
    MULTI_IS_NOT_EQUAL = 'MULTI_IS_NOT_EQUAL'
