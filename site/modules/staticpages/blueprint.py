from flask import Blueprint, render_template, make_response

staticpages = Blueprint("staticpages", __name__, template_folder="templates", url_prefix="")

@staticpages.route("/", defaults={"page": "index"})
@staticpages.route("/<page>/")
def show_staticpage(page):
    return render_template("{}.html".format(page))
