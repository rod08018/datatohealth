import pandas as pd


def clean_table_data(table, key):
    time_list = [
        'create_time',
        'update_time',
        'start_time',
        'end_time',
        'Time of Measurement',
        'original_wake_up_time',
        'original_bed_time'
    ]
    table.fillna(0, inplace=True)
    for field in time_list:
        for column in table.columns:
            if field in column:
                table[column] = pd.to_datetime(table[column])
    if 'activity_day_summary' in key:
        table['day_time'] = pd.to_datetime(table['day_time'])
        table['walk_time'] = table['walk_time'] / 60000
        table['longest_idle_time'] = table['longest_idle_time'] / 60000
        table['run_time'] = table['run_time'] / 60000
        return table
    elif 'calories_burned_details' in key:
        table['calories_burned.update_time'] = pd.to_datetime(table['calories_burned.update_time'])
        calories_table_list = [column for column in table.columns if column not in ['version']]
        return table[
            calories_table_list
        ]
    elif 'exercise' in key:
        exercise_table_list = [column for column in table.columns if column not in
                               [
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
        return table[
            weight_table_list
        ]
