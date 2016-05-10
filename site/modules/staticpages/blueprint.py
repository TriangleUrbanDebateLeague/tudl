from flask import Blueprint, render_template, make_response

staticpages = Blueprint("staticpages", __name__, template_folder="templates", url_prefix="")

@staticpages.route("/", defaults={"page": "index"})
@staticpages.route("/<page>/")
def show_staticpage(page):
    try:
        return render_template("{}.html".format(page))
    except:
        return make_response(render_template("not_found.html"), 404)
