import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import read_file_without_extension, create_markdown_file
from kringlecraft.utils.misc_tools import get_markdown, get_raw_markdown

blueprint = flask.Blueprint('report', __name__, template_folder='templates')


# Sitemap page
@blueprint.route('/sitemap.xml', methods=['GET'])
def sitemap():
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    # (2) initialize form data
    class SitemapURL:
        def __init__(self, loc, lastmod, changefreq):
            self.loc = loc
            self.lastmod = lastmod
            self.changefreq = changefreq

    all_urls = list()
    www_server = flask.current_app.config.get('app.www_server')
    sitemap_date = flask.current_app.config.get('app.date')
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    all_urls.append(SitemapURL(www_server + flask.url_for("home.index"), sitemap_date, MONTHLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("account.profile_create"), sitemap_date, YEARLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("home.login"), sitemap_date, YEARLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("home.password"), sitemap_date, YEARLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("home.privacy"), sitemap_date, YEARLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("home.release"), sitemap_date, WEEKLY))
    all_urls.append(SitemapURL(www_server + flask.url_for("data.stats"), sitemap_date, WEEKLY))

    all_urls.append(SitemapURL(www_server + flask.url_for("data.worlds"), sitemap_date, WEEKLY))
    all_worlds = world_services.find_all_worlds()
    for world in all_worlds:
        all_urls.append(SitemapURL(www_server + flask.url_for("data.world", world_id=world.id), sitemap_date, WEEKLY))
        all_urls.append(SitemapURL(www_server + flask.url_for("data.rooms", world_id=world.id), sitemap_date, WEEKLY))
        all_rooms = room_services.find_world_rooms(world.id)
        for room in all_rooms:
            all_urls.append(SitemapURL(www_server + flask.url_for("data.room", room_id=room.id), sitemap_date, WEEKLY))
            all_urls.append(SitemapURL(www_server + flask.url_for("data.objectives", room_id=room.id), sitemap_date, WEEKLY))
            all_objectives = objective_services.find_room_objectives(room.id)
            for objective in all_objectives:
                all_urls.append(SitemapURL(www_server + flask.url_for("data.objective", objective_id=objective.id), sitemap_date, WEEKLY))

    # (6a) show rendered page
    template = flask.render_template('report/sitemap.xml', urls=all_urls)
    response = flask.make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


# Show a report containing information about a specific objective and its solution in different formats
@blueprint.route('/single/<string:report_format>/<int:objective_id>', methods=['GET'])
@login_required
def single(report_format, objective_id):
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    objective_image = read_file_without_extension("objective", my_objective.id)
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    # (6a) show rendered page
    if report_format == "html":
        html_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)
        html_solution = "" if (solution_services.find_objective_solution_for_user(objective_id, current_user.id) is
                               None) else get_markdown(solution_services.find_objective_solution_for_user(objective_id, current_user.id).notes)

        return flask.render_template('report/single.html', objective=my_objective,
                                     objective_image=objective_image, room=my_room, world=my_world,
                                     objective_types=objective_services.get_objective_types(),
                                     html_challenge=html_challenge, html_solution=html_solution)

    if report_format == "markdown":
        md_challenge = "" if my_objective.challenge is None else get_raw_markdown(my_objective.challenge)
        md_solution = "" if (solution_services.find_objective_solution_for_user(objective_id, current_user.id) is
                               None) else get_raw_markdown(
            solution_services.find_objective_solution_for_user(objective_id, current_user.id).notes)

        md_output = flask.render_template('report/single.md', objective=my_objective,
                                          objective_image=objective_image, room=my_room, world=my_world,
                                          objective_types=objective_services.get_objective_types(),
                                          md_challenge=md_challenge, md_solution=md_solution,
                                          www_server=flask.current_app.config.get('app.www_server'),)
        local_file = create_markdown_file(f"objective-{my_objective.id}.md", md_output)

        return flask.send_file(local_file, download_name=f"objective-{my_objective.id}.md", as_attachment=True)