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


class ReportFilterOperator(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER_THAN = 3
    LESS_THAN = 4
    CONTAINS = 5
    BETWEEN = 6
    TODAY = 7
    PAST = 8
    FUTURE = 9
    LAST_N_DAYS = 10
    NEXT_N_DAYS = 11
    IS_BLANK = 12
    IS_NOT_BLANK = 13
    IS_NUMBER = 14
    IS_NOT_NUMBER = 15
    IS_DATE = 16
    IS_NOT_DATE = 17
    IS_CHECKED = 18
    IS_UNCHECKED = 19
    IS_ONE_OF = 20
    IS_NOT_ONE_OF = 21
    LESS_THAN_OR_EQUAL = 22
    GREATER_THAN_OR_EQUAL = 23
    DOES_NOT_CONTAIN = 24
    NOT_BETWEEN = 25
    NOT_TODAY = 26
    NOT_PAST = 27
    NOT_FUTURE = 28
    NOT_LAST_N_DAYS = 29
    NOT_NEXT_N_DAYS = 30
    HAS_ANY_OF = 31
    HAS_NONE_OF = 32
    HAS_ALL_OF = 33
    NOT_ALL_OF = 34
    MULTI_IS_EQUAL = 35
    MULTI_IS_NOT_EQUAL = 36
