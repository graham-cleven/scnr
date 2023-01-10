#! /usr/bin/env python3


from urllib import response
from RBAC import ad_logic
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import json
from models import *
from settings import engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import *
import util


db = scoped_session(sessionmaker(bind=engine))

# box routes


def add_boxes():
    if request.method == "POST":
        verify_jwt_in_request()
        jwt = get_jwt_identity()

        form = AddBoxesForm()
        if form.validate():

            if form.network.data:
                ips = util.split_network(form.network.data)
                for ip in ips:
                    new_box = Boxes(box_ip=ip, box_hostname=None,
                                    box_os_cat="Windows")
                    db.add(new_box)

            elif form.ip_address.data:
                new_box = Boxes(box_ip=form.ip_address.data, box_hostname=None)
                db.add(new_box)

            elif form.hostname.data:
                new_box = Boxes(box_ip=None, box_hostname=form.hostname.data)
                db.add(new_box)

            elif form.object_name.data:
                # ad lookup
                pass

            db.commit()

            return {"status": "complete"}, 200

        else:
            return {"data": form.errors, "status": "failure"}, 400

    if request.method == "OPTIONS":
        return {"status": "complete"}, 200


def remove_box():
    pass


def get_boxes():
    if request.method == "POST":
        verify_jwt_in_request()
        jwt = get_jwt_identity()
        form = GetBoxesForm()

        if form.validate():
            boxes = db.query(Boxes).paginate(
                page=form.page_number.data,
                per_page=form.page_count.data,
                max_per_page=100,
            )
            return {
                "status": "complete",
                "data": util.asDict(boxes.items),
                "total_pages": boxes.pages,
            }, 200

            # box_filter = {"os": ["%"], "os_cat": ["%"], "hostname": ["%"], "ip": ["%"]}

            # conditions = or_((Boxes.box_os_cat.ilike(x) for x in box_filter["os_cat"]))
            # #con = (or_((Boxes.box_os_cat == x for x in box_filter['os_cat'])))
            # q = db.query(Boxes)

            # boxes = (
            #    q.filter(conditions)
            #    .paginate(page=form.page_number.data, max_per_page=form.page_count.data)
            #    .items
            # )

            # #boxes = Boxes.query.filter(or_(Boxes.box_os_cat.ilike(in_(box_filter['os_cat'])))).all()
            # return {"status": "complete", "data": util.asDict(boxes), "pages": 0}, 200

        else:
            return {"status": "error", "data": form.errors}, 400

    elif request.method == "OPTIONS":
        return {}, 200


def ad_add():
    pass


def get_ad_groups():
    # Add computer or group from LDAP on add_boxes form
    if request.method == "OPTIONS":
        return {}, 200
    elif request.method == "POST":

        ous = ad_logic.getOUs()
        computers = ad_logic.getComputers()

        return {"data": {"ous": ous, "groups": groups}, "status": "complete"}, 200


# job control routes

# new job
def new_job():
    if request.method == "POST":
        verify_jwt_in_request()
        jwt = get_jwt_identity()
        form = NewNLPJobForm()

        if form.validate():

            new_job = Jobs(
                job_creator=jwt["user_id"], job_query=form.job_query.data)
            db.add(new_job)

            # flush to get id of new object before commiting
            db.flush()

            # call the Daemon
            try:
                query = {
                    "cmd": "create_job",
                    "job_id": new_job.job_id,
                    "data": f"{form.job_query.data}",
                }
                query = json.dumps(query)
            except:
                return {"status": "error", "data": "malformed_query"}, 400

            try:
                util.unix_socket(query)
                db.commit()
            except:
                db.flush()
                db.rollback()
                return {
                    "status": "error",
                    "data": "Cannot connect to Daemon socket",
                }, 400

            # return job_id to query for job progress
            return {"status": "complete", "data": new_job.job_id}, 200
        else:
            return {"status": "error", "data": form.errors}, 400

    if request.method == "OPTIONS":
        return {}, 200


# stop job
# view jobs
def view_jobs():
    if request.method == "OPTIONS":
        return {}, 200

    if request.method == "POST":
        verify_jwt_in_request()
        jwt = get_jwt_identity()

        jobs = db.query(Jobs).all()
        return {"data": util.asDict(jobs), "status": "complete"}


# view job
def view_job():
    def aggregate_job(responses=None):
        if len(responses) == 1:
            return responses
        for response in responses:
            json.loads(response.response_output)

    if request.method == "OPTIONS":
        return {"status": "complete"}, 200

    if request.method == "POST":
        form = ViewJobForm()
        if not form.validate():
            return {"status": "error", "data": form.errors}, 400

        verify_jwt_in_request()
        jwt = get_jwt_identity()

        job = (
            db.query(Jobs).filter_by(
                job_id=form.job_id.data, job_creator=jwt["user_id"]
            )
        ).all()
        if not job:
            return {
                "status": "error",
                "data": "no job record found for specified ID",
            }, 400

        responses = db.query(Responses).filter_by(
            job_id=form.job_id.data).all()
        if not responses:
            return {"status": "error", "data": "no responses"}, 400
        return {
            "status": {
                "failed" : 0,
                "running" : 0,
                "complete" : 0,
                "percent" : 0
            },
            "data": {"job": util.asDict(job)},
            "aggregate_responses": aggregate_job(responses=responses),
        }, 200
