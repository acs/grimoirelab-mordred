#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, 51 Franklin Street, Fifth Floor, Boston, MA 02110-1335, USA.
#
# Authors:
#     Luis Cañas-Díaz <lcanas@bitergia.com>
#


import sys
import unittest

import redis

from rq import Queue, use_connection
from rq.job import Job, JobStatus


# Hack to make sure that tests import the right packages
# due to setuptools behaviour
sys.path.insert(0, '..')


class TestRedis(unittest.TestCase):
    """Task tests"""

    def test_conn(self):

        with self.assertRaises(TypeError):
            redis_conn = redis.Redis(host1=None)

        # The Redis class does not try to connect
        redis_conn = redis.Redis(host=None)
        self.assertIsNotNone(redis_conn)


        redis_conn = redis.Redis(
            host="localhost",
            port=6379,
            password=None,
            db=None
        )

        # pipe = conn.pipeline()
        # pipe.lrange(Q_STORAGE_ITEMS, 0, -1)
        # pipe.ltrim(Q_STORAGE_ITEMS, 1, 0)
        # items = pipe.execute()[0]

    def test_read_queues(self):
        redis_conn = redis.Redis(
            host="46.101.142.213",
            port=6379,
            password=None,
            db=8
        )

        use_connection(redis_conn)

        print(Queue.all())

    def atest_read_tasks(self):

        redis_conn = redis.Redis(
            host="46.101.142.213",
            port=6379,
            password=None,
            db=8
        )

        use_connection(redis_conn)

        for queue in Queue.all():
            print("Getting jobs for ", queue)
            for job in queue.get_jobs():
                print(job)

    def test_read_tasks_failed(self):

        redis_conn = redis.Redis(
            host="46.101.142.213",
            port=6379,
            password=None,
            db=8
        )

        use_connection(redis_conn)

        for job in Queue('failed').get_job_ids():
            print(job)

        # Show details for a failed job
        job_failed = Job(Queue('failed').get_job_ids()[0])
        print (job_failed, job_failed.status)




if __name__ == "__main__":
    unittest.main(warnings='ignore')
