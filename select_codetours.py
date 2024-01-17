import json
import logging
import os
import re
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
                        logging.StreamHandler(),
                              logging.FileHandler('analyse-stacktraces.log')
                ]
)

projects = []

for project_name in ("Chart", "Closure", "Lang", "Math", "Time"):
    for filename in os.listdir('./stacktraces'):
        filename_re = re.compile(r'^' + project_name + r'-\d+\.json$')
        if filename_re.match(filename):
            with open('./stacktraces/' + filename) as f:
                projects.append(json.load(f))

steps_tours = {
    'name': [],
    'version': [],
    'test': [],
    'method': [],
    'order': [],
    'step': [],
    'tour_id': []
}

for project in projects:
    if 'generation_failure' in project:
        reason = project['generation_failure']['error_message']
        if 'codeql database create' in reason:
            reason = 'Failing to create the database'
        if 'defects4j checkout' in reason:
            reason = 'Failing to checkout the project'
    else:
        for i_tour, tour in enumerate(project['tours']):
            if 'generation_failure' in tour:
                reason = tour['generation_failure']['error_message']
                if 'No such file or directory' in reason:
                    reason = 'Direct call'
                if 'defects4j test' in reason:
                    reason = 'Failing to run the test'
                if 'codeql database analyze' in reason or reason == 'No columns to parse from file':
                    reason = 'Failing to extract methods'
            else:
                for i_step, step in enumerate(tour['steps']):
                    steps_tours['name'].append(project['project']['name'])
                    steps_tours['version'].append(project['project']['version'])
                    steps_tours['test'].append(json.dumps(tour['failing_test']))
                    steps_tours['method'].append(json.dumps(tour['patched_method']))
                    steps_tours['order'].append(i_step)
                    steps_tours['step'].append(json.dumps(step))
                    steps_tours['tour_id'].append(i_tour)

df_steps_tours = pd.DataFrame(steps_tours)

df_steps_tours = df_steps_tours.sort_values(by=['name', 'version', 'tour_id', 'order'])


grouped_tours = df_steps_tours.groupby(['name', 'version', 'tour_id'])

tours_per_project_count = grouped_tours.count().groupby(['name'])

tours_per_project_count_describe = tours_per_project_count['order'].describe()

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

tours_per_project_count = pd.DataFrame(selected_tours_refined, columns=['name', 'version', 'tour_id']).groupby('name').size().sort_values(ascending=False)

print(tours_per_project_count.sum())

common_attributes = df_selected_tours[['name', 'version', 'tour_id', 'test', 'method']].drop_duplicates()
steps = df_selected_tours.groupby(['name', 'version', 'tour_id'])[['step']].apply(lambda x: x.to_dict(orient='records')).rename('steps')
grouped_tours = common_attributes.join(steps, on=['name', 'version', 'tour_id'])
json_tours = grouped_tours.to_json(orient='records')

with open('selected_tours.json', 'w') as f:
    f.write(json_tours)