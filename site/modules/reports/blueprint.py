from .localutils import get_all_reports, get_report
from flask import Blueprint, abort, render_template
from modules.security.decorators import require_permission

reports = Blueprint("reports", __name__, template_folder="templates", url_prefix="/reports")

@reports.route("/")
@require_permission("reports", "run")
def reports_index():
    return render_template("reports/all.html", all_reports=get_all_reports())

@reports.route("/<module>/<report>/")
@require_permission("reports", "run")
def run(module, report):
    report_instance = get_report(module, report)
    if not report_instance:
        abort(404)

    return render_template("reports/report.html", report=report_instance)
