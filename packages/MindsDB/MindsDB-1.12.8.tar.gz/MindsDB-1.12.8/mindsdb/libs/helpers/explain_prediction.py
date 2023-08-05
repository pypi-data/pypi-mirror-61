import numpy as np
from mindsdb.libs.constants.mindsdb import *
from mindsdb.libs.helpers.general_helpers import value_isnan


def explain_prediction(lmd, prediction_row, confidence, pred_col):
    '''
        Given a row contianing a prediction, it tries to use the information in it plus the metadata generated by the ModelAnalyzer and StatsGenerator in order to explain "why" the prediction took said value.
        :param prediction_row: The row that was predicted by the model backend and processed by mindsdb
        :return: A, hopefully human readable, string containing the explaination
    '''
    if lmd['column_importances'] is None or len(lmd['column_importances']) < 2:
        important_cols = [col for col in lmd['columns'] if col not in lmd['predict_columns']]
        useless_cols = []
    else:
        top_20_val = np.percentile(list(lmd['column_importances'].values()),80)
        bottom_20_val = np.percentile(list(lmd['column_importances'].values()),20)

        important_cols = [col for col in lmd['column_importances'] if lmd['column_importances'][col] >= top_20_val]
        useless_cols = [col for col in lmd['column_importances'] if lmd['column_importances'][col] <= bottom_20_val]

    explain_predictions = {}

    predicted_val = prediction_row[pred_col]
    col_stats = lmd['column_stats'][pred_col]
    col_type = col_stats['data_type']

    if 'histogram' in col_stats and ['histogram'] is not None:
        histogram_x = None
        histogram_keys = col_stats['histogram']['x']
        if col_type == DATA_TYPES.NUMERIC:
            for i in range(len(histogram_keys)):
                if i == 0:
                    if histogram_keys[i] >= predicted_val:
                        histogram_x = histogram_keys[0]
                if i == len(histogram_keys) - 1:
                        if histogram_keys[i] <= predicted_val:
                            histogram_x = histogram_keys[0]
                else:
                    if histogram_keys[i] <= predicted_val or predicted_val > histogram_keys[i+1]:
                        histogram_x = histogram_keys[0]
        else:
            histogram_x = predicted_val

        bucket_occurances = col_stats['histogram']['y'][col_stats['histogram']['x'].index(histogram_x)]
        total_occuraces = sum(col_stats['histogram']['y'])

        percentage_bucket_percentage = round(100*bucket_occurances/total_occuraces, 2)

        column_confidence = confidence * 100

        confidence_str = 'very confident'
        if confidence < 0.80:
            confidence_str = 'confident'
        if confidence < 0.60:
            confidence_str = 'somewhat confident'
        if confidence < 0.40:
            confidence_str = 'not very confident'
        if confidence < 0.20:
            confidence_str = 'not confident'

        if percentage_bucket_percentage < 2:
            column_explaination = f'A similar value for the predicted column {pred_col} occurs rarely in your dataset'

            if column_confidence >= 70:
                column_explaination += ', in spite of this, due to the quality of the input data and the model, we are very confident this prediction is correct.'

            if column_confidence < 70 and column_confidence > 30:
                column_explaination += ', it is partially because of this reason that we are only somewhat confident this prediction is correct.'

            if column_confidence <= 30:
                column_explaination += ', it is partially because of this reason that we aren\'t confident this prediction is correct.'

        elif percentage_bucket_percentage < 12.5:
            column_explaination = f'A similar value for the predicted column {pred_col} occurs a moderate amount of times in your dataset'

            if column_confidence >= 70:
                column_explaination += ', we are very confident this prediction is correct.'

            if column_confidence < 70 and column_confidence > 30:
                column_explaination += ', we are only somewhat confident this prediction is correct.'

            if column_confidence <= 30:
                column_explaination += ', you\'r input data might be of sub-par qualkity, since we aren\'t confident this prediction is correct.'

        else:
            column_explaination = f'A similar value for the predicted column {pred_col} occurs very often in your dataset'

            if column_confidence >= 70:
                column_explaination += ', it\'s partially because of this plaethora of examples that we can be very confident this prediction is correct.'

            if column_confidence < 70 and column_confidence > 30:
                column_explaination += ', still we can only be somewhat confident this prediction is correct.'

            if column_confidence <= 30:
                column_explaination += ', in spite of this, possibly due to poor input data quality, we aren\'t confident this prediction is correct.'

        explain_predictions[pred_col] = column_explaination

    else:
        explain_predictions[pred_col] = f'Column {pred_col} is of type {col_type} and thus it\'s impossible for us to make statistical inferences about it.'

    explain_inputs = {}

    for icol in important_cols:
        if prediction_row[icol] is None or value_isnan(prediction_row[icol]):
            explain_inputs[icol] = f'The column {icol} is very important for this model to predict correctly. Since it\'s missing it\'s quite likely that the quality of this prediction is lacking because of this.'
        else:
            explain_inputs[icol] = f'The value of the column {icol} played a large role in generating this prediction.'

    for icol in useless_cols:
        if prediction_row[icol] is None or value_isnan(prediction_row[icol]):
            explain_inputs[icol] = f'The fact that {icol} is missing is probably not very relevant for this prediction.'
        else:
            explain_inputs[icol] = f'The column {icol} is probably not very relevant for this prediction.'

    join_str = '\n\n*'
    explaination = join_str + join_str.join(explain_predictions.values())
    explaination += join_str + join_str.join(explain_inputs.values())
    return explaination
