#!/usr/bin/env python3


from settings import app
import ums_routes
import core_routes
import sys
sys.path.append('../')
from RBAC import rbac
from RBAC import check_perms


@app.route('/api/v1/new_job', methods=['OPTIONS', 'POST'])
def new_job():
    return core_routes.new_job()


@app.route('/api/v1/view_jobs', methods=['OPTIONS', 'POST'])
def view_jobs():
    return core_routes.view_jobs()


@app.route('/api/v1/view_job', methods=['OPTIONS', 'POST'])
def view_job():
    return core_routes.view_job()


@app.route('/api/v1/ad_search', methods=['OPTIONS', 'POST'])
def ad_search():
    return core_routes.ad_search()


@app.route('/api/v1/boxes/add', methods=['OPTIONS', 'POST'])
def add_boxes():
    return core_routes.add_boxes()


@app.route('/api/v1/boxes/remove', methods=['OPTIONS', 'POST'])
def remove_boxes():
    return {}, 200


@app.route('/api/v1/boxes/get', methods=['OPTIONS', 'POST'])
def get_boxes():
    return core_routes.get_boxes()


@app.route('/api/v1/roles/create', methods=['OPTIONS', 'POST'])
def create_roles():
    return rbac.create_roles()


@app.route('/api/v1/roles/delete', methods=['OPTIONS', 'POST'])
def delete_roles():
    return rbac.delete_roles()


@app.route('/api/v1/roles/assign_perm', methods=['OPTIONS', 'POST'])
def assign_perm():
    return rbac.assign_perm()


@app.route('/api/v1/roles/remove_perm', methods=['OPTIONS', 'POST'])
def remove_perm():
    return rbac.remove_perm()


@app.route('/api/v1/perms/check', methods=['OPTIONS', 'POST'])
def view_perms():
    return check_perms.get_perms()


@app.route('/api/v1/users/add_role', methods=['OPTIONS', 'POST'])
def add_role():
    return rbac.add_role()


@app.route('/api/v1/users/remove_role', methods=['OPTIONS', 'POST'])
def remove_role():
    return rbac.remove_role()


@app.route('/api/v1/users/view_roles', methods=['OPTIONS', 'POST'])
def view_roles():
    return ums_routes.view_roles()


@app.route('/api/v1/login', methods=['OPTIONS', 'POST'])
def login():
    return ums_routes.login()


@app.route('/api/v1/create_user', methods=['OPTIONS', 'POST'])
def create_user():
    return ums_routes.create_user()


@app.route('/api/v1/resetPwd', methods=['OPTIONS', 'POST'])
def resetPwd():
    return ums_routes.resetPwd()


if __name__ == '__main__':
    # app.jinja_env.cache = {}
    app.run(debug=True, host="localhost", port=8888)
