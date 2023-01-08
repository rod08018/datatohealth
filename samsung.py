import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def clean_table_data(table, key):
    time_list = [
        'create_time',
        'update_time',
        'start_time',
        'end_time',
        'day_time',
        'Time of Measurement',
        'original_wake_up_time',
        'original_bed_time'
    ]
    table.fillna(0, inplace=True)
    for field in time_list:
        for column in table.columns:
            if field in column:
                table[column] = pd.to_datetime(table[column])
                if 'date' not in table.columns:
                    table['date'] = table[column].dt.date
    if 'activity_day_summary' in key:
        table.drop(['day_time'], axis=1, inplace=True)
        table['walk_time'] = (table['walk_time'] / 60000).round(2)
        table['longest_idle_time'] = (table['longest_idle_time'] / 60000).round(2)
        table['run_time'] = (table['run_time'] / 60000).round(2)
        print(table.columns)
        table = table.groupby([table['date']]).mean().round(2)

        return table
    elif 'calories_burned_details' in key:
        table['calories_burned.update_time'] = pd.to_datetime(table['calories_burned.update_time'])
        calories_table_list = [column for column in table.columns if column not in ['version', 'active_calories_goal']]
        return table[
            calories_table_list
        ]
    elif 'exercise' in key:
        exercise_table_list = [column for column in table.columns if column not in
                               [
                                   'exercise.update_time',
                                   'exercise.mean_caloricburn_rate',
                                   'live_data_internal',
                                   'sensing_status',
                                   'exercise.additional',
                                   'exercise.location_data',
                                   'exercise.custom',
                                   'exercise.mean_rpm',
                                   'exercise.count_type',
                                   'exercise.min_altitude',
                                   'exercise.max_power',
                                   'reward_status',
                                   'exercise.count_type',
                                   'exercise.decline_distance',
                                   'exercise.deviceuuid',
                                   'exercise.time_offset',
                                   'exercise.max_rpm',
                                   'exercise.comment',
                                   'exercise.live_data',
                                   'exercise.pkg_name',
                                   'exercise.mean_power',
                                   'exercise.altitude_gain',
                                   'exercise.altitude_loss',
                                   'exercise.exercise_custom_type',
                                   'exercise.sweat_loss',
                                   'exercise.datauuid',
                               ]
                               ]
        return table[
            exercise_table_list
        ]
    elif 'food_info' in key:
        food_info_table_list = [column for column in table.columns if column not in
                                [
                                    'provider_food_id',
                                    'info_provider',
                                ]
                                ]
        return table[
            food_info_table_list
        ]
    elif 'food_intake' in key:
        food_intake_table_list = [column for column in table.columns if column not in
                                  [
                                      'food_info_id',
                                      'unit',
                                  ]
                                  ]
        return table[
            food_intake_table_list
        ]
    elif 'nutrition' in key:

        nutrition_intake_table_list = [column for column in table.columns if column not in
                                       [
                                           'food_info_id',
                                           'unit',
                                       ]
                                       ]
        return table[
            nutrition_intake_table_list
        ]
    elif 'scale_data' in key:

        scale_data_table_list = [column for column in table.columns if column not in
                                 [
                                     'Remarks',
                                     'user_id',
                                 ]
                                 ]
        return table[
            scale_data_table_list
        ]
    elif 'sleep' in key:

        sleep_table_list = [column for column in table.columns if column not in
                            [
                                'original_efficiency',
                                'factor_01',
                                'factor_02',
                                'factor_03',
                                'factor_04',
                                'factor_05',
                                'factor_06',
                                'factor_07',
                                'factor_08',
                                'factor_09',
                                'factor_10',
                                'has_sleep_data',
                                'combined_id',
                                'quality',
                                'sleep.custom',
                                'sleep.time_offset',

                            ]
                            ]
        return table[
            sleep_table_list
        ]
    elif 'sleep_combined' in key:

        sleep_combined_table_list = [column for column in table.columns if column not in
                                     [
                                         'original_efficiency',
                                         'factor_01',
                                         'factor_02',
                                         'factor_03',
                                         'factor_04',
                                         'factor_05',
                                         'factor_06',
                                         'factor_07',
                                         'factor_08',
                                         'factor_09',
                                         'factor_10',
                                         'has_sleep_data',
                                         'combined_id',
                                         'quality',
                                         'sleep.custom',
                                         'sleep.time_offset',

                                     ]
                                     ]
        return table[
            sleep_combined_table_list
        ]
    elif 'sleep_stage' in key:
        return table
    elif 'sleep_stages_mapping' in key:
        return table
    elif 'step_daily_trend' in key:
        return table
    elif 'stress' in key:
        return table

    elif 'tracker_heart_rate' in key:

        hr_table_list = [column for column in table.columns if column not in
                         [
                             'heart_rate.custom',
                             'heart_rate.binning_data',
                             'heart_rate.heart_beat_count',
                             'heart_rate.deviceuuid',
                             'heart_rate.time_offset',
                             'heart_rate.comment',
                             'heart_rate.pkg_name',
                             'heart_rate.datauuid',
                             'heart_rate.max',
                             'heart_rate.min'
                         ]
                         ]
        return table[
            hr_table_list
        ]
    elif 'tracker_oxygen_saturation' in key:

        oxigen_saturation_table_list = [column for column in table.columns if column not in
                                        [
                                            'oxygen_saturation.custom',
                                            'oxygen_saturation.binning',
                                            'oxygen_saturation.time_offset',
                                            'oxygen_saturation.deviceuuid',
                                            'oxygen_saturation.comment',
                                            'oxygen_saturation.pkg_name',
                                            'oxygen_saturation.datauuid',
                                        ]
                                        ]
        return table[
            oxigen_saturation_table_list
        ]
    elif 'tracker_pedometer_step_count' in key:

        scale_data_table_list = [column for column in table.columns if column not in
                                 [
                                     'step_count.time_offset'
                                 ]
                                 ]
        return table[
            scale_data_table_list
        ]
    elif 'weight' in key:

        weight_table_list = [column for column in table.columns if column not in
                             [
                                 'pkg_name',
                                 'datauuid',
                                 'vfa_level',
                                 'comment',
                                 'time_offset',
                                 'deviceuuid',
                                 'custom',
                             ]
                             ]
        table['weight'] = table['weight'] * 2.20462
        table['fat_free_mass'] = table['fat_free_mass'] * 2.20462
        table = table[table['height'] != 0]
        return table[
            weight_table_list
        ]


def merge_all_data(tables_dict: dict):
    # food merger
    food_info_table = tables_dict['food_info']
    food_info_table = food_info_table.drop(['calorie'], axis=1)
    food_intake_table = tables_dict['food_intake']
    general_food_table = food_info_table.merge(right=food_intake_table, on=['name'], how='right')

    general_food_table = general_food_table.drop(
        columns=['metric_serving_unit', 'serving_description', 'name', 'description'],
        axis=1,
    )

    general_food_table['start_time'] = pd.to_datetime(general_food_table['start_time'])

    general_food_table = general_food_table.resample('W-MON', on='start_time').mean().reset_index()

    general_food_table.sort_values(by=['start_time'], ascending=False, inplace=True)
    tables_dict['general_food_table'] = general_food_table
    del tables_dict['food_info']
    del tables_dict['food_intake']
    del tables_dict['preferences']
    del tables_dict['stress_histogram']
    tables_dict = tables_dict.copy()
    tables_dict['daily_report'] = tables_dict[list(tables_dict.keys())[0]]
    print('1', list(tables_dict.keys())[0])

    for table in [

        'weight',
        'tracker_pedometer_step_count',
        'tracker_heart_rate',
        'tracker_oxygen_saturation',
        'sleep',
        'exercise'
    ]:
        if not table == list(tables_dict.keys())[0]:

            column_list = [column for column in tables_dict[table].columns if 'time' not in column]

            to_be_merged = pd.DataFrame(tables_dict[table].groupby('date').mean().round(2))

            tables_dict['daily_report'] = tables_dict['daily_report'].merge(
                right=to_be_merged,
                on=['date'],
                how='left'
            )
            tables_dict['daily_report'].fillna(0, inplace=True)
    return tables_dict
