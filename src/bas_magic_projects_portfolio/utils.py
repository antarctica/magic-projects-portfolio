import typing as t

from bas_style_kit_jinja_templates import BskTemplates
from werkzeug.datastructures import Headers
from werkzeug.wrappers import BaseResponse


"""
Python type for Flask responses
Source: https://stackoverflow.com/a/58866777
"""
_str_bytes = t.Union[str, bytes]
_data_type = t.Union[
    _str_bytes,
    BaseResponse,
    t.Dict[str, t.Any],
    t.Callable[
        [t.Dict[str, t.Any], t.Callable[[str, t.List[t.Tuple[str, str]]], None]],
        t.Iterable[bytes],
    ],
]
_status_type = t.Union[int, _str_bytes]
_headers_type = t.Union[
    Headers,
    t.Dict[_str_bytes, _str_bytes],
    t.Iterable[t.Tuple[_str_bytes, _str_bytes]],
]

FlaskResponseType = t.Union[
    _data_type,
    t.Tuple[_data_type],
    t.Tuple[_data_type, _status_type],
    t.Tuple[_data_type, _headers_type],
    t.Tuple[_data_type, _status_type, _headers_type],
]


def configure_bas_style_kit_templates() -> BskTemplates:
    """
    Configure BAS Style Kit Jinja Templates object for application.

    :rtype: BskTemplates
    :return: BAS Style Kit templates configuration
    """
    bsk_templates = BskTemplates()
    bsk_templates.site_title = "MAGIC Projects Portfolio"
    bsk_templates.site_description = (
        "Portfolio of projects undertaken, or planned to be undertaken, by "
        "the BAS Mapping and Geographic Information Centre (MAGIC)"
    )
    bsk_templates.bsk_site_nav_brand_text = "MAGIC Projects Portfolio"
    bsk_templates.bsk_site_development_phase = "alpha"
    bsk_templates.bsk_site_feedback_href = (
        "https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/" "issues/new"
    )
    bsk_templates.bsk_site_footer_policies_cookies_href = "/legal/cookies"
    bsk_templates.bsk_site_footer_policies_copyright_href = "/legal/copyright"
    bsk_templates.bsk_site_footer_policies_privacy_href = "/legal/privacy"
    bsk_templates.site_styles.append({"href": "/static/css/app.css"})
    bsk_templates.site_styles.append(
        {
            "href": "https://cdn.web.bas.ac.uk/libs/font-awesome-pro/5.13.0/css/all.min.css",
            "integrity": "sha256-DjbUjEiuM4tczO997cVF1zbf91BC9OzycscGGk/ZKks=",
        }
    )

    bsk_templates.bsk_container_classes = ["bsk-container-fluid"]
    bsk_templates.bsk_site_nav_launcher.append(
        {
            "value": "MAGIC Team (BAS Digital Workspace)",
            "href": "https://nercacuk.sharepoint.com/sites/BASDigitalw/people-teams/magic/Pages/default.aspx",
        }
    )
    bsk_templates.bsk_site_nav_launcher.append(
        {
            "value": "MAGIC Team (BAS Public Website)",
            "href": "https://www.bas.ac.uk/team/magic",
        }
    )

    return bsk_templates


def group_projects(projects: list, group_property: str) -> dict:
    """
    Group a set of projects by a common property.

    :type projects: list
    :param projects: collection of projects to group
    :type group_property: str
    :param group_property: property to group projects by
    :rtype: dict
    :return: projects grouped by common property
    """
    group_properties = {
        "strategic-objectives": "Strategic Objectives",
        "activity-areas": "Activity Areas",
    }
    grouped_projects = {"none": []}

    for project in projects:
        try:
            if isinstance(project["fields"][group_properties[group_property]], str):
                if (
                    project["fields"][group_properties[group_property]]
                    not in grouped_projects.keys()
                ):
                    grouped_projects[
                        project["fields"][group_properties[group_property]]
                    ] = []
                grouped_projects[
                    project["fields"][group_properties[group_property]]
                ].append(project)
                continue

            for group_property_value in project["fields"][
                group_properties[group_property]
            ]:
                if group_property_value not in grouped_projects.keys():
                    grouped_projects[group_property_value] = []
                grouped_projects[group_property_value].append(project)
        except KeyError:
            grouped_projects["none"].append(project)

    return grouped_projects
