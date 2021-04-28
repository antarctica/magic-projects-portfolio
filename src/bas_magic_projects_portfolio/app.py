from os import environ
from typing import Dict, List, Optional, Union

# noinspection PyPackageRequirements
from airtable import Airtable
from bas_style_kit_jinja_templates import BskTemplates
from flask import flash, Flask, redirect, render_template, request, session, url_for
from jinja2 import PackageLoader, PrefixLoader
from msal import ConfidentialClientApplication
from werkzeug import Response
from werkzeug.middleware.proxy_fix import ProxyFix

from bas_magic_projects_portfolio.utils import (
    check_permissions,
    configure_bas_style_kit_templates,
    FlaskResponseType,
    grid_people,
    grid_projects,
    group_people_by_project_roles,
    group_projects,
    index_people,
)

app: Flask = Flask(__name__)

app.config["SESSION_TYPE"]: str = environ.get("SESSION_TYPE")
app.config["BSK_TEMPLATES"]: BskTemplates = configure_bas_style_kit_templates()
app.config["AIRTABLE_KEY"]: str = environ.get("AIRTABLE_KEY")
app.config["AIRTABLE_BASE"]: str = environ.get("AIRTABLE_BASE")
app.config["AUTH_CLIENT_ID"]: str = environ.get("AUTH_CLIENT_ID")
app.config["AUTH_CLIENT_SECRET"]: str = environ.get("AUTH_CLIENT_SECRET")
app.config["AUTH_CLIENT_TENANCY"]: str = environ.get("AUTH_CLIENT_TENANCY")

app.secret_key = str(environ.get("FLASK_SESSION_KEY")).encode()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.jinja_loader = PrefixLoader(
    {
        "app": PackageLoader("bas_magic_projects_portfolio"),
        "bas_style_kit": PackageLoader("bas_style_kit_jinja_templates"),
    }
)

auth: ConfidentialClientApplication = ConfidentialClientApplication(
    client_id=app.config["AUTH_CLIENT_ID"],
    client_credential=app.config["AUTH_CLIENT_SECRET"],
    authority=app.config["AUTH_CLIENT_TENANCY"],
)

airtable_projects = Airtable(
    base_key=app.config["AIRTABLE_BASE"],
    table_name="Projects (V2)",
    api_key=app.config["AIRTABLE_KEY"],
)
airtable_project_links = Airtable(
    base_key=app.config["AIRTABLE_BASE"],
    table_name="Project Links (V2)",
    api_key=app.config["AIRTABLE_KEY"],
)
airtable_project_roles = Airtable(
    base_key=app.config["AIRTABLE_BASE"],
    table_name="Project Roles (V2)",
    api_key=app.config["AIRTABLE_KEY"],
)
airtable_people = Airtable(
    base_key=app.config["AIRTABLE_BASE"],
    table_name="People (V2)",
    api_key=app.config["AIRTABLE_KEY"],
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
    return redirect(url_for("all_projects"))


@app.route("/people")
def all_projects_by_person() -> FlaskResponseType:
    """
    Show people page (authenticated).

    People are loaded from Airtable with projects they have a role in.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Read.All' role.

    :rtype: FlaskResponseType
    :return: Jinja view or redirect
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Read.All"]):
        # noinspection PyUnresolvedReferences
        return render_template("app/views/auth/403-permissions.j2")

    people = airtable_people.get_all()
    roles = airtable_project_roles.get_all()
    projects = airtable_projects.get_all()

    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/people.j2",
        projects=grid_people(people=people, roles=roles, projects=projects),
        user=session.get("user"),
    )


@app.route("/projects/-/group/<string:group_property>")
def all_projects_grouped(group_property: str) -> FlaskResponseType:
    """
    Show all projects grouped by property page (authenticated).

    Projects are loaded from Airtable and grouped by a shared property.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Read.All' role.

    :type group_property: str
    :param group_property: shared property to group projects by
    :rtype: FlaskResponseType
    :return: Jinja view or redirect
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Read.All"]):
        # noinspection PyUnresolvedReferences
        return render_template("app/views/auth/403-permissions.j2")

    projects = airtable_projects.get_all()

    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/projects.j2",
        projects=grid_projects(projects=projects, group_property=group_property),
        projects_total=len(projects),
        group_property=group_property,
        user=session.get("user"),
    )


@app.route("/projects")
def all_projects() -> FlaskResponseType:
    """
    Show all projects page (authenticated).

    Projects are loaded from Airtable.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Read.All' role.

    :rtype: FlaskResponseType
    :return: Jinja view or redirect
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Read.All"]):
        # noinspection PyUnresolvedReferences
        return render_template("app/views/auth/403-permissions.j2")

    group_property: str = "status"
    projects = airtable_projects.get_all()

    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/projects.j2",
        projects=group_projects(projects=projects, group_property=group_property),
        projects_total=len(projects),
        group_property=group_property,
        user=session.get("user"),
    )


@app.route("/projects/add")
def add_project() -> redirect:
    """
    Create new project (authenticated).

    This method is used to enforce permissions checks, if ok the user is redirected to an Airtable form.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Write.All' role.

    :rtype: redirect
    :return: Redirect to either Airtable form or permissions error page
    """
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Write.All"]):
        flash("You do not have permission to add projects", "danger")
        return redirect(url_for("all_projects"))

    return redirect("https://airtable.com/shraeffFV5201B3zn")


@app.route("/projects/<string:project_id>/-/delete")
def delete_project(project_id: str) -> redirect:
    """
    Delete a project specified by its ID (authenticated).

    Then redirect the user back to the list of all projects.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Write.All' role.

    :type project_id: str
    :param project_id: ID of project to delete
    :rtype: redirect
    :return: Redirect back to all projects list
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))

    project = airtable_projects.get(record_id=project_id)

    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Write.All"]):
        flash("You do not have permission to remove projects", "danger")
        return redirect(url_for("single_project", project_id=project["id"]))

    airtable_projects.delete(record_id=project_id)
    flash(f"Project '{project['fields']['Title']}' removed successfully", "success")
    return redirect(url_for("all_projects"))


@app.route("/project-roles/<string:project_id>/add")
def add_project_role(project_id: str) -> redirect:
    """
    Create new project role (authenticated).

    This method is used to enforce permissions checks, if ok the user is redirected to an Airtable form.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Write.All' role.

    :type project_id: str
    :param project_id: ID of project to associate role with
    :rtype: redirect
    :return: Redirect to either Airtable form or permissions error page
    """
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Write.All"]):
        flash("You do not have permission to add project links", "danger")
        return redirect(url_for("single_project", project_id=project_id))

    return redirect("https://airtable.com/shrCpNmLYlDaOdvSP")


@app.route("/project-links/<string:project_id>/add")
def add_project_link(project_id: str) -> redirect:
    """
    Create new project link (authenticated).

    This method is used to enforce permissions checks, if ok the user is redirected to an Airtable form.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Write.All' role.

    :type project_id: str
    :param project_id: ID of project to associate link with
    :rtype: redirect
    :return: Redirect to either Airtable form or permissions error page
    """
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Write.All"]):
        flash("You do not have permission to add project links", "danger")
        return redirect(url_for("single_project", project_id=project_id))

    return redirect("https://airtable.com/shruPZLCOJwSNRk1t")


@app.route("/project-links/<string:link_id>/-/delete")
def delete_project_link(link_id: str) -> redirect:
    """
    Delete a project link specified by its ID (authenticated).

    Then redirect the user back to the project the project link belonged to.

    Requires the 'BAS.MAGIC.Portfolio.Projects.Write.All' role.

    :type link_id: str
    :param link_id: ID of project link to delete
    :rtype: redirect
    :return: Redirect back to project link belonged to
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))

    link = airtable_project_links.get(record_id=link_id)
    project = airtable_projects.get(record_id=link["fields"]["Project"][0])

    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Write.All"]):
        flash("You do not have permission to remove project links", "danger")
        return redirect(url_for("single_project", project_id=project["id"]))

    airtable_project_links.delete(record_id=link_id)
    flash(f"Link '{link['fields']['Title']}' removed successfully", "success")
    # noinspection PyUnresolvedReferences
    return redirect(url_for("single_project", project_id=project["id"]))


@app.route("/projects/<string:project_id>")
def single_project(project_id: str) -> FlaskResponseType:
    """
    Show details for a specific project specified by its ID (authenticated).

    Requires the 'BAS.MAGIC.Portfolio.Projects.Read.All' role.

    :type project_id: str
    :param project_id: ID of project to display
    :rtype: FlaskResponseType
    :return: Jinja view or redirect
    """
    if not session.get("user"):
        return redirect(url_for("auth_sign_in"))
    if not check_permissions(required_roles=["BAS.MAGIC.Portfolio.Projects.Read.All"]):
        # noinspection PyUnresolvedReferences
        return render_template("app/views/auth/403-permissions.j2")

    project = airtable_projects.get(record_id=project_id)
    project_links = airtable_project_links.search(
        field_name="Project", field_value=project["fields"]["Title"]
    )
    project_roles = airtable_project_roles.search(
        field_name="Project", field_value=project["fields"]["Title"]
    )
    people_indexed = index_people(people=airtable_people.get_all())
    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/project.j2",
        project=project,
        project_links=project_links,
        project_roles=group_people_by_project_roles(
            roles=project_roles, people=people_indexed
        ),
        user=session.get("user"),
    )


@app.route("/legal/cookies")
def legal_cookies() -> FlaskResponseType:
    """
    Show cookies policy page (unauthenticated).

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/cookies.j2")


@app.route("/legal/copyright")
def legal_copyright() -> FlaskResponseType:
    """
    Show copyright notice page (unauthenticated).

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/copyright.j2")


@app.route("/legal/privacy")
def legal_privacy() -> FlaskResponseType:
    """
    Show privacy policy page (unauthenticated).

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    # noinspection PyUnresolvedReferences
    return render_template("app/views/legal/privacy.j2")


@app.route("/auth/sign-in")
def auth_sign_in() -> FlaskResponseType:
    """
    Start sign in process by displaying link to an OAuth login URI.

    The MSAL library is used to construct the OAuth request URI, which is then displayed using the
    'sign in to continue' BAS Style Kit page pattern.

    This represents stage 1 of the 3-legged OAuth authorisation code flow.

    :rtype: FlaskResponseType
    :return: Jinja view
    """
    session["auth_code_flow"]: dict = auth.initiate_auth_code_flow(
        scopes=[],
        redirect_uri=url_for("auth_callback", _external=True),
    )
    # noinspection PyUnresolvedReferences
    return render_template(
        "app/views/auth/sign-in.j2",
        call_to_action_href=session.get("auth_code_flow")["auth_uri"],
    )


@app.route("/auth/sign-out")
def auth_sign_out() -> redirect:
    """
    Sign out current user by destroying their session.

    Then redirect the user back to the application homepage.

    :rtype: redirect
    :return: redirect to app homepage
    """
    session.clear()
    return redirect(url_for("index"))


@app.route("/auth/callback")
def auth_callback() -> FlaskResponseType:
    """
    Complete sign in process by checking OAuth login response.

    The MSAL library is used for verifying based response from the OAuth provider and previously stored information
    from the `auth_sign_in` method, stored in the current session under the 'auth_code_flow' key.

    Once verified, the claims contained in the ID token are stored in the current session under the 'user' key. These
    are used to enforce permissions via the 'roles' claim, and for displaying the name/email of the active user. The
    user is then redirected back to the application homepage.

    Where an error occurs processing the response from the OAuth provider, or where the provider returns an error, the
    user is redirected to an error page.

    This represents stage 3 of the 3-legged OAuth authorisation code flow, where stage 2 is performed within the OAuth
    provider, in this case Microsoft Azure.

    :rtype: FlaskResponseType
    :return: Jinja view or redirect
    """
    try:
        result = auth.acquire_token_by_auth_code_flow(
            auth_code_flow=session.get("auth_code_flow"),
            auth_response=request.args,
            scopes=[],
        )
        if "error" in result:
            if "error_uri" in result and "error?code=50105" in result["error_uri"]:
                # noinspection PyUnresolvedReferences
                return render_template("app/views/auth/403-access.j2")

            # noinspection PyUnresolvedReferences
            return render_template(
                "app/views/auth/403.j2",
                error=result.get("error"),
                description=result.get("error_description"),
                correlation_id=result.get("correlation_id"),
            )

        id_token_claims: Optional[Dict[str, Union[str, List[str]]]] = result.get(
            "id_token_claims"
        )
        session["user"] = id_token_claims
        return redirect(url_for("index"))
    except ValueError as e:
        # noinspection PyUnresolvedReferences
        return render_template(
            "app/views/auth/403.j2",
            error=str(e),
        )
