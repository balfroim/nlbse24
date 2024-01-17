import json
import logging
import os
import re
import pandas as pd

def setting_up_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
                        logging.StreamHandler(),
                              logging.FileHandler('codetour-selection.log')
                ]
    )

def load_projects():
    projects = []
    for project_name in ("Chart", "Closure", "Lang", "Math", "Time"):
        for filename in os.listdir('./stacktraces'):
            filename_re = re.compile(r'^' + project_name + r'-\d+\.json$')
            if filename_re.match(filename):
                with open('./stacktraces/' + filename) as f:
                    projects.append(json.load(f))
    return projects

def get_project_failure_reason(project):
    if 'generation_failure' in project:
        reason = project['generation_failure']['error_message']
        if 'codeql database create' in reason:
            reason = 'Failing to create the database'
        if 'defects4j checkout' in reason:
            reason = 'Failing to checkout the project'
        return reason
    return None


def initialize_steps_tours_data():
    return {
        'name': [],
        'version': [],
        'test': [],
        'method': [],
        'order': [],
        'step': [],
        'tour_id': []
    }

def get_tour_failure_reason(tour):
    if 'generation_failure' in tour:
        reason = tour['generation_failure']['error_message']
        if 'No such file or directory' in reason:
            return 'Direct call'
        if 'defects4j test' in reason:
            return 'Failing to run the test'
        if 'codeql database analyze' in reason or reason == 'No columns to parse from file':
            return 'Failing to extract methods'
    return None

def append_step_data(project, tour, step, i_step, i_tour, steps_tours_data):
    steps_tours_data['name'].append(project['project']['name'])
    steps_tours_data['version'].append(project['project']['version'])
    steps_tours_data['test'].append(json.dumps(tour['failing_test']))
    steps_tours_data['method'].append(json.dumps(tour['patched_method']))
    steps_tours_data['order'].append(i_step)
    steps_tours_data['step'].append(json.dumps(step))
    steps_tours_data['tour_id'].append(i_tour)

def add_project_steps_to_data(project, steps_tours_data):
    for i_tour, tour in enumerate(project['tours']):
        reason = get_tour_failure_reason(tour)
        if reason is None:
            for i_step, step in enumerate(tour['steps']):
                append_step_data(project, tour, step, i_step, i_tour, steps_tours_data)

def json_list_to_df(projects):
    """
    Convert the projects the list of json files to a dataframe
    """
    steps_tours_data = initialize_steps_tours_data()
    for project in projects:
        reason = get_project_failure_reason(project)
        if reason is None:
            add_project_steps_to_data(project, steps_tours_data)
    return pd.DataFrame(steps_tours_data)

projects = load_projects()
df_steps_tours = json_list_to_df(projects)
df_steps_tours = df_steps_tours.sort_values(by=['name', 'version', 'tour_id', 'order'])
grouped_tours = df_steps_tours.groupby(['name', 'version', 'tour_id'])
tours_per_project_count = grouped_tours.count().groupby(['name'])
min_length_steps_per_project = tours_per_project_count.quantile(0.25)['order']
min_length_steps_per_project = min_length_steps_per_project.map(lambda x: 3 if x < 3 else x)
max_length_steps_per_project = tours_per_project_count.quantile(0.75)['order']


selected_tours_refined = []
unique_steps_set = set()
unique_step_counts = []
unique_tests_set = set()
unique_methods_set = set()

for tour_id, tour_data in grouped_tours:
    test = tour_data['test'].iloc[0]
    method = tour_data['method'].iloc[0]

    length = len(tour_data['step'])
    is_in_iqr = min_length_steps_per_project[tour_id[0]] <= length <= max_length_steps_per_project[tour_id[0]]
    new_unique_step_counts = 0
    for step in tour_data['step']:
        if step not in unique_steps_set:
            new_unique_step_counts += 1
        unique_steps_set.add(step)
    is_test_method_unique = (test not in unique_tests_set) and (method not in unique_methods_set)
    if is_in_iqr and new_unique_step_counts >= length / 2 and is_test_method_unique:
        selected_tours_refined.append(tour_id)
        unique_steps_set.update(tour_data['step'])
        unique_step_counts.append(new_unique_step_counts)
        unique_tests_set.add(test)
        unique_methods_set.add(method)

df_selected_tours = df_steps_tours.set_index(['name', 'version', 'tour_id']).loc[selected_tours_refined].sort_values(by=['name', 'version', 'tour_id', 'order']).reset_index()
common_attributes = df_selected_tours[['name', 'version', 'tour_id', 'test', 'method']].drop_duplicates()
steps = df_selected_tours.groupby(['name', 'version', 'tour_id'])[['step']].apply(lambda x: x.to_dict(orient='records')).rename('steps')
grouped_tours = common_attributes.join(steps, on=['name', 'version', 'tour_id'])
json_tours = grouped_tours.to_json(orient='records')

with open('selected_tours.json', 'w') as f:
    f.write(json_tours)