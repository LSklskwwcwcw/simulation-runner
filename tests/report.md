PS C:\Users\86139\Desktop\学习\simulation-runner> python -m unittest discover -s tests -v
test_missing_file_raises (test_csv_dealer.TestFileValidation.test_missing_file_raises) ... ok
test_wrong_extension_raises (test_csv_dealer.TestFileValidation.test_wrong_extension_raises) ... ok
test_accepts_parameter_value_boundaries (test_csv_dealer.TestHappyPath.test_accepts_parameter_value_boundaries)
design.md 写的是 [0,1]，0 和 1 都应当合法。 ... ok
test_accepts_plus_sign_and_scientific_notation (test_csv_dealer.TestHappyPath.test_accepts_plus_sign_and_scientific_notation) ... ok
test_converted_values_have_numeric_types (test_csv_dealer.TestHappyPath.test_converted_values_have_numeric_types) ... ok
test_multiple_rows_keep_file_order (test_csv_dealer.TestHappyPath.test_multiple_rows_keep_file_order) ... ok
test_single_row_returns_one_record (test_csv_dealer.TestHappyPath.test_single_row_returns_one_record) ... ok
test_duplicate_column_raises (test_csv_dealer.TestHeaderValidation.test_duplicate_column_raises) ... ok
test_empty_file_raises (test_csv_dealer.TestHeaderValidation.test_empty_file_raises) ... ok
test_extra_column_raises (test_csv_dealer.TestHeaderValidation.test_extra_column_raises) ... ok
test_header_only_raises (test_csv_dealer.TestHeaderValidation.test_header_only_raises) ... ok
test_missing_and_extra_columns_reported_together (test_csv_dealer.TestHeaderValidation.test_missing_and_extra_columns_reported_together) ... ok
test_missing_column_raises (test_csv_dealer.TestHeaderValidation.test_missing_column_raises) ... ok
test_duplicate_task_id_raises (test_csv_dealer.TestRowValidation.test_duplicate_task_id_raises) ... ok
test_empty_cell_raises (test_csv_dealer.TestRowValidation.test_empty_cell_raises) ... ok
test_float_task_id_raises (test_csv_dealer.TestRowValidation.test_float_task_id_raises) ... ok
test_infinite_parameter_value_raises (test_csv_dealer.TestRowValidation.test_infinite_parameter_value_raises) ... ok
test_infinite_temperature_raises (test_csv_dealer.TestRowValidation.test_infinite_temperature_raises)
1e400 能通过正则，但 float() 会溢出成 inf。 ... ok
test_negative_task_id_format_raises (test_csv_dealer.TestRowValidation.test_negative_task_id_format_raises) ... ok
test_non_numeric_parameter_value_raises (test_csv_dealer.TestRowValidation.test_non_numeric_parameter_value_raises) ... ok
test_non_numeric_task_id_raises (test_csv_dealer.TestRowValidation.test_non_numeric_task_id_raises) ... ok
test_non_numeric_temperature_raises (test_csv_dealer.TestRowValidation.test_non_numeric_temperature_raises) ... ok
test_parameter_value_above_range_raises (test_csv_dealer.TestRowValidation.test_parameter_value_above_range_raises) ... ok
test_parameter_value_below_range_raises (test_csv_dealer.TestRowValidation.test_parameter_value_below_range_raises) ... ok
test_zero_task_id_raises (test_csv_dealer.TestRowValidation.test_zero_task_id_raises)
'0' 能通过正则，但违反 > 0 的约束。 ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.298s

OK