# pyDMNrules
An implementation DMN (Decision Model Notation) in Python, using the [pySFeel](https://pypi.org/project/pySFeel/) and [openpyxl](https://pypi.org/project/openpyxl/)
modules.

DMN rules are read from an Excel workbook.
Then data, matching the input variables in the DMN rules is passed to the decide() function.
The returned data contains the decision.

The passed Excel workbook must contain the two tabs 'Glossary' and 'Decision'.
Other tabs contain as many DMN rules tables as necessary.
## Glossary
The 'Glossary' tab must contain a table headed 'Glossary'.
This table must have exactly three columns with the headings 'Variable', 'Business Concept' and 'Attribute'.
The data in these three columns describe the inputs and outputs associated with the 'Decision'.
'Variable' can be any text and is used to pass data to and from pyDMNrules.
'Business Concept' and 'Attribute' must be valid S-FEEL names, but may **not** contain the dot, or period character. Vertically merged cells in the 'Business Concept' column are used to group multiple 'Variable'/'Attribute' pairs together into a single 'Businss Concept'. The 'Glossary' cannot have any Annotations.

Items in the Glossary can be outputs of one decision table and inputs in the next decision table, which makes it easy to support complex business models.

|   Glossary   |                      |               |
|--------------|----------------------|---------------|
| **Variable** | **Business Concept** | **Attribute** |
|   Customer   |   Customer           |   sector      |
|   OrderSize  |   Order              |   orderSize   |
|   Delivery   |                      |   delivery    |
|   Discount   |   Discount           |   discount    |
## Decision
The 'Decision' tab must contain a table headed 'Decision' with the headings 'Decisions' and 'Execute Decision Table'.
The 'Decisions' column contain a brief description of the DMN rules table which is named in 'Execute Decision Table' column. pyDMNrules will execute each decision table in this order. The 'Decision' table can have Annotations.

| Decision           |                            |
|--------------------|----------------------------|
| **Decisions**      | **Execute Decision Table** |
| Determine Discount | Discount                   |

The Decision table can be preceded by 'Input' columns.
- The headings of each 'Input' column must be a Variable from the Glossary. 
- The cells under each input heading are input test cells containing an expression about the input Variable, and which must evalutate to True, or False, depending upon the value of the input Variable.

pyDMNrules will evalutate all the input test cells before running the associate DMN rules table.
If all of the input test cells do not evaluate to True, then pyDMNrules will skip this DMN decision table and moves on to the next row
in the Decision table. These input cell are evaluated on the fly, which means that a preceeding DMN rules table can set or clear
values in the Glossary which can effect which DMN rules tables are included, and which DMN rules tables are excluded,
in the final decision.
## DMN rules tables
The DMN rules table(s), listed under **Execute Decision Table**, must exist 
on other spreadsheets in the Excel workbook and can be 'Decisions as Rows', 'Decisions as Columns' or 'Decision as Crosstab' rules tables.
### Decision as Rows rules tables
Decisions as Rows DMN rules tables have columns of inputs and columns of outputs,
with a double line vertical border delineating where input columns stop and output columns begin.
- The headings for the input and output columns must be Variables from the Glossary.
- The input test cells under the input heading must contain expressions about the input Variable,
which will evaluate to True or False, depending upon the value of the input Variable.
- The values in the output results cells, under the output headings, are the values that will be assigned to the output Variables, if all the input cells evaluate to True on the same row.

[ExampleRows.xlsx](https://github.com/russellmcdonell/pyDMNrules/blob/master/ExampleRows.xlsx) is an example fo a Decision as Rows DMN table.
### Decision as Columns rules tables
Decisions as Columns DMN rules tables have rows of inputs and rows of outputs,
with a double line horizontal border delineating where input rows stop and output rows begin.
- The headings on the left hand side of the decision table, for the input and output rows, must be Variables from the Glossary.
- The input test cells across the row must contain expressions about the input Variable,
which will evalutate to True or False, depending upon the value of the input Variable.
- The values in the output cells, across the row, are the values that will be assigned to the output Variable, if all the input cells evaluate to True in the same column.

[ExampleColumns.xlsx](https://github.com/russellmcdonell/pyDMNrules/blob/master/ExampleColumns.xlsx) is an example fo a Decision as Columns DMN table.
### Decision as Crosstab rules tables
Decision as Crosstab DMN rules tables have one output heading at the top left of the table.
- The horizontal and vertical headings, which must be Variables from the Glossary, are the input headings.
- Under the horizontal headings and besides the vertical headings are the input test cells.
- The output results cells form the body of the table and are assigned to the output Variable when the input cells in the same row and same column, all evaluate to True.

[ExampleCrosstab.xlsx](https://github.com/russellmcdonell/pyDMNrules/blob/master/ExampleCrosstab.xlsx) is an example fo a Decision as Crosstab DMN table.

# Strings:
Decision Model Notation specifies that strings must be enclosed in double quotes ("), as in "this is a string", or be italicized.
pyDMNrules does not look for italicized text, but it does try to interpret unequivocal strings as string.
So, **HIGH,DECLINE** are both strings; they are not numbers, nor dates, nor time periods.

pyDMNrules also recognizes entries from the Glossary, so **Patient.age** is not a string if 'Patient' is a 'Business Concept' in the Glossary
and 'age' is an attribute associated with the 'Patient' Business Concept in the Glossary.
When any expression containing Patient.age is evaluated, Patient.age will be replaced with the current value associated with that Glossary entry.

However, strings that may be ambiguous, must be enclosed in double quotes (").
Any string that contains spaces or a comma is ambiguous and must enclosed in double quotes (").
All strings can be enclosed in double quotes, so HIGH,DECLINE and "HIGH","DECLINE" are equivalent.

# USAGE:

    import pyDMNrules
    dmnRules = pyDMNrules.DMN()
    status = dmnRules.load('ExampleHPV.xlsx')
    if 'errors' in status:
        print('ExampleHPV.xlsx has errors', status['errors'])
        sys.exit(0)
    else:
        print('ExampleHPV.xlsx loaded')

    data = {}
    data['Participant Age'] = 36
    data['In Test of Cure'] = True
    data['Hysterectomy Flag'] = False
    data['Cancer Flag'] = False
    data['HPV-V'] = 'V0'
    data['Current Participant Risk Category'] = 'low'
    print('Testing',repr(data))
    (status, newData) = dmnRules.decide(data)
    print('Decision',repr(newData))
    if 'errors' in status:
        print('With errors', status['errors'])

For a Single Hit Policy DMN rules table, newData will be a decision dictionary of the decision.
For a Multi Hit Policy DMN rules tables newData will be a list of decison dictionaries; one for each matched rule.
The keys to each decision dictionary are
- 'Result' - for a Single Hit Policy DMN rules table this will be a  dictionary where all the keys will be 'Variables' from the Glossary and the matching the value will be the value of that 'Variable' after the decision was made. For a Multi Hit Policy DMN rules table this will be a list of decision dictionaries, one for each matched rule.
- 'Excuted Rule' - for a Single Hit Policy DMN rules table this will be a tuple of the Decision Table Description ('Decisions' from the 'Decision' table), the DMN rules table name ('Execute Decision Table' from the 'Decision' table) and the Rule number for the rule that matched in that DMN rules Table. For a Multi Hit Policy DMN rules table this will be the a list of tuples, being the Decision Table Description, DMN rules table name and matched Rule number for each matching rule.
- 'DecisionAnnotations'(optional) - list of tuples (heading, value) of the annotations from the 'Decision' table named in the 'Executed Rule' tuple.
- 'RuleAnnotations'(optional) - for a Single Hit Policy DMN rules table, this well be a list of tuples (heading, value) of the annotations for the matching rule, if there were any annotations for the matching rule. For a Multi Hit Policy DMN rules table this will be a list of the lists of any annotations for each matching rule, where an empty list means that the associated matching rule had no annotations.

If the Decision table contains multiple rows (multiple DMN rules tables run sequentially in order to make the decision) then the returned 'newData' will be a list of decision dictionaries, with each containing the keys 'Result', 'Excuted Rule', 'DecisionAnnotations'(optional) and 'RuleAnnotations'(optional), being one list entry for each DMN rules table used from the Decision table. The final enty in this list is the final decision. All other entries are the intermediate states involved in making the final decision.

    $ python3 HPV.py
    ExampleHPV.xlsx loaded
    Testing {'Participant Age': 36, 'In Test of Cure': True, 'Hysterectomy Flag': False, 'Cancer Flag': False, 'HPV-V': 'V0', 'Current Participant Risk Category': 'low'}
    Decision(newData) {'Result': {'Immune Deficient Flag': None, 'Hysterectomy Flag': False, 'Cancer Flag': False, 'In Test of Cure': True, 'Participant Age': 36.0, 'Current Participant Risk Category': 'low', 'HPV-V': 'V0', 'Cyto-S': None, 'Cyto-E': None, 'Cyto-O': None, 'Collection Method': None, 'Test Risk Code': 'L', 'New Participant Risk Category': 'low', 'Participant Care Pathway': 'toBeDetermined', 'Next Rule': 'CervicalRisk2'}, 'Executed Rule': ('Determine CervicalRisk', 'FirstTestOfCervicalRisk', '20'), 'DecisionAnnotations': [('Decides', 'Test risk')], 'RuleAnnotations': [('Test meaning', 'need more info')]}


# Testing
pyDMNrules reserves the spreadsheet name 'Test' which can be used for storing test data.
The function test() reads the test data, passes it through the decide() function and assembles the results which are returned to the caller.
### Unit Test data table(s)
The 'Test' spreadsheet must contain Unit Test data tables.
- Each Unit Test data table must be named with a 'Business Concept' from the Glossary.
- The heading of the table must be Variables from the Glossary associated with the Business Concept.
- The data, in each column, must be valid input data for the associated Variable.
- Each row is considered a unit test data set.
- Unit Test data tables can have 'Annotations'

### DMNrulesTest - the test that will be run
pyDMNrules also searches the 'Test' worksheet for a special table named 'DMNrulesTests' which must exist.
- The 'DMNrulesTests' table has input columns followed by output columns with a double line vertical border delineating where input columns stop and output columns begin.
- The headings for the input columns must be Business Concepts from the Glossary.
- The data in input columns must be one based indexes into the matching unit test data table.
- The headings for the output columns must be Variables from the Glossary.
- The data in output columns will be valid data for the matching Variable and are the expected values returned by the decide() function.
- The 'DMNrulesTests' table can have 'Annotations'

The test() function will process each row in the 'DMNrulesTests' table, getting data from the Unit Test data tables and building a data{} dictionary. The test() function then passes this data{} dictionary to the decide() function. The returned newData{} is then compared to the output data for the matching test in the 'DMNrulesTests' table. The data{}, newData{} and a list of mismatches, if any, is then appended to the list of results, which is eventually passed back to the caller of the test() function.

The returned list is a list of dictionaries, one for each test in the 'DMNrulesTests' table. The keys to this dictionary are
- 'Test ID' - the one based index into the 'DMNrulesTests' table which identifies which test which was run
- 'TestAnnotations'(optional) - the list of annotation for this test - not present if no annotations were present in 'DMNrulesTests'
- 'data' - the dictionary of assembed data passed to the decide() function
- 'newData' - the decision dictionary returned by the decide() function [see above]
- 'DataAnnotations'(optional) - the list of annotations from the unit test data tables, for the unit test sets used in this test - not present if no annotations were persent in any of the unit test data tables for the selected unit test sets.
- 'Mismatches'(optional) - the list of mismatch reports, one for each 'DMNrulesTests' table output value that did not match the value returned from the decide() function - not present if all the data returned from the decide() function matched the values in the 'DMNrulesTest' table.

# Note
If an output value should be the value of an input, then you can use the 'Variable' from the Glossary. However, if the output is a manuipulation of an input, then you will need to use the internal name for that variable, being the 'Business Concept' and the 'Attibute' concateneted with the period character. That is, 'Patient Age' is valid, but 'Patient Age + 5' is not. Instead you will need to use the syntax 'Patient.age + 5'


# USAGE:

    import pyDMNrules
    dmnRules = pyDMNrules.DMN()
    status = dmnRules.load('Therapy.xlsx')
    if 'errors' in status:
        print('Therapy.xlsx has errors', status['errors'])
        sys.exit(0)
    else:
        print('Therapy.xlsx loaded')
    (testStatus, results) = dmnRules.test()
    for test in range(len(results)):
        if 'Mismatches' not in results[test]:
            print('Test ID', results[test]['Test ID'], 'passed')
        else:
            print('Test ID', results[test]['Test ID'], 'failed')


    $ python3 Therapy.py
    Test ID 1 passed
    Test ID 2 passed
    Test ID 3 passed
    Decisions(results) [{'Test ID': 1, 'data': {'Encounter Diagnosis': 'Acute Sinusitis', 'Patient Age': 58, 'Patient Allergies': ['Penicillin', 'Streptomycin'], 'Patient Creatinine Level': 2, 'Patient Creatinine Clearance': 44.42, 'Patient Weight': 78, 'Patient Active Medication': 'Coumadin'}, 'newData': {'Result': {'Encounter Diagnosis': 'Acute Sinusitis', 'Recommended Medication': 'Levofloxacin', 'Recommended Dose': '250mg every 24 hours for 14 days', 'Warning': 'Coumadin and Levofloxacin can result in reduced effectiveness of Coumadin.', 'Error Message': None, 'Patient Age': 58.0, 'Patient Weight': 78.0, 'Patient Allergies': ['Penicillin', 'Streptomycin'], 'Patient Creatinine Level': 2.0, 'Patient Creatinine Clearance': 44.416667, 'Patient Active Medication': 'Coumadin'}, 'Executed Rule': ('Check Drug Interaction', 'WarnAboutDrugInteraction', 'Interaction-1')}, 'status': {}}, {'Test ID': 2, 'data': {'Encounter Diagnosis': 'Acute Sinusitis', 'Patient Age': 65, 'Patient Creatinine Level': 1.8, 'Patient Creatinine Clearance': 48.03, 'Patient Weight': 83}, 'newData': {'Result': {'Encounter Diagnosis': 'Acute Sinusitis', 'Recommended Medication': 'Amoxicillin', 'Recommended Dose': '250mg every 24 hours for 14 days', 'Warning': None, 'Error Message': None, 'Patient Age': 65.0, 'Patient Weight': 83.0, 'Patient Allergies': None, 'Patient Creatinine Level': 1.8, 'Patient Creatinine Clearance': 48.032407, 'Patient Active Medication': None}, 'Executed Rule': ('Check Drug Interaction', 'WarnAboutDrugInteraction', 'Interaction-2')}, 'status': {}}, {'Test ID': 3, 'data': {'Encounter Diagnosis': 'Diabetes', 'Patient Age': 27, 'Patient Creatinine Level': 1.88, 'Patient Weight': 110}, 'newData': {'Result': {'Encounter Diagnosis': 'Diabetes', 'Recommended Medication': None, 'Recommended Dose': None, 'Warning': None, 'Error Message': 'Sorry, this decision service can handle only Acute Sinusitis', 'Patient Age': 27.0, 'Patient Weight': 110.0, 'Patient Allergies': None, 'Patient Creatinine Level': 1.88, 'Patient Creatinine Clearance': None, 'Patient Active Medication': None}, 'Executed Rule': ('Create Message', 'ErrorMessage', 'Error-1')}, 'status': {}}]


Documentation:
More details can be found at [readthedocs](https://pyDMNrules.readthedocs.io/en/latest/)
