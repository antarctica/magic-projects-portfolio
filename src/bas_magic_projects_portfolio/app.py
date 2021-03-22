from os import environ

# noinspection PyPackageRequirements
from airtable import Airtable
from flask import flash, Flask, redirect, render_template, url_for
from jinja2 import FileSystemLoader, PackageLoader, PrefixLoader
from werkzeug import Response

from bas_magic_projects_portfolio.utils import (
    configure_bas_style_kit_templates,
    FlaskResponseType,
    group_projects,
)


app = Flask(__name__)
app.secret_key = str(environ.get("FLASK_SESSION_KEY")).encode()

app.jinja_loader = PrefixLoader(
    {
        "app": FileSystemLoader("templates"),
        "bas_style_kit": PackageLoader("bas_style_kit_jinja_templates"),
    }
)
app.config["BSK_TEMPLATES"] = configure_bas_style_kit_templates()

app.config["airtable_key"] = environ.get("AIRTABLE_KEY", None)
app.config["airtable_base"] = environ.get("AIRTABLE_BASE", None)

airtable_projects = Airtable(
    base_key=app.config["airtable_base"],
    table_name="Projects",
    api_key=app.config["airtable_key"],
)
airtable_project_links = Airtable(
    base_key=app.config["airtable_base"],
    table_name="Project Links",
    api_key=app.config["airtable_key"],
)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(e: Exception) -> FlaskResponseType:
    """
    Show 404 error page.

    :type e: Exception
    :param e: Exception that has caused error
    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/404.j2"), 404


@app.route("/")
def index() -> Response:
    """
    Redirect the user to the all projects view with a default grouping property.

    :rtype: Response
    :return: Redirect back to all projects list
    """
    return redirect(url_for("all_projects", group_property="strategic-objectives"))


@app.route("/projects/-/group/<string:group_property>")
def all_projects(group_property: str) -> FlaskResponseType:
    """
    Show all projects page.

    Projects are loaded from Airtable and grouped by a shared property.

    :type group_property: str
    :param group_property: shared property to group projects by
    :rtype: FlaskResponseType
    :return: Jinja view
    """
    projects = airtable_projects.get_all()
    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/index.j2",
        projects=group_projects(projects=projects, group_property=group_property),
        projects_total=len(projects),
        group_property=group_property,
    )


@app.route("/projects/<string:project_id>/-/delete")
def delete_project(project_id: str) -> Response:
    """
    Delete a project specified by its ID.

    Then redirect the user back to the list of all projects.

    :type project_id: str
    :param project_id: ID of project to delete
    :rtype: Response
    :return: Redirect back to all projects list
    """
    project = airtable_projects.get(record_id=project_id)
    airtable_projects.delete(record_id=project_id)
    flash(f"Project '{project['fields']['Title']}' removed successfully", "success")
    # noinspection PyUnresolvedReferences
    return redirect(url_for("all_projects", group_property="strategic-objectives"))


@app.route("/project-links/<string:link_id>/-/delete")
def delete_project_link(link_id: str) -> Response:
    """
    Delete a project link specified by its ID.

    Then redirect the user back to the project the project link belonged to.

    :type link_id: str
    :param link_id: ID of project link to delete
    :rtype: Response
    :return: Redirect back to project link belonged to
    """
    link = airtable_project_links.get(record_id=link_id)
    project = airtable_projects.get(record_id=link["fields"]["Project"][0])
    airtable_project_links.delete(record_id=link_id)
    flash(f"Link '{link['fields']['Title']}' removed successfully", "success")
    # noinspection PyUnresolvedReferences
    return redirect(url_for("single_project", project_id=project["id"]))


@app.route("/projects/<string:project_id>")
def single_project(project_id: str) -> FlaskResponseType:
    """
    Show details for a specific project specified by its ID.

    :type project_id: str
    :param project_id: ID of project to display
    :rtype: FlaskResponseType
    :return: Jinja view
    """
    project = airtable_projects.get(record_id=project_id)
    project_links = airtable_project_links.search(
        field_name="Project", field_value=project["fields"]["Title"]
    )
    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/project.j2", project=project, project_links=project_links
    )


@app.route("/legal/cookies")
def legal_cookies() -> FlaskResponseType:
    """
    Show cookies policy page.

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/cookies.j2")


@app.route("/legal/copyright")
def legal_copyright() -> FlaskResponseType:
    """
    Show copyright notice page.

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/copyright.j2")


@app.route("/legal/privacy")
def legal_privacy() -> FlaskResponseType:
    """
    Show privacy policy page.

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/privacy.j2")
