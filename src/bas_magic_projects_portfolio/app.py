from os import environ

from flask import Flask, render_template, redirect, url_for, flash
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader
from bas_style_kit_jinja_templates import BskTemplates
# noinspection PyPackageRequirements
from airtable import Airtable

app = Flask(__name__)
app.secret_key = str(environ.get('FLASK_SESSION_KEY')).encode()

app.jinja_loader = PrefixLoader({
    'app': FileSystemLoader('templates'),
    'bas_style_kit': PackageLoader('bas_style_kit_jinja_templates'),
})
app.config['BSK_TEMPLATES'] = BskTemplates()
app.config['BSK_TEMPLATES'].site_title = 'MAGIC Projects Portfolio'
app.config['BSK_TEMPLATES'].site_description = 'Portfolio of projects undertaken, or planned to be undertaken, by ' \
                                               'the BAS Mapping and Geographic Information Centre (MAGIC)'
app.config['BSK_TEMPLATES'].bsk_site_nav_brand_text = 'MAGIC Projects Portfolio'
app.config['BSK_TEMPLATES'].bsk_site_development_phase = 'alpha'
app.config['BSK_TEMPLATES'].bsk_site_feedback_href = 'https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/' \
                                                     'issues/new'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_cookies_href = '/legal/cookies'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_copyright_href = '/legal/copyright'
app.config['BSK_TEMPLATES'].bsk_site_footer_policies_privacy_href = '/legal/privacy'
app.config['BSK_TEMPLATES'].site_styles.append({'href': '/static/css/app.css'})
app.config['BSK_TEMPLATES'].site_styles.append({
    "href": "https://cdn.web.bas.ac.uk/libs/font-awesome-pro/5.13.0/css/all.min.css",
    "integrity": "sha256-DjbUjEiuM4tczO997cVF1zbf91BC9OzycscGGk/ZKks="
})

app.config['BSK_TEMPLATES'].bsk_container_classes = ['bsk-container-fluid']
app.config['BSK_TEMPLATES'].bsk_site_nav_launcher.append({
    'value': 'MAGIC Team (BAS Digital Workspace)',
    'href': 'https://nercacuk.sharepoint.com/sites/BASDigitalw/people-teams/magic/Pages/default.aspx'
})
app.config['BSK_TEMPLATES'].bsk_site_nav_launcher.append({
    'value': 'MAGIC Team (BAS Public Website)',
    'href': 'https://www.bas.ac.uk/team/magic'
})

app.config['airtable_key'] = environ.get('AIRTABLE_KEY', None)
app.config['airtable_base'] = environ.get('AIRTABLE_BASE', None)

airtable_projects = Airtable(
    base_key=app.config['airtable_base'],
    table_name='Projects',
    api_key=app.config['airtable_key']
)
airtable_project_links = Airtable(
    base_key=app.config['airtable_base'],
    table_name='Project Links',
    api_key=app.config['airtable_key']
)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(e):
    # noinspection PyUnresolvedReferences
    return render_template('app/views/404.j2'), 404


@app.route('/')
def index():
    return redirect(url_for('projects', group_property="strategic-objectives"))


@app.route('/projects/-/group/<string:group_property>')
def all_projects(group_property: str):
    projects = airtable_projects.get_all()
    # noinspection PyUnresolvedReferences
    return render_template(
        f"app/views/index.j2",
        projects=_group_projects(projects=projects, group_property=group_property),
        projects_total=len(projects),
        group_property=group_property
    )


@app.route('/projects/<string:project_id>/-/delete')
def delete_project(project_id: str):
    project = airtable_projects.get(record_id=project_id)
    airtable_projects.delete(record_id=project_id)
    flash(f"Project '{project['fields']['Title']}' removed successfully", "success")
    # noinspection PyUnresolvedReferences
    return redirect(url_for('projects', group_property="strategic-objectives"))


@app.route('/project-links/<string:link_id>/-/delete')
def delete_project_link(link_id: str):
    link = airtable_project_links.get(record_id=link_id)
    project = airtable_projects.get(record_id=link['fields']['Project'][0])
    airtable_project_links.delete(record_id=link_id)
    flash(f"Link '{link['fields']['Title']}' removed successfully", "success")
    # noinspection PyUnresolvedReferences
    return redirect(url_for('project', project_id=project['id']))


@app.route('/projects/<string:project_id>')
def single_project(project_id: str):
    project = airtable_projects.get(record_id=project_id)
    project_links = airtable_project_links.search(field_name='Project', field_value=project['fields']['Title'])
    # noinspection PyUnresolvedReferences
    return render_template(f"app/views/project.j2", project=project, project_links=project_links)


@app.route('/legal/cookies')
def legal_cookies():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/views/legal/cookies.j2")


@app.route('/legal/copyright')
def legal_copyright():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/views/legal/copyright.j2")


@app.route('/legal/privacy')
def legal_privacy():
    # noinspection PyUnresolvedReferences
    return render_template(f"app/views/legal/privacy.j2")


def _group_projects(projects: list, group_property: str) -> dict:
    group_properties = {
        "strategic-objectives": "Strategic Objectives",
        "activity-areas": "Activity Areas",
        "project-lead": "Owner"
    }
    grouped_projects = {'none': []}

    for project in projects:
        # current_app.logger.warning(project['fields'].keys())
        try:
            if isinstance(project['fields'][group_properties[group_property]], str):
                if project['fields'][group_properties[group_property]] not in grouped_projects.keys():
                    grouped_projects[project['fields'][group_properties[group_property]]] = []
                grouped_projects[project['fields'][group_properties[group_property]]].append(project)
                continue

            for group_property_value in project['fields'][group_properties[group_property]]:
                if group_property_value not in grouped_projects.keys():
                    grouped_projects[group_property_value] = []
                grouped_projects[group_property_value].append(project)
        except KeyError:
            grouped_projects['none'].append(project)

    return grouped_projects
